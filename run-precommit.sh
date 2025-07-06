#!/usr/bin/env bash
set -e

if [ -t 0 ]; then
  # 標準入力が端末（パイプなし）の場合
  file=""
else
  file=$(jq -r '.tool_input.file_path // empty' -)
fi

if [ -n "$file" ]; then
  uv run pre-commit run --hook-stage manual --files "$file"   # ← stage を明示
else
  uv run pre-commit run --hook-stage manual --all-files
fi