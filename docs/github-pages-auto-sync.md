# GitHub Pages 自動同步

目標：本機在晚上 9 點產生最新盤前簡報後，順手把報告檔案 commit / push 到 GitHub，讓 GitHub Pages 網站同步更新。

## 新增腳本

- `scripts/sync_github_pages.py`
  - `git add data/latest_premarket_report.json reports`
  - `git commit -m "Update premarket report"`
  - `git push`

- `scripts/run_premarket_report.py`
  - 先生成報告
  - 再同步 GitHub Pages
  - 最後送 Discord 通知

## 需要主機具備

- 可用的 `git`
- 已登入 GitHub（例如 SSH key 或 credential helper）
- 專案 remote 已設定完成

## 手動測試

```bash
cd "/Users/boyyy/Documents/New project/market-dashboard"
"/Users/boyyy/Documents/New project/market-dashboard/.venv/bin/python" scripts/run_premarket_report.py
```

## 預期結果

1. 報告產出成功
2. GitHub repo 出現新 commit
3. GitHub Pages 更新
4. Discord 收到完成通知

## 注意

若 `git push` 需要互動登入，cron 可能失敗；這種情況建議先改用 SSH key。
