"""テストヘルパー関数を提供するモジュール"""

from datetime import datetime
from pathlib import Path
from typing import Any

import yaml
from python_agent_env.types import JsonDict


def create_test_config(config_data: dict[str, Any], config_path: Path) -> None:
    """テスト用の設定ファイルを作成する

    Args:
        config_data: 設定データ
        config_path: 設定ファイルのパス
    """
    config_path.parent.mkdir(parents=True, exist_ok=True)
    with open(config_path, "w", encoding="utf-8") as f:
        yaml.safe_dump(config_data, f)


def create_test_file(content: str, file_path: Path) -> None:
    """テスト用のファイルを作成する

    Args:
        content: ファイルの内容
        file_path: ファイルのパス
    """
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(content, encoding="utf-8")


def generate_test_data(base_dict: JsonDict, **overrides: Any) -> JsonDict:
    """テスト用のデータを生成する

    Args:
        base_dict: ベースとなる辞書
        **overrides: 上書きするキーと値

    Returns:
        dict: 生成されたテストデータ
    """
    result = base_dict.copy()
    result.update(overrides)
    return result


class FakeDateTime:
    """datetime.nowのモック用クラス"""

    def __init__(self, fixed_time: datetime) -> None:
        self._fixed_time = fixed_time

    def now(self) -> datetime:
        """固定の時刻を返す"""
        return self._fixed_time
