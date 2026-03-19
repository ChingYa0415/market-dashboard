import json
import subprocess
import sys
from pathlib import Path

from send_to_discord import send_message


ROOT = Path(__file__).resolve().parent.parent
GENERATE_SCRIPT = ROOT / "scripts" / "generate_premarket_report.py"
SYNC_SCRIPT = ROOT / "scripts" / "sync_github_pages.py"
LATEST_JSON = ROOT / "data" / "latest_premarket_report.json"
SITE_URL = "https://chingya0415.github.io/market-dashboard/"


def run_python_script(script_path):
    result = subprocess.run(
        [sys.executable, str(script_path)],
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout


def generate_report():
    return run_python_script(GENERATE_SCRIPT)


def sync_site():
    return run_python_script(SYNC_SCRIPT)


def load_latest_report():
    with open(LATEST_JSON, "r", encoding="utf-8") as f:
        return json.load(f)


def build_notification(report, sync_output=None):
    overview = report.get("overview", {})
    action_summary = report.get("actionSummary", {})
    focus = "、".join(overview.get("focus", [])) or "待補"
    important = "、".join(action_summary.get("mostImportant", [])) or "待補"

    lines = [
        "🦐 每日美股盤前簡報已完成",
        f"- 生成時間：{report.get('generatedAt', '未知')}",
        f"- 市場情緒：{overview.get('marketSentiment', '待補資料')}",
        f"- 主線題材：{overview.get('mainTheme', '待補資料')}",
        f"- 優先關注：{focus}",
        f"- 最值得注意：{important}",
        f"- 網站連結：{SITE_URL}",
    ]

    if sync_output:
        lines.append(f"- GitHub 同步：{sync_output.strip()}")

    return "\n".join(lines)


def main(send_discord=True, sync_github=True):
    output = generate_report()
    print(output)

    sync_output = None
    if sync_github:
        sync_output = sync_site()
        print(sync_output)

    if send_discord:
        report = load_latest_report()
        message = build_notification(report, sync_output=sync_output)
        send_message(message)
        print("Discord notification sent.")


if __name__ == "__main__":
    main()
