# 開発ガイド

このドキュメントは、このリポジトリでの開発をスムーズに進めるためのガイドです。

## 1. 概要

このプロジェクトは、堅牢で使いやすいPythonプロジェクトの雛形を目指しています。以下の主要なツールとプラクティスを採用しています。

- **`uv`**: 高速なPythonパッケージインストーラおよび依存関係マネージャ。
- **`src`レイアウト**: ソースコードを`src/python_agent_env`に配置する標準的なプロジェクト構造。
- **`ruff`**: 高速なPythonリンターおよびフォーマッター。
- **`black`**: 厳格なPythonコードフォーマッター。
- **`pyright`**: Pythonの静的型チェッカー。
- **`pytest`**: Pythonのテストフレームワーク。
- **`.env`ファイル**: 環境変数と機密情報の管理。
- **GitHub Actions**: CI/CDワークフロー。
- **Pre-commit Hooks**: コミット前の自動チェック。

## 2. 開発環境のセットアップ

### 前提条件

- Python 3.12
- `uv` (インストールされていない場合は `pip install uv` でインストールできます)

### セットアップ手順

1.  リポジトリをクローンします。
    ```bash
    git clone <your-repository-url>
    cd <your-repository-name>
    ```

2.  仮想環境を作成し、依存関係をインストールします。
    ```bash
    uv venv
    uv sync --extra dev
    ```
    これにより、プロジェクトに必要なすべての依存関係と開発ツールがインストールされます。

## 3. コード構造

ソースコードは`src/python_agent_env`ディレクトリ内に配置されます。

```
/workspace/
└───src/
    └───python_agent_env/
        ├───__init__.py
        ├───greet.py
        ├───main.py
        └───types.py
```

- `src/python_agent_env`: プロジェクトの主要なPythonパッケージ。
- `tests/`: テストコード。

## 4. 依存関係の管理

`uv`を使用して依存関係を管理します。

- **新しい依存関係の追加**:
    ```bash
    uv add <package-name>
    ```
    開発環境のみに必要な場合は、`uv add <package-name> --group dev` を使用します。

- **依存関係の削除**:
    ```bash
    uv remove <package-name>
    ```

- **依存関係の同期**:
    `pyproject.toml`または`uv.lock`が変更された場合、または新しい環境で作業を開始する場合に実行します。
    ```bash
    uv sync
    ```

## 5. コード品質

`ruff`, `black`, `pyright` を使用してコード品質を維持します。

- **Linting (ruff)**:
    ```bash
    uv run --frozen ruff check .
    ```

- **Formatting (black)**:
    ```bash
    uv run --frozen black .
    ```
    コードを自動的にフォーマットします。

- **Type Checking (pyright)**:
    ```bash
    uv run --frozen pyright
    ```

## 6. テスト

`pytest`を使用してテストを実行します。

- **すべてのテストを実行**:
    ```bash
    PYTEST_DISABLE_PLUGIN_AUTOLOAD="" uv run --frozen pytest
    ```

- **特定のテストファイルを実行**:
    ```bash
    PYTEST_DISABLE_PLUGIN_AUTOLOAD="" uv run --frozen pytest tests/test_greet.py
    ```

## 7. 環境変数の管理

APIキーなどの機密情報や環境ごとの設定値は、`.env`ファイルを使用して管理します。

1.  `.env.example`を参考に、`.env`ファイルを作成します。
    ```bash
    cp .env.example .env
    ```

2.  `.env`ファイルに環境変数を記述します。例:
    ```
    API_KEY=your_actual_api_key
    ```

3.  Pythonコード内で環境変数を読み込むには、`python-dotenv`を使用します。
    ```python
    from dotenv import load_dotenv
    import os

    load_dotenv() # .envファイルを読み込む
    api_key = os.getenv("API_KEY")
    ```
    `.env`ファイルは`.gitignore`によってバージョン管理から除外されています。

## 8. CI/CD (GitHub Actions)

`.github/workflows/ci.yml`に定義されているGitHub Actionsワークフローは、以下のタスクを自動的に実行します。

- コードのLinting (`ruff`, `black`, `pyright`)
- テストの実行 (`pytest`)
- 依存関係の脆弱性スキャン (`uv pip audit`)

プルリクエストが作成された際や`main`ブランチにプッシュされた際に自動的に実行され、コードの品質とセキュリティを保証します。

## 9. Pre-commit Hooks

このリポジトリでは、`pre-commit`フレームワークを使用して、コミット前に自動的にコード品質チェックを実行します。

- **手動で実行**:
    ```bash
    pre-commit run --all-files
    ```
    これにより、コミット前に設定されたすべてのフックが実行されます。

- **フックのインストール**:
    初回セットアップ時に`uv sync --extra dev`を実行すると自動的にインストールされます。手動でインストールする場合は以下を実行します。
    ```bash
    pre-commit install
    ```
