from enum import Enum
from typing import Any, Dict

ConfigDict = Dict[str, Any]
JsonDict = Dict[str, Any]


class Environment(Enum):
    DEVELOPMENT = "development"
    PRODUCTION = "production"
    TEST = "test"
