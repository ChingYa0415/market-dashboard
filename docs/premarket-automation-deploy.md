# Premarket 自動化部署說明

目標：讓每日美股盤前簡報在晚上 9 點自動生成，並在完成後送出 Discord 通知。

## 目前已具備的腳本

- `scripts/generate_premarket_report.py`
  - 產生最新 JSON / Markdown 與封存檔
- `scripts/send_to_discord.py`
  - 使用 `DISCORD_WEBHOOK_URL` 發送 Discord 訊息
- `scripts/run_premarket_report.py`
  - 串接生成流程與 Discord 通知

## 通知內容

執行完成後會送出：

- 生成時間
- 市場情緒
- 主線題材
- 優先關注
- 最值得注意標的
- 最新 Markdown 簡報正文

## 環境變數

先複製：

```bash
cp .env.example .env
```

然後填入：

- `DISCORD_WEBHOOK_URL`
- 之後若接真實資料再補 API keys

## 手動測試

```bash
cd "/Users/boyyy/Documents/New project/market-dashboard"
source .venv/bin/activate
python scripts/run_premarket_report.py
```

預期結果：

1. 產生 / 更新報告檔案
2. Discord 收到「每日美股盤前簡報已完成」通知

## 排程範例（cron）

若部署在可長時間在線的主機，可加入 crontab：

```cron
0 21 * * 1-5 cd /path/to/market-dashboard && /path/to/market-dashboard/.venv/bin/python scripts/run_premarket_report.py >> logs/premarket.log 2>&1
```

說明：

- `0 21 * * 1-5` = 每週一到週五晚上 9:00
- 建議先建立 `logs/` 目錄
- 若未來要判斷美股休市，可再補 holiday 檢查邏輯

## 目前尚未完成

- 失敗重試 / 錯誤告警
- 更細緻的 Discord 訊息分段與格式化

## 建議下一步

1. 先測通 Discord webhook
2. 再決定 nightly 排程要跑在哪台主機
3. 最後補上真實資料來源與休市日判斷
