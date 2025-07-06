Redmine → Excel 自動更新システム設計書（統合版）

バージョン: v0.1.0  |  環境: Linux / Python 3.11  |  主要ライブラリ: Flask 2.x, Gunicorn 21.x, python-redmine 2.x, openpyxl 3.1.x, pandas 2.x, pydantic 2.x

⸻

1. 目的・背景

現状課題	解決方針
Redmine チケットを手作業で Excel 転記 → ミス・工数増大	Redmine API から自動取得し Python で貼付け
既存 Excel の書式が壊れておりテンプレート流用不可	行コピー＋セル置換方式で書式を維持

ゴール
	1.	Web UI で既存 Excel をアップロードすると、最新チケット情報に基づく Excel を自動生成してダウンロードできる。
	2.	タイトル一致行は Redmine 情報で上書き。新規チケットは行追加。
	3.	期日 (CF#2) の残日数で行書式を自動切替。
	4.	4 箇所 (タイトル + CF1/2/3) を置換。CF3 の改行は Excel 内改行へ反映。

⸻

2. 全体アーキテクチャ

graph LR
A[Web UI<br>(Upload / Download)] -->|Excel 読込| B(Parser)
B -->|既存タイトル一覧| C(Merger)
C --> D(Sorter)
D -->|書式判定| E(ExcelService)
E -->|openpyxl save| F(Output.xlsx)
C <--|REST| G[RedmineService]
A -->|HTTP POST| H[Flask API]

レイヤ責務

レイヤ	主な責務	主要ライブラリ
Web UI	アップ/ダウンロード・進捗表示	Flask + Jinja2 (PoC: Streamlit)
Flask API	HTTP 入口, ファイル I/O, Service 呼び出し	Flask Blueprint
ReportService	既存行コピー・マージ・並べ替え	pandas
ExcelService	行コピー・書式選択・セル置換	openpyxl
RedmineService	チケット取得, DTO 化	python-redmine


⸻

3. ディレクトリ構成

app/
 ├─ api/
 │   └─ reports.py         # /reports エンドポイント
 ├─ services/
 │   ├─ redmine_service.py  # Redmine API ラッパ
 │   ├─ excel_service.py    # 行コピー & 書式処理
 │   └─ report_service.py   # 業務ロジック統括
 ├─ templates/             # normal.xlsx / gray.xlsx
 ├─ configs/
 │   └─ settings.yaml       # URL・API キー等
 ├─ wsgi.py                # app = create_app()
 └─ tests/


⸻

4. 詳細クラス設計（関数レベル）

4.1 TicketDTO

@dataclass(frozen=True)
class TicketDTO:
    title: str
    cf1: str | None
    cf2: str | None  # ISO 日付文字列
    cf3: str | None  # 改行含む


⸻

4.2 RedmineService

関数	シグネチャ	処理概要
__init__	(base_url: str, api_key: str)	python-redmine クライアント生成
fetch_tickets	(project_id: int, **filters) -> list[TicketDTO]	issue.filter()で取得 → DTO リストへ変換 (500系はリトライ)
_cf (private)	(issue, cf_id)	指定カスタムフィールド値を抽出


⸻

4.3 ExcelService

関数	シグネチャ	主処理
__init__	(tmpl_normal: Path, tmpl_gray: Path)	テンプレ xlsx パス保持
parse_uploaded	(Path) -> list[str]	“Data” シート A列からタイトル配列取得
within_19 (static)	(due_iso) -> bool	期日との差分で書式判定
copy_row (private)	(src_ws, dst_ws, src_idx, dst_idx)	値・書式・結合セル・行高を丸コピー
build_workbook	(tickets, src_wb, src_map) -> Workbook	既存行コピー / 新規行テンプレ使用 → 4セル置換 → wb 返却
_clone_template	(ticket) -> Workbook	残日数でテンプレ選択し複製


⸻

4.4 ReportService

関数	シグネチャ	主処理
__init__	(redmine, excel)	DI で依存注入
generate	(uploaded, project_id, filters, out_path) -> Path	①既存タイトル抽出 → ②Redmine 取得 → ③DataFrame マージ→ ④ExcelService で wb 構築→ ⑤保存
_merge_frames	(df_up, df_rm)	タイトルキーでマージ & ソート
_flag_existing	(df)	既存行 bool フラグ付与


⸻

5. API 設計

エンドポイント	メソッド	入力	出力
/reports	POST	multipart/form-data (file=xlsx)	更新済み Excel (application/vnd.openxmlformats-officedocument.spreadsheetml.sheet)

エラー : ServiceError→400, 予期せぬ例外→500。

⸻

6. インフラ / デプロイ

gunicorn
	•	コマンド: gunicorn -c gunicorn.conf.py wsgi:app
	•	gunicorn.conf.py

bind = "0.0.0.0:8000"
workers = 4
threads = 2
timeout = 30
loglevel = "info"
accesslog = "-"



systemd Unit

[Unit]
Description=Redmine → Excel Updater
After=network.target

[Service]
User=www-data
WorkingDirectory=/srv/redmine-report
ExecStart=/usr/bin/gunicorn -c gunicorn.conf.py wsgi:app
Restart=always
Environment=PYTHONUNBUFFERED=1

Nginx (抜粋)

location / {
  proxy_pass http://127.0.0.1:8000;
  proxy_set_header Host $host;
  proxy_set_header X-Real-IP $remote_addr;
}


⸻

7. テスト戦略

テストモジュール	観点	ツール
unit/test_redmine_service.py	DTO 化・リトライ	pytest + respx
unit/test_excel_service.py	行コピー後の値/書式	pytest + openpyxl
integration/test_report_service.py	generate 一括フロー	pandas.testing
api/test_reports.py	200 OK & 添付検証	Flask test_client

CI: GitHub Actions matrix (Python 3.9–3.12, ubuntu-latest)。

⸻

8. 性能指標

指標	目標
処理時間 (100 行)	≤ 5 秒 (2 vCPU)
同時リクエスト	10
メモリ	≤ 250 MB / worker


⸻

9. TODO / 依存
	•	normal.xlsx / gray.xlsx のセル番地確定
	•	Redmine カスタムフィールド ID を settings.yaml へ反映
	•	i18n (Flask-Babel) 検討
	•	5,000 行超ブックでの負荷試験

⸻

本ドキュメントは高レベル設計および関数レベル詳細設計を統合したものです。追加要件・命名規約変更などがあればお知らせください。