# python_agent_env

Python開発のAIエージェント環境の雛形です。参考として [modelcontextprotocol/python-sdk](https://github.com/modelcontextprotocol/python-sdk) を元に簡易的な構成を用意しています。
このリポジトリでは `uv` で依存関係を管理し、`ruff` と `black` を使ってコードを整形・検証します。

## 使い方

```bash
uv pip install -e .[dev]
ruff .
black --check .
pytest -q
```

CLI を試すには次のように実行します。

```bash
python-agent-env your-name
```
