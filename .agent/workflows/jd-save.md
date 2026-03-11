---
description: 貼入 JD 後自動存檔到 jobs/{Company}/{Role}/ 資料夾
---

# JD 存檔 Workflow

當使用者貼入一份 Job Description 並觸發此 workflow 時，執行以下步驟：

## 步驟

### 1. 從 JD 中提取公司名稱與職位名稱

- **Company**：公司名稱，使用英文，例如 `Google`, `Binance`, `MEXC`
- **Role**：職位簡稱，使用英文短橫線命名，例如 `PM`, `Risk-Analyst`, `User-Ops`

### 2. 建立資料夾結構

```
jobs/{Company}/{Role}/JD.md
```

- 如果 `jobs/{Company}/` 已存在，直接建立新的 `{Role}/` 子資料夾
- 如果公司和職位都已存在，詢問使用者是否要覆蓋

### 3. 寫入 JD.md

將使用者貼入的 JD **原文完整保留**寫入 `JD.md`，不做任何刪減或重新排版。

在檔案最上方加入 metadata header：

```markdown
---
company: {Company}
role: {Role（完整職位名稱）}
source: {來源平台，如 LinkedIn / Careers Page / 其他，若無法判斷則寫 Unknown}
saved_at: {當前日期 YYYY-MM-DD}
---

{原始 JD 全文}
```

### 4. 確認回報

存檔完成後，回報：
- 存檔路徑
- 提示使用者可以用 `/jd-match` 進行匹配分析

## 注意事項

- 全程使用**繁體中文**回答
- 公司名稱統一用英文、不加空格以外的特殊字元
- Role 名稱用英文短橫線，簡潔明瞭
