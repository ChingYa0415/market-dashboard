# Market Dashboard

本機用的看盤網站骨架。先用靜態檔與 mock data 起步，之後可以逐步接上即時行情、個人策略、後端 API 或資料庫。

## 快速啟動

在專案根目錄執行：

```bash
python3 -m http.server 4173
```

然後打開：

```text
http://localhost:4173
```

## 專案結構

- `index.html`: 首頁版型
- `assets/styles.css`: 視覺樣式
- `assets/app.js`: 前端邏輯與渲染
- `data/watchlist.json`: mock 市場資料
- `AGENTS.md`: 給 OpenClaw 的專案操作規則

## 下一步可以做什麼

1. 把 `data/watchlist.json` 換成你自己的觀察清單。
2. 接上真實 API，例如股票、加密貨幣或匯率資料源。
3. 增加歷史走勢、成交量、持倉、風險控管與事件行事曆。
4. 把筆記或提醒改成寫入後端，而不是只存在瀏覽器 localStorage。
