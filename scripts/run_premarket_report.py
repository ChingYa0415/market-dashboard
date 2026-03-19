import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
GENERATE_SCRIPT = ROOT / "scripts" / "generate_premarket_report.py"


def main():
    result = subprocess.run(
        ["python", str(GENERATE_SCRIPT)],
        capture_output=True,
        text=True,
        check=True
    )
    print(result.stdout)


if __name__ == "__main__":
    main()
