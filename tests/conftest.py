"""pytest用の共通フィクスチャを定義するモジュール"""

import os
from pathlib import Path
from typing import Generator

import pytest
import yaml
from python_agent_env.types import ConfigDict, Environment


@pytest.fixture(scope="session")
def test_data_dir() -> Path:
    """テストデータディレクトリのパスを返す"""
    return Path(__file__).parent / "data"


@pytest.fixture(scope="session")
def test_config() -> ConfigDict:
    """テスト用の設定を読み込む"""
    config_path = Path(__file__).parent / "data" / "test_config.yaml"
    with open(config_path, encoding="utf-8") as f:
        return yaml.safe_load(f)


@pytest.fixture(autouse=True)
def setup_test_environment() -> Generator[None, None, None]:
    """テスト環境のセットアップと後処理を行う"""
    # テスト前の環境変数を保存
    original_env = dict(os.environ)

    # テスト用の環境変数を設定
    os.environ.update(
        {
            "APP_ENV": Environment.DEVELOPMENT.name,
            "APP_DEBUG": "true",
            "APP_LOG_LEVEL": "DEBUG",
            "TEST_MODE": "true",
        }
    )

    yield

    # テスト後に環境変数を元に戻す
    os.environ.clear()
    os.environ.update(original_env)


@pytest.fixture
def temp_log_dir(tmp_path: Path) -> Generator[Path, None, None]:
    """一時的なログディレクトリを提供する"""
    log_dir = tmp_path / "logs"
    log_dir.mkdir()
    yield log_dir
