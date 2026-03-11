#!/usr/bin/env python3
"""
Resume Generator
================
Generates HTML and PDF resumes from JSON data using templates.

Usage:
  python generate.py                              # Generate from resume_example.json
  python generate.py --profile resume_example     # Generate specific profile
  python generate.py --preview                    # Open in browser after generation
  python generate.py --html-only                  # Only generate HTML
  python generate.py --pdf-only                   # Only generate PDF
"""

from __future__ import annotations
import os
import sys

# ── Python version guard ────────────────────────────────────────────────────
if sys.version_info < (3, 8):
    sys.exit(
        f"❌ Python 3.8+ required (you have {sys.version_info.major}.{sys.version_info.minor}).\n"
        "   Please upgrade: https://www.python.org/downloads/"
    )

# ── venv detection ──────────────────────────────────────────────────────────
_in_venv = sys.prefix != sys.base_prefix
_venv_exists = os.path.isdir(os.path.join(os.path.dirname(__file__), "..", ".venv"))
if not _in_venv and _venv_exists:
    print(
        "⚠️  .venv exists but you're not using it.\n"
        "   Run: source .venv/bin/activate && python3 scripts/generate.py\n"
        "   Or:  .venv/bin/python3 scripts/generate.py\n"
    )

import json
import re
import argparse
import webbrowser
from pathlib import Path

# macOS: auto-inject homebrew lib path so WeasyPrint can find libgobject, etc.
if sys.platform == "darwin":
    homebrew_lib = "/opt/homebrew/lib"
    existing = os.environ.get("DYLD_FALLBACK_LIBRARY_PATH", "")
    if homebrew_lib not in existing:
        os.environ["DYLD_FALLBACK_LIBRARY_PATH"] = (
            f"{homebrew_lib}:{existing}" if existing else homebrew_lib
        )

try:
    from weasyprint import HTML, CSS
    WEASYPRINT_AVAILABLE = True
except (ImportError, OSError) as e:
    WEASYPRINT_AVAILABLE = False
    _WEASYPRINT_ERROR = str(e)

# Paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
TEMPLATES_DIR = PROJECT_ROOT / "templates"
OUTPUT_DIR = PROJECT_ROOT / "output"


def load_json(path: Path) -> dict:
    """Load JSON data from file."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# ── Validation ───────────────────────────────────────────────────────────────

EXAMPLE_SIGNALS = {"Mike Chen", "Jane Doe", "John Doe"}
EXAMPLE_EMAIL_DOMAIN = "@example.com"


def validate_resume_data(data: dict, profile_name: str) -> None:
    """Validate resume JSON structure. Raises SystemExit with a friendly message on failure."""
    errors: list[str] = []

    # Top-level sections
    for section in ("personal", "education", "experience", "skills"):
        if section not in data:
            errors.append(f"  • Missing top-level key: '{section}'")

    if errors:
        _fail_validation(profile_name, errors)

    personal = data["personal"]
    required_personal = {
        "name_en": "English name",
        "email": "email address",
        "location": "location",
        "title": "job title",
    }
    for key, label in required_personal.items():
        if not personal.get(key, "").strip():
            errors.append(f"  • personal.{key} ({label}) is missing or empty")

    if not isinstance(data.get("experience", None), list):
        errors.append("  • 'experience' must be a list")
    elif not data["experience"]:
        errors.append("  • 'experience' list is empty — add at least one entry")

    if not isinstance(data.get("education", None), list):
        errors.append("  • 'education' must be a list")

    if not isinstance(data.get("skills", None), dict):
        errors.append("  • 'skills' must be an object (dict)")

    if errors:
        _fail_validation(profile_name, errors)


def _fail_validation(profile_name: str, errors: list[str]) -> None:
    msg = (
        f"❌ Invalid resume data in '{profile_name}.json':\n"
        + "\n".join(errors)
        + "\n\nPlease fix the issues above and try again."
    )
    sys.exit(msg)


def check_example_profile(data: dict, profile_name: str) -> None:
    """Warn if the profile looks like the bundled example data."""
    personal = data.get("personal", {})
    name_en = personal.get("name_en", "")
    email = personal.get("email", "")
    if name_en in EXAMPLE_SIGNALS or email.endswith(EXAMPLE_EMAIL_DOMAIN):
        print(
            f"\n⚠️  Warning: '{profile_name}.json' appears to contain example/placeholder data "
            f"(name: '{name_en}', email: '{email}').\n"
            "   Did you forget to create your own profile?\n"
            "   Run: cp data/master_profile.example.json data/master_profile.json\n"
            "   Then use /profile-init to fill in your real data.\n"
        )


def load_template(name: str = "default") -> str:
    """Load HTML template."""
    template_path = TEMPLATES_DIR / f"{name}.html"
    with open(template_path, "r", encoding="utf-8") as f:
        return f.read()


def simple_render(template: str, data: dict) -> str:
    """
    Simple Mustache-like template rendering.
    Supports: {{variable}}, {{#list}}...{{/list}}, {{.}} for list items
    """
    result = template

    # Replace simple variables
    for key, value in data.items():
        if isinstance(value, str):
            result = result.replace(f"{{{{{key}}}}}", value)

    # Handle list sections
    def replace_section(match):
        section_name = match.group(1)
        section_content = match.group(2)

        if section_name not in data:
            return ""

        items = data[section_name]
        if not isinstance(items, list):
            return section_content if items else ""

        output = []
        for item in items:
            item_content = section_content
            if isinstance(item, dict):
                for k, v in item.items():
                    if isinstance(v, str):
                        item_content = item_content.replace(f"{{{{{k}}}}}", v)
                    elif isinstance(v, list):
                        # Handle nested lists (like bullets)
                        nested_pattern = rf"\{{\{{#{k}\}}\}}(.*?)\{{\{{/{k}\}}\}}"
                        nested_match = re.search(nested_pattern, item_content, re.DOTALL)
                        if nested_match:
                            nested_content = nested_match.group(1)
                            nested_output = "".join(
                                nested_content.replace("{{.}}", str(b)) for b in v
                            )
                            item_content = re.sub(nested_pattern, nested_output, item_content, flags=re.DOTALL)
            elif isinstance(item, str):
                item_content = item_content.replace("{{.}}", item)
            output.append(item_content)

        return "".join(output)

    # Process sections
    section_pattern = r"\{\{#(\w+)\}\}(.*?)\{\{/\1\}\}"
    while re.search(section_pattern, result, re.DOTALL):
        result = re.sub(section_pattern, replace_section, result, flags=re.DOTALL)

    # Process markdown bold (**text**)
    result = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", result)

    return result


def prepare_template_data(resume_data: dict) -> dict:
    """Prepare data for template rendering."""
    personal = resume_data["personal"]

    # Extract twitter handle
    twitter = personal.get("twitter", "")
    twitter_handle = twitter.lstrip("@") if twitter else ""

    # Prepare skills list
    skills_list = [
        {"category": cat, "items": ", ".join(items) if isinstance(items, list) else items}
        for cat, items in resume_data.get("skills", {}).items()
    ]

    return {
        # Personal
        "name_en": personal.get("name_en", ""),
        "name_zh": personal.get("name_zh", ""),
        "title": personal.get("title", ""),
        "location": personal.get("location", ""),
        "email": personal.get("email", ""),
        "phone": personal.get("phone", ""),
        "twitter": personal.get("twitter", ""),
        "twitter_handle": twitter_handle,
        "twitter_url": personal.get("twitter_url", f"https://x.com/{twitter_handle}"),
        "website": personal.get("website", ""),
        "website_url": (
            w if (w := personal.get("website", "")).startswith(("http://", "https://"))
            else f"https://{w}" if w else ""
        ),
        "linkedin": personal.get("linkedin", ""),
        "github": personal.get("github", ""),
        "summary": personal.get("summary", ""),

        # Sections - rename title to job_title to avoid conflict
        "experience": [
            {**exp, "job_title": exp.get("title", "")}
            for exp in resume_data.get("experience", [])
        ],
        "education": resume_data.get("education", []),

        # Projects (backward compatible: supports both "projects" and legacy "personal_investment")
        "project_section_title": (
            resume_data.get("projects", resume_data.get("personal_investment", {}))
            .get("section_title", "Projects")
        ),
        "project_items": [
            {**item, "item_title": item.get("title", "")}
            for item in (
                resume_data.get("projects", resume_data.get("personal_investment", {}))
                .get("items", [])
            )
        ],

        # Skills
        "skills_list": skills_list,
    }


def get_output_folder(profile_name: str) -> str:
    """Auto-infer output folder from profile name.

    Generic profiles map to named folders.
    Company-specific profiles (resume_{company}_{role}) map to apps/{Company-Role}/.
    """
    generic_map = {
        "resume_base": "general",
        "resume_example": "example",
        "resume_pm": "pm",
        "resume_risk_ops": "ops",
        "resume_strategy": "strategy",
    }

    if profile_name in generic_map:
        return generic_map[profile_name]

    # Company-specific: resume_binance_risk_bap → apps/Binance-Risk-Bap
    name = profile_name.removeprefix("resume_")
    parts = name.split("_")
    folder_name = "-".join(p.capitalize() for p in parts)
    return f"apps/{folder_name}"


def generate_resume(
    template_name: str = "default",
    profile_name: str = "resume_example",
    output_name: str = "",
    generate_html: bool = True,
    generate_pdf: bool = True,
) -> tuple[Path | None, Path | None]:
    """Generate resume HTML and/or PDF from data and template.

    Returns:
        Tuple of (html_path, pdf_path) - either can be None if not generated
    """
    # Load & validate data
    resume_data = load_json(DATA_DIR / f"{profile_name}.json")
    validate_resume_data(resume_data, profile_name)
    check_example_profile(resume_data, profile_name)

    # Auto-infer output folder if not specified
    if not output_name:
        folder = get_output_folder(profile_name)
        name_en = resume_data["personal"]["name_en"].replace(" ", "_")
        output_name = f"{folder}/Resume_{name_en}"

    # Ensure output directory exists
    final_output_dir = OUTPUT_DIR
    if "/" in output_name:
        final_output_dir = OUTPUT_DIR / Path(output_name).parent

    final_output_dir.mkdir(parents=True, exist_ok=True)

    template = load_template(template_name)

    # Prepare data and render
    template_data = prepare_template_data(resume_data)
    html_output = simple_render(template, template_data)

    html_path = None
    pdf_path = None

    # Write HTML
    if generate_html:
        html_path = OUTPUT_DIR / f"{output_name}.html"
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html_output)
        print(f"✅ HTML generated: {html_path}")

    # Write PDF
    if generate_pdf:
        if not WEASYPRINT_AVAILABLE:
            print("❌ PDF generation failed. WeasyPrint could not load system libraries.")
            print("   macOS fix: brew install cairo pango gdk-pixbuf libffi")
            print("   Linux fix: sudo apt install libcairo2 libpango-1.0-0 libpangocairo-1.0-0")
            print(f"   Detail: {_WEASYPRINT_ERROR}")
        else:
            pdf_path = OUTPUT_DIR / f"{output_name}.pdf"
            # Use Letter size (8.5in x 11in) for US resume standard
            # PDF-safe font CSS: override CDN fonts with system fonts so WeasyPrint
            # doesn't need network access. HTML preview still uses Google Fonts CDN.
            pdf_font_css = CSS(string="""
                @page { size: letter; margin: 0; }
                body {
                    font-family: 'Helvetica Neue', Helvetica, Arial,
                                 'Noto Sans', sans-serif !important;
                }
            """)
            # Set base_url to templates dir so relative paths (../assets/) resolve correctly
            base_url = str(TEMPLATES_DIR) + "/"
            HTML(string=html_output, base_url=base_url).write_pdf(pdf_path, stylesheets=[pdf_font_css])
            print(f"✅ PDF generated: {pdf_path}")

    return html_path, pdf_path


def main():
    parser = argparse.ArgumentParser(description="Generate resume from JSON data")
    parser.add_argument("--template", type=str, default="default", help="Template name")
    parser.add_argument("--profile", type=str, default="resume_example", help="Profile JSON filename (without .json)")
    parser.add_argument("--output", type=str, default="", help="Output filename (without extension). Defaults to auto-inferred path.")
    parser.add_argument("--preview", action="store_true", help="Open in browser after generation")
    parser.add_argument("--html-only", action="store_true", help="Only generate HTML, skip PDF")
    parser.add_argument("--pdf-only", action="store_true", help="Only generate PDF, skip HTML")

    args = parser.parse_args()

    # Determine what to generate
    generate_html = not args.pdf_only
    generate_pdf = not args.html_only

    html_path, pdf_path = generate_resume(
        template_name=args.template,
        profile_name=args.profile,
        output_name=args.output,
        generate_html=generate_html,
        generate_pdf=generate_pdf,
    )

    if args.preview and html_path:
        webbrowser.open(f"file://{html_path.absolute()}")


if __name__ == "__main__":
    main()
