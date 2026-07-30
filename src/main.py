import os
import subprocess
import sys
from pathlib import Path

from PySide6.QtCore import Slot
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox


def get_app_version() -> str:
    """Gitタグまたは環境変数からアプリケーションのバージョンを取得する。

    Returns:
        str: バージョン文字列
    """
    version = os.getenv("APP_VERSION")
    if version:
        return version

    try:
        version = subprocess.check_output(
            ["git", "describe", "--tags", "--always"],
            stderr=subprocess.DEVNULL,
            text=True,
        ).strip()
        return version
    except Exception:
        return "v0.0.0-dev"


APP_VERSION = get_app_version()


class MainWindow(QMainWindow):
    """メインウィンドウクラス"""

    def __init__(self) -> None:
        """MainWindowを初期化し、UIをロードしてシグナルとスロットを接続する。"""
        super().__init__()
        try:
            loader = QUiLoader()
            ui_path = Path(__file__).parent / "ui" / "app_window.ui"

            # QUiLoaderでQWidget（あるいはロードされたウィンドウ）を直接生成する
            self.ui = loader.load(str(ui_path))
            if self.ui is None:
                raise RuntimeError(f"UIファイルのロードに失敗しました: {ui_path}")

            # UIファイルをQWdiget/QMainWindow形式でロードした場合のウィジェット構造に対応
            # ui_app_window.ui のルートが QMainWindow の場合、自らをリサイズ・ウィジェット設定する
            if isinstance(self.ui, QMainWindow):
                # UIファイルのgeometryやcentralWidgetを引き継ぐ
                self.resize(self.ui.size())
                if self.ui.centralWidget():
                    self.setCentralWidget(self.ui.centralWidget())
                # ボタン参照を自インスタンス配下またはロードしたuiから取得できるようにする
                self.btn_exit = self.ui.findChild(object, "btn_exit")
            else:
                self.setCentralWidget(self.ui)
                self.resize(400, 300)
                self.btn_exit = self.findChild(object, "btn_exit")

        except Exception as e:
            QMessageBox.critical(
                None,
                "エラー",
                f"UIファイルの読み込み中に予期せぬエラーが発生しました。\n{e}",
            )
            sys.exit(1)

        self.setWindowTitle(f"動作確認サンプルアプリ - {APP_VERSION}")

        # ボタンのシグナルとスロット接続
        btn = self.findChild(object, "btn_exit")
        if btn is not None:
            btn.clicked.connect(self.on_btn_exit_clicked)

    @Slot()
    def on_btn_exit_clicked(self) -> None:
        """終了ボタンがクリックされたときにアプリケーションを終了する。"""
        QApplication.quit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
