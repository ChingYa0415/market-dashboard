import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


def run(command):
    result = subprocess.run(
        command,
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.strip()


def has_changes():
    result = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    return bool(result.stdout.strip())


def main():
    if not has_changes():
        print("No changes to sync.")
        return

    run(["git", "add", "data/latest_premarket_report.json", "reports"])
    run(["git", "commit", "-m", "Update premarket report"])
    run(["git", "push"])
    print("GitHub Pages sync complete.")


if __name__ == "__main__":
    main()
