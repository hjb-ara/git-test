# 🎨 UI Components & Widget Naming Conventions

本ドキュメントは、本プロジェクトにおける UI/ウィジェットの設計方針および `objectName` の命名規則を定義します。  
AIエージェントおよび開発者は、Qt Designerでの画面作成およびPySide6でのコード実装時に必ず本規約に従ってください。

---

## 1. 基本命名ルール (Naming Rules)

1. **フォーマット**: `[略称]_[役割・機能名]`
2. **文字修飾**: すべて **スネークケース (snake_case)** の小文字＋アンダースコアで記述する。
3. **英語表記**: 役割・機能名は明確で意味の通る英語（または略称）を使用する。
4. **デフォルト名の禁止**: ロジックコード（Python側）から参照・操作するウィジェットにおいて、Qt Designerのデフォルト名（例: `pushButton_1`, `label_2`）を放置することを厳禁とする。

---

## 2. ウィジェット別 略称プレフィックス一覧 (Prefix Reference)

### 入力系 (Input Widgets)
| ウィジェットクラス | 略称 (Prefix) | 命名例 (Example) | 説明 |
| :--- | :--- | :--- | :--- |
| **QPushButton** | `btn_` | `btn_submit`, `btn_cancel`, `btn_add` | 各種操作ボタン |
| **QLineEdit** | `txt_` | `txt_user_name`, `txt_search` | 1行テキスト入力 |
| **QTextEdit / QPlainTextEdit** | `txt_` | `txt_memo`, `txt_log` | 複数行テキスト入力 |
| **QComboBox** | `cmb_` | `cmb_category`, `cmb_gender` | ドロップダウンリスト |
| **QCheckBox** | `chk_` | `chk_agree`, `chk_auto_login` | チェックボックス |
| **QRadioButton** | `rdo_` | `rdo_male`, `rdo_female` | ラジオボタン |
| **QSpinBox / QDoubleSpinBox** | `spn_` | `spn_age`, `spn_count` | 数値入力スピンボックス |

### 表示・出力系 (Display Widgets)
| ウィジェットクラス | 略称 (Prefix) | 命名例 (Example) | 説明 |
| :--- | :--- | :--- | :--- |
| **QLabel** | `lbl_` | `lbl_title`, `lbl_status` | 動的にテキスト変更するラベル |
| **QProgressBar** | `prg_` | `prg_download_status` | 進捗バー |

### リスト・ビュー系 (Item Views / Widgets)
| ウィジェットクラス | 略称 (Prefix) | 命名例 (Example) | 説明 |
| :--- | :--- | :--- | :--- |
| **QListWidget / QListView** | `lst_` | `lst_items`, `lst_file_history` | リスト表示 |
| **QTableWidget / QTableView** | `tbl_` | `tbl_users`, `tbl_orders` | テーブル・表表示 |
| **QTreeWidget / QTreeView** | `tre_` | `tre_directory` | ツリー構造表示 |

### コンテナ・ウィンドウ系 (Containers & Windows)
| ウィジェットクラス | 略称 (Prefix) | 命名例 (Example) | 説明 |
| :--- | :--- | :--- | :--- |
| **QGroupBox** | `grp_` | `grp_user_info` | グループボックス枠 |
| **QTabWidget** | `tab_` | `tab_main` | タブコンテナ |
| **QDialog** | `dlg_` | `dlg_maintenance` | ダイアログウィンドウ |

---

## 3. 特例および例外ルール (Exceptions)

* **静的ラベル (Static Labels)**  
  「ユーザー名：」などの固定表示テキストであり、Pythonコード側から文字列の変更や状態参照を**一切行わない `QLabel`** に限っては、デフォルト名（`label_1` 等）のままにして構わない。
* **レイアウトオブジェクト (Layouts)**  
  `QVBoxLayout` や `QHBoxLayout` などのレイアウト自体をコードから動的に操作しない場合は、リネーム不要とする。

---

## 4. コードからの参照例 (PySide6 Code Example)

```python
# 〇 良い例（補完が効き、役割が一目でわかる）
self.ui.btn_add.clicked.connect(self.add_item)
user_input = self.ui.txt_user_name.text()
self.ui.lst_items.addItem(user_input)

# ✕ 悪い例（どのパーツか判別不能・バグの原因）
self.ui.pushButton_1.clicked.connect(self.add_item)
user_input = self.ui.lineEdit_2.text()
self.ui.listWidget.addItem(user_input)
```
