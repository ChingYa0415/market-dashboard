# Premarket Report 規格文件

本文件用來固定這一輪要建立的「每日美股盤前簡報」骨架，避免之後對話中斷時遺失方向。

## 目標

先建立可執行的 Python 骨架流程，用固定假資料產出盤前簡報，暫時不串接真實 API、Discord webhook 發送流程驗證、或 cron 排程。

## 第一批建立檔案

- `requirements.txt`
- `config/premarket_report.json`
- `.env.example`
- `scripts/generate_premarket_report.py`
- `scripts/send_to_discord.py`
- `scripts/run_premarket_report.py`

## config/premarket_report.json

- 時區：`Asia/Taipei`
- 排程時間：平日 `21:00`
- 跳過美股休市日：`true`
- 核心股票：`NVDA`, `AMD`
- 觀察股票：`ETN`, `GSAT`, `ZETA`, `RTX`
- 最多總股票數：`8`
- 空新聞預設文字：`今晚沒新聞`
- 開盤傾向標籤：`利多` / `中性` / `利空`

## 產出格式

腳本執行後應產出：

- `data/latest_premarket_report.json`
- `reports/latest_premarket_report.md`
- `reports/YYYY-MM-DD-premarket.json`
- `reports/YYYY-MM-DD-premarket.md`

## 當前階段不做

- 真實 API 串接
- Discord webhook 正式整合驗證
- cron 排程

## 預期測試命令

```bash
python scripts/generate_premarket_report.py
```

## 預期結果

- 終端機印出一份盤前簡報
- JSON / Markdown 最新檔與封存檔成功建立
- 目錄結構與存檔流程正常
