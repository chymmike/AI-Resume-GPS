---
name: resume-conventions
description: Resume JSON schema 規範與命名慣例，AI 在此專案內生成或修改 resume JSON 時自動遵守
---

# Resume Conventions

本專案所有 resume JSON 檔案必須遵守以下規範。

## JSON Schema

每份 resume JSON 必須包含以下頂層欄位：

```json
{
    "personal": {},
    "education": [],
    "experience": [],
    "projects": {},
    "skills": {}
}
```

### `personal` 欄位

| 欄位 | 必填 | 說明 |
|------|------|------|
| `name_zh` | 選填 | 中文姓名 |
| `name_en` | ✅ | 英文姓名 |
| `title` | ✅ | 一句話定位，需對齊目標 JD 方向 |
| `summary` | 條件必填 | 客製化履歷必須有；三句話結構（詳見下方規範） |
| `location` | ✅ | 所在地 |
| `email` | ✅ | 電子信箱 |
| `phone` | ✅ | 聯絡電話 |
| `twitter` | 選填 | Twitter/X handle |
| `twitter_url` | 選填 | Twitter/X URL |
| `website` | 選填 | 個人網站 |
| `linkedin` | ✅ | LinkedIn URL |
| `github` | 選填 | GitHub URL |

### `education` 欄位

陣列，每項包含：`school`, `degree`, `period`, `highlights`（陣列）。
教育資料**不隨 JD 變動**，直接沿用 master_profile。

### `personal.summary` AI-Proof 規範

> 客製化履歷（`/jd-resume` 產出的）必須有 summary，且遵守三句話結構：

| 句次 | 內容 | 規則 |
|-----|------|------|
| 第 1 句 | 直接命中 JD 的職能定位 | **使用 JD 的原始措辭**定義自己；覆蓋全部 Required Skills 關鍵字 |
| 第 2 句 | 點出最強量化成就 | 必須包含具體數字；應是對目標 JD 最有說服力的成就 |
| 第 3 句 | 延伸優勢或消除 Risk | 補充額外強項，或主動交代職涯轉換邏輯以消除 AI HR 的疑問 |

> ❌ 弱 summary：「Experienced professional with background in blockchain and operations."
> ✅ 強 summary：「Full-stack SWE with 3+ years shipping distributed systems in Go and TypeScript across fintech and SaaS. Proven track record in high-availability payment infrastructure at Stripe (50K+ req/sec, 99.99% uptime) and owned end-to-end from API design to CI/CD. Transitioned from startup full-stack roles to fintech scale to deepen system reliability expertise."

### `experience` 欄位

陣列，每項包含：

| 欄位 | 說明 |
|------|------|
| `company` | 公司名稱 |
| `title` | 職位名稱，可微調以對齊 JD 但不可造假 |
| `period` | 任職期間 |
| `bullets` | 陣列，3-4 條。每條用 action verb 開頭，盡量含量化數據 |
| `tags` | 陣列，用於內部分類（不顯示在履歷上） |

**Bullet 寫法規則（AI-HR Proof）：**

每條 bullet 必須**同時符合**以下四個條件：

1. **Action Verb 開頭**（e.g. Architected, Designed, Led, Reduced, Optimized, Shipped）
2. **含量化數據**：至少一個數字（百分比、金額、倍數、數量）；無法量化的經歷不要放進來
3. **含 JD 核心能力詞**：至少語意對齊 JD 的其中一個 Required Skill（可改寫措辭但指向相同能力）
4. **結果導向結尾**：句中或句尾說明「造成了什麼影響」，而非只描述做了什麼

> ❌ 弱 bullet：「Worked on migrating the billing service to a new architecture."
> ✅ 強 bullet：「Led migration of monolithic billing service to event-driven architecture (Kafka), **reducing P99 latency by 40%** and enabling independent team deployments at scale."

長度控制在 1-2 行。

### `projects` 欄位

```json
{
    "section_title": "Projects",
    "items": [
        { "title": "...", "description": "..." }
    ]
}
```

此區塊**不隨 JD 變動**，直接沿用 master_profile。
`section_title` 可自訂（預設 "Projects"），支援 legacy `personal_investment` key（向下相容）。

### `skills` 欄位

Object，key 為類別名稱，value 為技能陣列：

```json
{
    "Category Name": ["Skill 1", "Skill 2", "..."]
}
```

**規則：**
- 分 3-5 個類別
- 每類 4-6 個項目
- 類別名稱應對齊 JD 要求的能力方向
- JD 最重要的技能類別放最前面

## 檔案命名規範

| 項目 | 格式 | 範例 |
|------|------|------|
| JSON 檔名 | `resume_{company}_{role}.json` | `resume_google_pm.json` |
| 全小寫 | ✅ | `resume_example_analyst.json` |
| 分隔符 | 底線 `_` | `resume_acme_corp_ops.json` |

## 不可造假原則

所有履歷內容必須基於以下兩份檔案中已有的素材進行包裝調整：
- `data/master_profile.example.json`（或你自己的 `master_profile.json`）
- `data/experience_notes.md`

允許的調整：重新措辭、調整強調重點、重組順序。
不允許的調整：憑空捏造經歷、誇大數字、虛構技能。

## 兩份來源文件的分工

在讀取使用者資料時，這兩份文件的用途不同：

| | `master_profile.json` | `experience_notes.md` |
|---|---|---|
| **語言** | 英文 | 中文或英文均可 |
| **詳細程度** | 精簡版（3-4 bullets/job） | 完整原始筆記（越細越好） |
| **bullets 風格** | 素材版：記錄事實，不需 JD 對齊 | 口語描述，幕後細節也要包含 |
| **用途** | 直接作為 resume 的基底 | 供 AI 撰寫時選取細節與數字 |

> 撰寫 `resume_*.json` 的 bullets 時：
> - **從 `experience_notes.md` 取用細節和量化數字**
> - **以 `master_profile.json` 的素材版 bullet 作為骨架**
> - 再套用 AI-HR Proof 四條規則對齊 JD

如需建立或更新這兩份文件，請使用 `/profile-init` workflow，
詳細格式規範見 `profile-conventions` skill。
