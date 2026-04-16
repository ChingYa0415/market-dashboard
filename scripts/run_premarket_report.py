import json
import subprocess
import sys
from pathlib import Path
from zoneinfo import ZoneInfo

from send_to_discord import send_message

try:
    import holidays
except ImportError:  # pragma: no cover
    holidays = None


ROOT = Path(__file__).resolve().parent.parent
GENERATE_SCRIPT = ROOT / "scripts" / "generate_premarket_report.py"
LATEST_JSON = ROOT / "data" / "latest_premarket_report.json"
LATEST_MD = ROOT / "reports" / "latest_premarket_report.md"
CONFIG_PATH = ROOT / "config" / "premarket_report.json"
TAIPEI_TZ = ZoneInfo("Asia/Taipei")
NEW_YORK_TZ = ZoneInfo("America/New_York")


def load_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def run_python_script(script_path):
    result = subprocess.run(
        [sys.executable, str(script_path)],
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout


def should_skip_for_market_close(config):
    schedule = config.get("schedule", {})
    if not schedule.get("skip_market_holidays", True):
        return False, ""

    if holidays is None:
        return False, "holidays 套件未安裝，略過休市判斷"

    now_taipei = datetime.now(TAIPEI_TZ)
    now_ny = now_taipei.astimezone(NEW_YORK_TZ)
    ny_date = now_ny.date()

    try:
        nyse_holidays = holidays.financial_holidays("NYSE")
    except Exception:
        return False, "NYSE holiday calendar 無法載入，略過休市判斷"

    if ny_date in nyse_holidays:
        holiday_name = nyse_holidays.get(ny_date, "NYSE holiday")
        return True, f"skip: {ny_date.isoformat()} 美股休市（{holiday_name}）"

    return False, ""


def generate_report():
    return run_python_script(GENERATE_SCRIPT)


def load_latest_report():
    with open(LATEST_JSON, "r", encoding="utf-8") as f:
        return json.load(f)


def load_latest_markdown():
    return LATEST_MD.read_text(encoding="utf-8").strip()


def build_notification(report, markdown_report):
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
        "",
        markdown_report,
    ]

    return "\n".join(lines)


def main(send_discord=True):
    config = load_config()
    should_skip, reason = should_skip_for_market_close(config)
    if should_skip:
        print(reason)
        return
    if reason:
        print(reason)

    output = generate_report()
    print(output)

    if send_discord:
        report = load_latest_report()
        markdown_report = load_latest_markdown()
        message = build_notification(report, markdown_report)
        send_message(message)
        print("Discord notification sent.")


if __name__ == "__main__":
    main()
