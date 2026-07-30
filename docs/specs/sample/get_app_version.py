import os
import subprocess


def get_app_version() -> str:
    # 1. CI/CD等で環境変数がセットされている場合はそれを優先
    version = os.getenv("APP_VERSION")
    if version:
        return version

    # 2. ローカル開発時: Gitコマンドから最新タグを取得
    try:
        version = subprocess.check_output(
            ["git", "describe", "--tags", "--always"], stderr=subprocess.DEVNULL, text=True
        ).strip()
        return version
    except Exception:
        # 3. Git未設定・タグが存在しない場合のデフォルト値
        return "v0.0.0-dev"


# グローバル変数として保持
APP_VERSION = get_app_version()
