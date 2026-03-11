# experience_notes.example.md
#
# 這是 experience_notes.md 的完整範例。
# 這份文件是給 AI 讀的原始素材，不是給人看的正式文件。
# 可以很口語、可以中文、越細越好。
#
# 使用方式：
#   cp data/experience_notes.example.md data/experience_notes.md
#   然後替換成你自己的真實內容。

---

## Stripe (2023/01 – Present)

**公司背景**
- 全球頂級 Fintech 公司，約 8,000 人，B2B 為主
- 我進去時公司正在大規模擴展歐洲市場
- Series H，估值 ~$50B

**你的角色**
- 正式職稱：Software Engineer（L4）
- 在 Payments Core 團隊，負責支付微服務的核心邏輯
- 唯一同時負責 Go backend 和 React dashboard 的工程師

**核心職責**
1. 維護處理 50K+ req/sec 的支付微服務（Go）
2. 領導 monolithic billing 系統遷移到 event-driven（Kafka + gRPC）
3. 建立給內部 200+ 工程師用的即時交易監控 dashboard
4. mentor 3 位 junior engineers（onboarding + code review）

**關鍵專案 / 成果**
- Kafka 遷移：把 billing service 從 monolith 切成 event-driven，P99 latency 降了 40%，各 team 可以獨立 deploy
- 監控 Dashboard：React + TypeScript + WebSocket，上線後被全公司 200+ engineers 用於 incident response
- 招募：參與面試流程，協助錄取 5 位 SWE，幫 team 從 8 人擴到 13 人

**量化數據（原始數字）**
- 50K+ requests/sec
- 99.99% uptime SLA
- P99 latency reduced by 40%
- Dashboard 被 200+ engineers 採用
- 3 junior engineers mentored
- 5 interviews conducted, 擴編 13 人

**幕後細節（補充）**
- 這份工作是從 DataNova（startup）跳來的，當初是因為想做更大規模的系統
- Kafka 那個專案其實推了半年才被 approve，中間遇到很多內部阻力，主要是 migration risk 的顧慮
- Dashboard 一開始只是我自己做的小工具，後來被 team lead 看到，變成正式專案
- 還在這份工作，目前在評估是否跳去其他公司

---

## Shopify (2022/05 – 2022/08)

**公司背景**
- 大型電商 SaaS 平台，約 12,000 人（當時），B2B
- 實習期 3 個月，在 Checkout Optimization 團隊

**你的角色**
- Software Engineer Intern
- 同時有 backend（GraphQL API）和 frontend（A/B test feature）的工作

**核心職責**
1. 開發 merchant analytics 的 GraphQL API 層
2. 實作 Redis caching 策略
3. 跟 checkout team 一起做 A/B test feature

**關鍵專案 / 成果**
- GraphQL API：比舊的 REST 快 3 倍，主要是透過 resolver pattern 優化
- Redis caching：把 peak-hour database load 降了 35%，dashboard 從 2.4s 到 0.8s
- A/B test feature：merchant conversion rate 提高了 2.1%，影響超過 $50M GMV

**量化數據（原始數字）**
- GraphQL 3x performance over REST
- Redis 降 35% database load
- Dashboard load time: 2.4s → 0.8s
- Conversion rate +2.1%
- GMV impact: $50M+

**幕後細節（補充）**
- 這是我第一個大公司實習，之前只在小公司工作過
- A/B test 那個功能其實是自己提的 idea，然後被 team lead 採納
- 實習結束後有收到 return offer，但因為還在讀 Master's 所以沒接

---

## DataNova (2021/01 – 2022/04)

**公司背景**
- 早期 SaaS startup，約 25 人，B2B，主打 analytics dashboard 給中小企業
- 我進去時公司成立 1.5 年，Series A 剛完成
- 後來 B 輪沒拿到，公司縮編

**你的角色**
- 正式職稱：Full-Stack Developer
- 幾乎是 team 裡唯一全端工程師（另外有 1 個 backend-only）
- 負責從零開始建整個客戶端 dashboard

**核心職責**
1. 建立 customer-facing SaaS analytics dashboard（Next.js + PostgreSQL）
2. 設計並維護所有 RESTful API（Node.js/Express）
3. 建立 CI/CD pipeline（GitHub Actions + Docker）
4. 跨功能協作：weekly sprint，與 PM 和 designer 緊密合作

**關鍵專案 / 成果**
- Dashboard：從零開始 8 個月長到 5K+ MAU
- CI/CD：deploy 時間從 45 分鐘縮到 8 分鐘，實現 zero-downtime deploy
- API：10K+ 日請求量，P95 < 200ms

**量化數據（原始數字）**
- 5K+ monthly active users（8 個月內達到）
- 10K+ daily API calls
- P95 response time < 200ms
- CI/CD: 45 min → 8 min
- 15+ features shipped in 12 months
- 95%+ test coverage maintained

**幕後細節（補充）**
- 這份工作讓我從「只寫前端」變成真正的全端工程師
- 後來公司 B 輪沒成，開始縮編，我在縮編前主動離職去找更穩的公司
- 其實在這裡學到最多的是 infrastructure 和 DevOps，不是程式本身
- 跟 PM 和 designer 的合作方式是每週 sprint review + planning，我學到如何跟非工程師溝通
