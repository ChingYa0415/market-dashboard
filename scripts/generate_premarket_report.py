import json
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo


ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = ROOT / "config" / "premarket_report.json"


def load_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def now_taipei():
    return datetime.now(ZoneInfo("Asia/Taipei"))


def build_overview():
    return {
        "marketSentiment": "待補資料",
        "mainTheme": "待補資料",
        "riskEvent": "待補資料",
        "focus": ["NVDA", "AMD", "ETN"]
    }


def build_symbol_entry(symbol, empty_news_text):
    return {
        "symbol": symbol,
        "news": empty_news_text,
        "judgement": "待補判讀",
        "premarket": "資料不足",
        "openingBias": "中性",
        "observation": "待補觀察"
    }


def build_report(config):
    empty_news_text = config["report"]["empty_news_text"]
    core_symbols = config["symbols"]["core"]
    watch_symbols = config["symbols"]["watch"]

    return {
        "generatedAt": now_taipei().isoformat(),
        "overview": build_overview(),
        "core": [build_symbol_entry(symbol, empty_news_text) for symbol in core_symbols],
        "watch": [build_symbol_entry(symbol, empty_news_text) for symbol in watch_symbols],
        "actionSummary": {
            "mostImportant": ["NVDA", "AMD", "ETN"],
            "coreView": "待補核心持股看法",
            "highestVolatility": ["GSAT", "ZETA"],
            "ifMarketWeakens": ["GSAT"]
        }
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
