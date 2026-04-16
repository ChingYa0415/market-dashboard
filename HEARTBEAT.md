## Heartbeat Purpose

這個 heartbeat 的目標是做低風險、可驗證的盤前簡報巡檢與 Discord 發送前置確認，不做自動交易。

## Allowed Heartbeat Work

- 檢查 `data/latest_premarket_report.json` 是否存在、格式是否合理、時間是否過舊。
- 檢查 `reports/latest_premarket_report.md` 是否存在，且與最新 JSON 的生成時間大致一致。
- 檢查 `config/premarket_report.json` 的核心股票與觀察股設定是否可讀。
- 若盤前簡報缺失或明顯過舊，可執行盤前簡報相關腳本來重建報告。
- 若 Discord 發送流程的必要檔案與輸出存在，可整理出待發送狀態，但不要自行改動 Discord 憑證。
- 若資料品質過低，例如大量 `待補資料`、`今晚沒新聞`、`新聞抓取失敗`，要明確標示。

## Preferred Nightly Checks

若 heartbeat 發生在台北時區的平日晚上，優先做這些：

- 20:30-21:30：確認隔天盤前簡報是否已生成。
- 生成後：檢查 JSON 與 Markdown 是否一致。
- 若生成失敗：回報失敗點，不要反覆重試超過 1 次。

## Do Not Do

- 不要主動下單、模擬下單、修改交易決策或產生自動交易指令。
- 不要自動變更 watchlist、核心持股、策略參數，除非使用者先要求。
- 不要自動修改系統設定、憑證、API key、Discord webhook、Git remote。
- 不要因為 heartbeat 而做大型重構、換框架或新增網站前端。
- 不要把任何 token、API key、憑證寫進 repo。

## Response Policy

- 如果沒有需要處理的事情，回覆 `HEARTBEAT_OK`。
- 如果有處理事情，回覆一段簡短摘要，包含：
  - 做了什麼
  - 哪些檔案受影響
  - 是否需要使用者後續確認
- 如果遇到風險或不確定性，停止在安全邊界內並明確說明原因。

## Safe Auto-Fix Scope

heartbeat 可以自動處理的修改僅限於：

- `data/latest_premarket_report.json`
- `reports/latest_premarket_report.md`
- 盤前簡報流程直接產生的報告檔

若需要修改下列檔案，先視為較高風險並保守處理：

- `config/premarket_report.json`
- `scripts/`

## Practical Rule

heartbeat 的角色是「夜間巡檢員」，不是「夜間產品經理」或「網站站長」。

優先做：

- 檢查
- 生成
- 驗證
- 摘要

避免做：

- 自作主張的產品變更
- 大型程式修改
- 任何交易行為
