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
FINNHUB_QUOTE_URL = "https://finnhub.io/api/v1/quote"
FRED_BASE_URL = "https://api.stlouisfed.org/fred/series/observations"
FRED_SERIES = {
    "vix": "VIXCLS",
    "dgs10": "DGS10",
    "dgs2": "DGS2",
}


def load_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def now_taipei():
    return datetime.now(ZoneInfo("Asia/Taipei"))


def now_utc_date():
    return datetime.now(ZoneInfo("UTC")).date()


def load_api_keys():
    load_dotenv()
    return {
        "finnhub": os.getenv("MARKET_DATA_API_KEY") or os.getenv("FINNHUB_API_KEY", ""),
        "fred": os.getenv("FRED_API_KEY", ""),
    }


class FinnhubClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.rate_limited = False

    def _request(self, url, params):
        if not self.api_key:
            return None, "missing_key"
        if self.rate_limited:
            return None, "rate_limited"

        try:
            response = requests.get(url, params={**params, "token": self.api_key}, timeout=20)
        except Exception:
            return None, "request_failed"

        if response.status_code == 429:
            self.rate_limited = True
            return None, "rate_limited"

        try:
            payload = response.json()
        except ValueError:
            payload = None

        error_text = ""
        if isinstance(payload, dict):
            error_text = str(payload.get("error") or payload.get("message") or "").lower()

        if "limit" in error_text or "quota" in error_text or "rate" in error_text:
            self.rate_limited = True
            return None, "rate_limited"

        if response.status_code >= 400:
            return None, "request_failed"

        return payload, "ok"

    def fetch_company_news(self, symbol, empty_news_text):
        if not self.api_key:
            return {
                "headline": empty_news_text,
                "source": "fallback",
                "summary": "未設定 Finnhub API key，使用骨架內容。",
                "url": "",
            }
        if self.rate_limited:
            return {
                "headline": empty_news_text,
                "source": "fallback",
                "summary": "Finnhub 免費額度已用完，等待額度恢復後再更新新聞。",
                "url": "",
            }

        today = now_utc_date()
        date_from = (today - timedelta(days=3)).isoformat()
        date_to = today.isoformat()
        items, status = self._request(
            FINNHUB_BASE_URL,
            {
                "symbol": symbol,
                "from": date_from,
                "to": date_to,
            },
        )

        if status == "rate_limited":
            return {
                "headline": empty_news_text,
                "source": "fallback",
                "summary": "Finnhub 免費額度已用完，等待額度恢復後再更新新聞。",
                "url": "",
            }
        if status != "ok":
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

    def fetch_quote(self, symbol):
        if not self.api_key:
            return "未設定 Finnhub API key"
        if self.rate_limited:
            return "Finnhub 免費額度已用完，等待恢復"

        payload, status = self._request(FINNHUB_QUOTE_URL, {"symbol": symbol})
        if status == "rate_limited":
            return "Finnhub 免費額度已用完，等待恢復"
        if status != "ok" or not isinstance(payload, dict):
            return "資料暫時不可用"

        current = payload.get("c")
        previous_close = payload.get("pc")
        if not current or not previous_close:
            return "資料暫時不可用"

        change_pct = ((current - previous_close) / previous_close) * 100 if previous_close else 0
        return f"最新 {current:.2f} / 前收 {previous_close:.2f} / {change_pct:+.2f}%"


def fetch_fred_latest(series_id, api_key):
    if not api_key:
        return None

    try:
        response = requests.get(
            FRED_BASE_URL,
            params={
                "series_id": series_id,
                "api_key": api_key,
                "file_type": "json",
                "sort_order": "desc",
                "limit": 10,
            },
            timeout=20,
        )
        response.raise_for_status()
        payload = response.json()
    except Exception:
        return None

    for item in payload.get("observations", []):
        value = item.get("value")
        if value in {None, ".", ""}:
            continue
        try:
            return float(value)
        except ValueError:
            continue
    return None


def build_overview(fred_api_key, focus):
    if not fred_api_key:
        return {
            "marketSentiment": "待補資料（未設定 FRED_API_KEY）",
            "mainTheme": "以個股新聞骨架彙整，待補更完整市場主線判讀",
            "riskEvent": "未設定 FRED_API_KEY，宏觀風險欄位維持骨架",
            "focus": focus,
        }

    vix = fetch_fred_latest(FRED_SERIES["vix"], fred_api_key)
    dgs10 = fetch_fred_latest(FRED_SERIES["dgs10"], fred_api_key)
    dgs2 = fetch_fred_latest(FRED_SERIES["dgs2"], fred_api_key)

    if vix is None and dgs10 is None and dgs2 is None:
        return {
            "marketSentiment": "待補資料（FRED 暫時不可用）",
            "mainTheme": "以個股新聞骨架彙整，待補更完整市場主線判讀",
            "riskEvent": "FRED 資料拉取失敗，宏觀風險欄位維持骨架",
            "focus": focus,
        }

    if vix is None:
        market_sentiment = "市場情緒待補（VIX 暫時不可用）"
    elif vix >= 25:
        market_sentiment = f"風險偏好偏弱（VIX {vix:.2f}）"
    elif vix >= 18:
        market_sentiment = f"市場情緒中性偏保守（VIX {vix:.2f}）"
    else:
        market_sentiment = f"市場情緒偏穩定（VIX {vix:.2f}）"

    curve_text = ""
    if dgs10 is not None and dgs2 is not None:
        spread = dgs10 - dgs2
        curve_text = f"10Y {dgs10:.2f}% / 2Y {dgs2:.2f}% / 利差 {spread:+.2f}%"
        if spread < 0:
            main_theme = "利率曲線偏倒掛，市場仍在交易成長放緩與降息預期"
        elif spread < 0.5:
            main_theme = "利率曲線偏平，市場主線仍以個股消息與宏觀數據混合驅動"
        else:
            main_theme = "利率曲線較正常，宏觀壓力相對緩和，個股消息面主導"
    else:
        main_theme = "以個股新聞骨架彙整，宏觀利率資料仍不完整"

    risk_parts = []
    if vix is not None:
        risk_parts.append(f"VIX {vix:.2f}")
    if curve_text:
        risk_parts.append(curve_text)
    risk_event = " / ".join(risk_parts) if risk_parts else "宏觀風險資料暫時不足"

    return {
        "marketSentiment": market_sentiment,
        "mainTheme": main_theme,
        "riskEvent": risk_event,
        "focus": focus,
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


def build_symbol_entry(symbol, empty_news_text, finnhub_client):
    news = finnhub_client.fetch_company_news(symbol, empty_news_text)
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
        "premarket": finnhub_client.fetch_quote(symbol),
        "openingBias": infer_bias_from_news(news.get("headline", ""), news.get("summary", "")),
        "observation": build_observation(symbol, news.get("source", "fallback")),
    }


def build_report(config):
    empty_news_text = config["report"]["empty_news_text"]
    core_symbols = config["symbols"]["core"]
    watch_symbols = config["symbols"]["watch"]
    api_keys = load_api_keys()
    finnhub_client = FinnhubClient(api_keys["finnhub"])

    core_entries = [build_symbol_entry(symbol, empty_news_text, finnhub_client) for symbol in core_symbols]
    watch_entries = [build_symbol_entry(symbol, empty_news_text, finnhub_client) for symbol in watch_symbols]
    focus = (core_symbols + watch_symbols)[:3]

    return {
        "generatedAt": now_taipei().isoformat(),
        "overview": build_overview(api_keys["fred"], focus),
        "core": core_entries,
        "watch": watch_entries,
        "actionSummary": {
            "mostImportant": focus,
            "coreView": "目前僅使用免費的 Finnhub 與 FRED 來源，關鍵決策仍需人工複核。",
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
