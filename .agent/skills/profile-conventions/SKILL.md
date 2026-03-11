---
name: profile-conventions
description: 定義 master_profile.json 和 experience_notes.md 的內容規範，AI 在讀寫這兩份檔案時自動遵守
---

# Profile Conventions

本規範定義使用者的「個人資料」應如何結構化儲存。
這兩份檔案是所有履歷產出的**唯一真實來源**，品質越高，後續客製化履歷越強。

---

## `master_profile.json` 規範

### 定義

`master_profile.json` 是你經歷的**原始完整版本**，不針對任何特定職位調整。
它應包含所有真實發生過的事情，供後續 `/jd-resume` 選取和重新包裝。

### 填寫原則

1. **原始數字優先**：量化數據直接填原始數字（e.g. `"200+ cases"`、`"$3M+"`），不要描述化
2. **不需 JD 對齊**：bullets 不用刻意加關鍵字，只要說清楚「做了什麼、結果是什麼」
3. **寧多勿少**：即使某些事看起來不重要，先填進來；後續 `/jd-resume` 會選取最相關的
4. **真實即可**：不需要美化措辭，這份文件是 AI 讀的原始素材

### `experience[].bullets` 的寫法（master_profile 版）

> 與 `resume_*.json` 的 bullets 不同：這裡是**素材版**，不需要同時滿足「四條件」
> 只要清楚記錄「做了什麼 + 結果數字」即可

範例：
```json
"bullets": [
    "Handled 200+ fraud investigation cases, conversion rate improved from 10% to 30%",
    "Built automation tool with engineers, reduced tracing time from 3hr to 1hr",
    "Traced cases up to $500K on ETH, BTC, Tron, Arbitrum, BSC"
]
```

### `projects` 的填寫原則

- 記錄所有有意義的 side projects，即使未完成
- 每個 project 填：名稱、一行描述、可量化的成果（stars、downloads、得獎等）

---

## `experience_notes.md` 規範

### 定義

`experience_notes.md` 是每段工作的**詳細原始筆記**，比 master_profile 更細、更口語。
目的是讓 AI 在產出客製化履歷時，有足夠的細節可以選取和重新措辭。

### 格式規範

每段工作必須使用以下結構（順序固定）：

```markdown
## {公司名稱} ({任職期間})

**公司背景**
- 公司規模、類型（新創/大公司）、B2B/B2C、產業
- 你進去時的狀況（成立多久、多少人等）

**你的角色**
- 正式職稱
- 在團隊中的定位（e.g. 第一個 PM、唯一的工程師）

**核心職責**
1. 職責一（可用中文口語描述）
2. 職責二
3. （更多）

**關鍵專案 / 成果**
- 專案名稱：做了什麼、結果是什麼（**必須有數字**）
- 另一個專案：...

**量化數據（原始數字）**
- 所有可量化的數字，不管大小直接列出
- e.g. 200+ cases、轉換率 10% → 30%、時間 3hr → 1hr

**幕後細節（補充）**
- 任何「履歷不會直接寫但 AI 需要知道」的背景
- e.g. 為什麼換工作、這份工作遇到的挑戰、與其他角色的關係
```

### 填寫原則

1. **這份文件是給 AI 讀的，不是給人看的**：可以很口語、可以中文
2. **越細越好**：幕後細節越多，AI 越能寫出有深度的 bullet
3. **所有數字都寫進來**：哪怕你覺得不重要，讓 AI 來決定要不要用
4. **時態用過去式描述**：即使是現職

---

## 兩份文件的分工

| | `master_profile.json` | `experience_notes.md` |
|---|---|---|
| **語言** | 英文（最終呈現用） | 中文或英文均可 |
| **詳細程度** | 精簡版（3-4 bullets/job） | 完整版（越細越好） |
| **用途** | 直接作為 resume 的 base | 供 AI 撰寫和選取素材 |
| **是否隨 JD 改變** | 不變（由 master 分支出 resume_*.json） | 不變（永遠是原始筆記） |
