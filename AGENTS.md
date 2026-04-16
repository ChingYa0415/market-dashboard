# Premarket Discord Workspace

這個 workspace 的主要目的只有一個：生成美股盤前簡報並發送到 Discord。

## 工作範圍

- 優先維護盤前簡報生成流程、報告輸出與 Discord 發送邏輯。
- 不再維護網站前端、GitHub Pages 或靜態首頁。
- 預設不要觸碰其他資料夾、系統設定或使用者私人檔案。

## 修改原則

- 先做小步、可驗證的改動。
- 優先保持資料流程清楚、輸出穩定、錯誤可追蹤。
- 若要引入新的資料來源、排程、推送管道或憑證機制，先說明風險再動手。
- 不要把任何 token、API key、憑證寫進 repo。

## 主要檔案

- `config/premarket_report.json`: 簡報輸入設定
- `scripts/generate_premarket_report.py`: 生成最新 JSON / Markdown 報告
- `scripts/run_generate_premarket_report.sh`: nightly cron 使用的固定入口
- `scripts/run_premarket_report.py`: 手動生成並發送 Discord 的入口
- `scripts/send_to_discord.py`: Discord webhook 發送工具
- `data/latest_premarket_report.json`: 最新結構化報告
- `reports/latest_premarket_report.md`: 最新 Markdown 簡報

## 互動習慣

- 如果使用者從 Discord 下指令，預設理解成要維護盤前簡報與 Discord 發送流程。
- 如果需求明確屬於報告生成、內容修正、排程、Discord 訊息輸出，預設直接動手。
- 完成後回報改了哪些檔案、做了什麼改動，以及如何驗證。
- 若需求超出簡報 / Discord 範圍，先停下來提醒。
