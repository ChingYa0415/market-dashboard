# Premarket Discord Bot Workspace

這個專案現在只負責兩件事：

1. 生成每日美股盤前簡報
2. 將簡報內容發送到 Discord

不再維護任何網站前端或 GitHub Pages 站點。

## 核心流程

- `scripts/generate_premarket_report.py`
  讀取設定、抓資料、生成最新 JSON / Markdown 報告。
- `scripts/run_generate_premarket_report.sh`
  nightly cron 的固定入口。
- `scripts/run_premarket_report.py`
  手動生成簡報並透過 webhook 發送 Discord。
- `scripts/send_to_discord.py`
  單純的 Discord webhook 發送工具。

## 主要輸出

- `data/latest_premarket_report.json`
- `reports/latest_premarket_report.md`

## 手動測試

生成最新報告：

```bash
./scripts/run_generate_premarket_report.sh
```

手動生成並發送到 Discord：

```bash
.venv/bin/python scripts/run_premarket_report.py
```
