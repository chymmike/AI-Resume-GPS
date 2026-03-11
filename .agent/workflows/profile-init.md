---
description: 引導新使用者完成四輪訪談，產出 master_profile.json 和 experience_notes.md
---

# Profile 初始化 Workflow

當使用者想建立自己的個人資料時，執行以下步驟。
這個 workflow 的目的是產出 `data/master_profile.json` 和 `data/experience_notes.md`。

## 前置說明

執行前先讀取以下規範，確保產出的格式正確：
- `.agent/skills/profile-conventions/SKILL.md` — master_profile 和 experience_notes 的填寫規範
- `.agent/skills/resume-conventions/SKILL.md` — master_profile JSON schema

---

## 開場：選擇模式

先問使用者：

> 你想怎麼開始？
>
> **A）** 我有現成的履歷，我可以貼上（Markdown、純文字，或 PDF 複製的內容都可以）
> **B）** 我沒有現成履歷，請從頭帶我建立

根據回答進入對應模式。

---

## 模式 A：貼入履歷 → 提取 + 補問

### A-1. 請使用者貼入履歷

> 請把你的履歷貼進來（純文字即可，不支援上傳檔案）。
> 如果你的履歷是 PDF，請全選複製後貼上。

### A-2. 提取結構化資料

從使用者貼入的履歷文字中，提取以下資訊，對應到 `master_profile.json` 和 `experience_notes.md` 的欄位：

- `personal`：姓名、聯絡方式、位置、對外連結
- `education`：學校、學位、年份、亮點
- `experience`：每段工作的公司、職稱、期間、職責、成果
- `skills`：技能清單
- `projects`：Side projects

### A-3. 掃描缺口並補問

提取完成後，輸出缺口清單，例如：

```
✅ 已從履歷提取：
- 基本資料（姓名、Email、LinkedIn）
- 學歷（2 段）
- 工作經歷（3 段，含職稱和職責）
- 技能清單

❓ 需要補充下列資訊（我會逐一詢問）：
- [公司 A] 有沒有更具體的量化數據？
- [公司 B] 幕後細節：你為什麼離開？這段工作遇到什麼挑戰？
- Side projects：有沒有可量化的成果（stars、下載數、得獎等）？
```

然後**逐項補問**，不重複詢問已有的資訊。

### A-4. 產出兩份檔案

補問完成後，整合履歷原始資料 + 補問資訊，產出：
- `data/master_profile.json`
- `data/experience_notes.md`

---

## 模式 B：從頭建立（四輪訪談）

### 開場白

> 我會用四個階段引導你建立個人履歷資料庫。這些資料只會存在你的本機，之後每次求職都可以直接用。
>
> 各階段耗時約：基本資料 1 分鐘、學歷 2 分鐘、每段工作 5-10 分鐘。

### 第 1 輪：基本資料

依序詢問：

1. 姓名（中文名 + 英文名）
2. 現在在哪個城市？
3. 聯絡方式：Email、電話
4. 對外連結（有幾個填幾個）：LinkedIn、GitHub、個人網站、Twitter/X

### 第 2 輪：學歷

對每段學歷依序詢問：

1. 學校名稱（英文）
2. 科系 / 學位（e.g. B.S. in Computer Science）
3. 就讀期間（年份）
4. 有什麼值得一提的？（GPA、得獎、助教——不確定就跳過）

> 學歷從最高學歷開始填。交換學生算一段。

### 第 3 輪：工作經歷（每段重複）

先問：**你有幾段正式工作經驗？**

對每段工作，依序詢問：

**A. 公司基本資訊**
- 公司名稱和你的職稱？任職期間？
- 這家公司規模多少人？B2B 還是 B2C？

**B. 工作內容**
- 你每天主要在做什麼？
- 你最主要負責的 1-3 件事是什麼？

**C. 成果與數字**
- 有什麼成果比較明顯的事情？能不能給我一些數字？
- 有沒有主導或參與任何專案？結果怎樣？

**D. 幕後細節**
- 有什麼「履歷不會寫但你做過」的事嗎？
- 為什麼離開（或為什麼還在）？

### 第 4 輪：補充資料

1. **Side Projects**：名稱、一句話說明、可量化成果？
2. **技能與工具**：最熟悉的技術 / 工具？語言能力？

---

## 產出步驟（模式 A 和 B 共用）

### 1. 產出 `data/master_profile.json`

遵守 `resume-conventions` skill 的 JSON schema。
`experience[].bullets` 使用**素材版**（不需 JD 對齊，只要清楚記錄）。

### 2. 產出 `data/experience_notes.md`

遵守 `profile-conventions` skill 的格式規範。

### 3. 回報結果

```
✅ 已產出：
- data/master_profile.json
- data/experience_notes.md

📋 資料品質評估：
- X 段工作經歷
- 量化數據豐富度：高 / 中 / 建議補充

💡 建議補充的內容：
- [列出仍薄弱的部分]

下一步：可以貼入 JD 後執行 /jd-match 或 /jd-resume
```

## 注意事項

- 全程使用**繁體中文**
- 模式 B 訪談時語氣要自然，像對話，不要像填表格
- 使用者回答太簡短時，追問細節（e.g. 「這個你能給我一個數字嗎？」）
- 沒有資料的欄位填 `""` 或 `[]`，不要捏造
