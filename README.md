# python_agent_env

Python開発のAIエージェント環境の雛形です。参考として [modelcontextprotocol/python-sdk](https://github.com/modelcontextprotocol/python-sdk) を元に簡易的な構成を用意しています。
このリポジトリでは `uv` で依存関係を管理し、`ruff` と `black` を使ってコードを整形・検証します。

## 使い方

```bash
uv pip install -e .[dev]
uv run --frozen ruff check .
uv run --frozen black --check .
PYTEST_DISABLE_PLUGIN_AUTOLOAD="" uv run --frozen pytest -q
```

CLI を試すには次のように実行します。

```bash
python-agent-env your-name
```

コミット前の検証には次を実行します。

```bash
uv run pre-commit run --all-files
```
