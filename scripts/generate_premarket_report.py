import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

import requests
from dotenv import load_dotenv


ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = ROOT / "config" / "premarket_report.json"
FINNHUB_BASE_URL = "https://finnhub.io/api/v1/company-news"


def load_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def now_taipei():
    return datetime.now(ZoneInfo("Asia/Taipei"))


def now_utc_date():
    return datetime.now(ZoneInfo("UTC")).date()


def load_api_key():
    load_dotenv()
    return os.getenv("MARKET_DATA_API_KEY") or os.getenv("FINNHUB_API_KEY", "")


def build_overview():
    return {
        "marketSentiment": "待補資料",
        "mainTheme": "待補資料",
        "riskEvent": "待補資料",
        "focus": ["NVDA", "AMD", "ETN"],
    }


def fetch_company_news(symbol, api_key, empty_news_text):
    if not api_key:
        return {
            "headline": empty_news_text,
            "source": "fallback",
            "summary": "未設定 Finnhub API key，使用骨架內容。",
            "url": "",
        }

    today = now_utc_date()
    date_from = (today - timedelta(days=3)).isoformat()
    date_to = today.isoformat()

    try:
        response = requests.get(
            FINNHUB_BASE_URL,
            params={
                "symbol": symbol,
                "from": date_from,
                "to": date_to,
                "token": api_key,
            },
            timeout=20,
        )
        response.raise_for_status()
        items = response.json()
    except Exception:
        return {
            "headline": empty_news_text,
            "source": "fallback",
            "summary": "新聞抓取失敗，使用骨架內容。",
            "url": "",
        }

    if not items:
        return {
            "headline": empty_news_text,
            "source": "fallback",
            "summary": "最近沒有抓到可用新聞。",
            "url": "",
        }

    best = pick_best_news(items)
    return {
        "headline": clean_text(best.get("headline")) or empty_news_text,
        "source": clean_text(best.get("source")) or "Unknown",
        "summary": clean_text(best.get("summary"), limit=220) or "摘要不足",
        "url": best.get("url", ""),
    }


def pick_best_news(items):
    def score(item):
        headline = item.get("headline", "") or ""
        summary = item.get("summary", "") or ""
        source = item.get("source", "") or ""
        return (
            len(summary) > 30,
            source in {"Reuters", "CNBC", "Bloomberg", "MarketWatch", "Yahoo"},
            len(headline),
        )

    return sorted(items, key=score, reverse=True)[0]


def clean_text(value, limit=140):
    if not value:
        return ""
    text = " ".join(str(value).split())
    if len(text) <= limit:
        return text
    return text[: limit - 1].rstrip() + "…"


def infer_bias_from_news(headline, summary):
    text = f"{headline} {summary}".lower()
    bullish_terms = ["beat", "surge", "growth", "upgrade", "partnership", "record", "strong"]
    bearish_terms = ["miss", "drop", "lawsuit", "delay", "weak", "downgrade", "cut"]

    if any(term in text for term in bullish_terms):
        return "利多"
    if any(term in text for term in bearish_terms):
        return "利空"
    return "中性"


def build_judgement(summary):
    if summary in {"摘要不足", "最近沒有抓到可用新聞。", "新聞抓取失敗，使用骨架內容。", "未設定 Finnhub API key，使用骨架內容。"}:
        return "待補判讀"
    return f"依新聞摘要初判：{summary}"


def build_observation(symbol, source):
    if source == "fallback":
        return f"{symbol} 暫時以價格與量能為主，等待更多催化。"
    return f"留意 {symbol} 是否延續 {source} 所反映的市場敘事。"


def build_symbol_entry(symbol, empty_news_text, api_key):
    news = fetch_company_news(symbol, api_key, empty_news_text)
    news_text = news["headline"]
    if news.get("source") and news["source"] != "fallback":
        news_text = f"{news_text}（{news['source']}）"

    return {
        "symbol": symbol,
        "news": news_text,
        "newsSource": news.get("source", "fallback"),
        "newsSummary": news.get("summary", ""),
        "newsUrl": news.get("url", ""),
        "judgement": build_judgement(news.get("summary", "")),
        "premarket": "資料待接入",
        "openingBias": infer_bias_from_news(news.get("headline", ""), news.get("summary", "")),
        "observation": build_observation(symbol, news.get("source", "fallback")),
    }


def build_report(config):
    empty_news_text = config["report"]["empty_news_text"]
    core_symbols = config["symbols"]["core"]
    watch_symbols = config["symbols"]["watch"]
    api_key = load_api_key()

    core_entries = [build_symbol_entry(symbol, empty_news_text, api_key) for symbol in core_symbols]
    watch_entries = [build_symbol_entry(symbol, empty_news_text, api_key) for symbol in watch_symbols]
    focus = (core_symbols + watch_symbols)[:3]

    return {
        "generatedAt": now_taipei().isoformat(),
        "overview": {
            **build_overview(),
            "focus": focus,
            "mainTheme": "以個股新聞骨架彙整，待補更完整市場主線判讀",
            "riskEvent": "若新聞量不足，需另查財報、Fed 與宏觀事件",
        },
        "core": core_entries,
        "watch": watch_entries,
        "actionSummary": {
            "mostImportant": focus,
            "coreView": "先用免費新聞來源建立晚間快報骨架，關鍵決策仍需人工複核。",
            "highestVolatility": watch_symbols[:2],
            "ifMarketWeakens": watch_symbols[:1],
        },
    }


def render_markdown(report):
    lines = []
    lines.append(f"# 每日美股盤前簡報｜{report['generatedAt']}")
    lines.append("")
    lines.append("## 今晚總覽")
    lines.append(f"- 市場情緒：{report['overview']['marketSentiment']}")
    lines.append(f"- 主線題材：{report['overview']['mainTheme']}")
    lines.append(f"- 風險事件：{report['overview']['riskEvent']}")
    lines.append(f"- 今晚優先關注：{', '.join(report['overview']['focus'])}")
    lines.append("")
    lines.append("## 核心持股")
    lines.append("")

    for item in report["core"]:
        lines.append(f"**{item['symbol']}**")
        lines.append(f"- 新聞：{item['news']}")
        lines.append(f"- 摘要：{item.get('newsSummary', '摘要不足')}")
        lines.append(f"- 判讀：{item['judgement']}")
        lines.append(f"- 盤前：{item['premarket']}")
        lines.append(f"- 開盤前：{item['openingBias']}")
        lines.append(f"- 觀察：{item['observation']}")
        lines.append("")

    lines.append("## 觀察股")
    lines.append("")

    for item in report["watch"]:
        lines.append(f"**{item['symbol']}**")
        lines.append(f"- 新聞：{item['news']}")
        lines.append(f"- 摘要：{item.get('newsSummary', '摘要不足')}")
        lines.append(f"- 判讀：{item['judgement']}")
        lines.append(f"- 盤前：{item['premarket']}")
        lines.append(f"- 開盤前：{item['openingBias']}")
        lines.append(f"- 觀察：{item['observation']}")
        lines.append("")

    lines.append("## 行動摘要")
    lines.append(f"- 最值得注意：{', '.join(report['actionSummary']['mostImportant'])}")
    lines.append(f"- 核心持股看法：{report['actionSummary']['coreView']}")
    lines.append(f"- 波動可能較大：{', '.join(report['actionSummary']['highestVolatility'])}")
    lines.append(f"- 若市場轉弱先留意：{', '.join(report['actionSummary']['ifMarketWeakens'])}")
    lines.append("")

    return "\n".join(lines)


def save_report(config, report):
    latest_json_path = ROOT / config["output"]["latest_json"]
    latest_md_path = ROOT / config["output"]["latest_md"]
    archive_dir = ROOT / config["output"]["archive_dir"]
    archive_dir.mkdir(parents=True, exist_ok=True)
    latest_json_path.parent.mkdir(parents=True, exist_ok=True)
    latest_md_path.parent.mkdir(parents=True, exist_ok=True)

    date_str = now_taipei().strftime("%Y-%m-%d")
    archive_json_path = archive_dir / f"{date_str}-premarket.json"
    archive_md_path = archive_dir / f"{date_str}-premarket.md"

    markdown = render_markdown(report)

    with open(latest_json_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    with open(latest_md_path, "w", encoding="utf-8") as f:
        f.write(markdown)

    with open(archive_json_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    with open(archive_md_path, "w", encoding="utf-8") as f:
        f.write(markdown)

    return markdown


def main():
    config = load_config()
    report = build_report(config)
    markdown = save_report(config, report)
    print(markdown)


if __name__ == "__main__":
    main()
