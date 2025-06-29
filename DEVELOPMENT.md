# 開発者向けガイド

このドキュメントでは、コミット前に実行すべき操作や、このリポジトリで利用している主要なライブラリについてまとめます。

## コミット前のチェック項目

1. `uv venv` で仮想環境を作成する
2. `uv sync --extra dev` で開発用依存関係をインストールする
3. コードフォーマットと静的解析を実行する
   ```bash
   uv run --frozen ruff check .
   uv run --frozen black --check .
   uv run --frozen pyright
   ```
4. テストを実行する
   ```bash
   PYTEST_DISABLE_PLUGIN_AUTOLOAD="" uv run --frozen pytest -q
   ```
5. すべてのファイルに対して pre-commit を実行する
   ```bash
   uv run pre-commit run --all-files
   ```

## 使用している主なライブラリ

| ライブラリ | 用途 |
|-----------|------|
| **uv** | 依存関係のインストールと実行管理 |
| **pytest** | テストフレームワーク |
| **ruff** | 静的解析ツール |
| **black** | コードフォーマッタ |
| **pre-commit** | コミット前のフック実行 |
| **pyright** | 型チェックツール |

Python の必須バージョンは `>=3.12` です。依存関係の詳細は `pyproject.toml` と `uv.lock` を参照してください。

## 不足している項目

- `uv` 自体のインストール方法
- `pre-commit install` の手順
- CI 環境での実行手順

