---
description: 貼入 JD 後自動產出客製化履歷 JSON 並生成 PDF
---

# JD 客製化履歷產出 Workflow

當使用者貼入一份 Job Description 並觸發此 workflow 時，執行以下步驟：

## 步驟

### 1. 讀取使用者資料

讀取以下檔案，完整理解使用者的背景與能力：

- `data/master_profile.json`（若不存在則使用 `data/master_profile.example.json`）— 原始技能、經歷、學歷
- `data/experience_notes.md` — 各份工作的詳細描述、量化數據、實際職責
- `data/resume_example.json` — 參考 base 版的 summary 和 bullet 寫法風格（作為品質標竿）

### 2. 解析 JD 並萃取關鍵字

從 JD 中提取：

**A. 核心能力詞（3-5 個）**
- 直接從 JD 原文抓取的關鍵能力詞（例如：`cross-functional collaboration`、`data-driven decision making`）
- 這些詞將作為後續 bulletin 撰寫的「必出現關鍵字」

**B. 硬性要求 vs. 加分項**
- Required Skills：必須在 summary 和 bullets 中覆蓋
- Preferred Qualifications：盡量覆蓋，但不強制

**C. 職位核心本質**
- 這個角色日常在做什麼（e.g. B2B 客戶對接、數據分析、產品規劃）

### 3. 決定包裝策略

根據分析決定如何調整：

- `personal.title` — 一句話定位，直接對齊 JD 的職能方向與層級
- `personal.summary` — 3 句話結構（詳見 resume-conventions skill），第一句必須用 JD 的語言描述自己，覆蓋全部 Required Skills
- `experience[].title` — 可微調 title 來對齊 JD（但不可造假）
- `experience[].bullets` — 每條 bullet 必須包含至少 1 個萃取出的核心能力詞 + 量化數據；用 JD 的語言重新描述同一件事
- `skills` — 第一個分類的名稱直接對應 JD 最重視的能力方向；分類順序按 JD 重要性排列

### 4. 產出客製化 JSON

- 檔名規則：`data/resume_{company}_{role}.json`（全小寫、底線分隔）
- 從 JD 中提取公司名稱和職位簡稱作為命名依據
- JSON 結構必須遵守 `resume-conventions` skill 中定義的 schema

### 5. 執行 generate.py 產出 PDF

```bash
.venv/bin/python3 scripts/generate.py --profile resume_{company}_{role}
```

### 6. 回報結果

- 回報 JSON 檔案路徑和 PDF 檔案路徑
- 簡要說明做了哪些關鍵調整：
  - 萃取到哪些核心能力詞
  - title / summary 如何對齊 JD
  - 哪些 bullets 被重寫、怎麼重寫
  - skills 如何重組
- 提示使用者可以接著執行 `/jd-aiproof` 對履歷做 AI HR 模擬審查

## 注意事項

- 全程使用**繁體中文**回答
- Bullets 要具體，用 action verb 開頭，盡量包含量化數據
- **不可造假**：只能從 master_profile 和 experience_notes.md 中已有的素材去包裝調整，不能憑空捏造經歷
- 如果 JD 已經存在於 `jobs/{Company}/{Role}/JD.md`，優先讀取該檔案
- 萃取核心能力詞時，優先使用 JD 的原始措辭，不要自己翻譯或改寫
