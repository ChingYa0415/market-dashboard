# 免費新聞來源接入（Finnhub）

目前盤前簡報已先接上免費版 Finnhub 骨架。

## 使用方式

1. 申請 Finnhub API key
2. 在專案根目錄建立 `.env`
3. 填入以下任一欄位：

```env
MARKET_DATA_API_KEY=你的_finnhub_key
```

或

```env
FINNHUB_API_KEY=你的_finnhub_key
```

## 目前行為

- 會抓 `config/premarket_report.json` 內股票清單近 3 天 company news
- 抓到資料就填入 `news`
- 抓不到或沒設定 key，就回退到：
  - `今晚沒新聞`
  - `待補判讀`

## 現階段限制

- 只做免費版骨架
- 尚未接盤前報價
- `marketSentiment` / `mainTheme` 仍以骨架為主，未做真正市場總覽聚合
- 新聞判讀只做簡單關鍵字傾向分類，不能當交易依據
