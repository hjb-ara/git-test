# 設計書: 動作確認サンプルアプリ

## 1. 概要
本設計書は、[`docs/specs/spec.md`](docs/specs/spec.md) に記載された「動作確認サンプルアプリ」の仕様を実現するためのアーキテクチャおよび詳細設計を定義するものです。

---

## 2. アーキテクチャ・ディレクトリ構成
[`docs/rules/rule.md`](docs/rules/rule.md) および [`AGENTS.md`](AGENTS.md) の規定に基づき、以下の構成を採用します。

```
git-test/
├── src/
│   ├── main.py                  # アプリケーションのエントリポイント
│   ├── ui/
│   │   ├── app_window.ui        # PySide6-Designerで作成されたUI定義ファイル
│   │   └── app_window.py        # （必要に応じて）UIロジックやラッパー
│   └── assets/                  # アセットファイル格納用ディレクトリ
└── tests/                       # テストコード配置ディレクトリ
```

- **インポート規則**: エントリポイントを起点とし、`src.` プレフィックスを含めないこと（例: `import main` や `from ui.app_window import ...`）。
- **UIファイル**: `src/ui/` に配置し、`Path(__file__).parent` の相対パスで読み込むこと。

---

## 3. モジュール設計

### 3.1. バージョン取得モジュール (`src/utils/version.py` または `src/main.py` 内)
[`docs/specs/sample/get_app_version.py`](docs/specs/sample/get_app_version.py) のロジックを流用し、Gitタグまたは環境変数 (`APP_VERSION`) からバージョン情報を取得します。

- **関数**: [`get_app_version() -> str`](docs/specs/sample/get_app_version.py:5)
- **グローバル変数**: [`APP_VERSION`](docs/specs/sample/get_app_version.py:23)

### 3.2. メインウィンドウ設計 (`src/main.py`)
[`docs/specs/sample/use_app_version.py`](docs/specs/sample/use_app_version.py) をベースに、仕様書およびUIコンポーネント規約を満たすよう実装します。

- **クラス名**: `MainWindow` (継承: `QMainWindow`)
- **ウィジェット構成**:
  - ウィンドウタイトル: `動作確認サンプルアプリ - {APP_VERSION}`
  - ボタン: [`QPushButton`](docs/rules/ui_components.md:22)
    - `objectName`: `btn_exit`
    - 表示テキスト: 「終了」または「アプリ終了」
    - スロット関数: [`@Slot()`](docs/rules/rule.md:18) デコレータを付与した `on_btn_exit_clicked()`。クリック時にアプリケーションを終了 (`QApplication.quit()`) する。
- **UIファイルの読み込み**: [`QUiLoader`](https://doc.qt.io/qtforpython-6/PySide6/QtUiTools/QUiLoader.html) または `QtUiTools` を用いて、`src/ui/app_window.ui` をロードする。

---

## 4. コーディング規約・例外処理
- **型アノテーション**: 全ての変数および関数定義に型ヒントを付与する。
- **スロット関数**: シグナルと接続する関数には必ず [`@Slot()`](docs/rules/rule.md:18) デコレータを使用する。
- **例外処理**: ファイル読み込みや外部コマンド（Git）実行時に発生しうる例外を適切に捕捉し、ログ出力またはフォールバック値（例: `"v0.0.0-dev"`）を利用する。予期せぬクリティカルエラーが発生した場合は `QMessageBox` を用いてユーザーに通知する。

---

## 5. Coder向け実装ステップ (TODO)

1. **ディレクトリおよびファイルの確認・配置**:
   - `src/ui/app_window.ui` が存在することを確認する（ない場合は作成する）。
2. **バージョン取得ロジックの実装**:
   - `src/main.py` 内、または独立したモジュールに `get_app_version()` を実装する。
3. **メインウィンドウ・UI連携の実装**:
   - `src/ui/app_window.ui` を動的にロードする `MainWindow` クラスを `src/main.py` に記述する。
   - `btn_exit` ボタンのクリックシグナルと終了処理スロットを接続する。
   - ウィンドウタイトルにバージョン情報を動的に反映させる。
4. **エントリポイントの整備**:
   - [`src/main.py`](docs/rules/rule.md:5) の `if __name__ == "__main__":` ブロックからアプリケーションを起動できるようにする。
