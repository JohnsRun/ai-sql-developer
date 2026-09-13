import importlib.util
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / ".github" / "agents" / "DB_DDL_AGENT" / "ref" / "db_connect_ddl.py"
SPEC = importlib.util.spec_from_file_location("db_connect_ddl", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC is not None and SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


def test_load_config_accepts_service_alias_without_host_port(monkeypatch):
    monkeypatch.setenv("ORA_SERVICE_DEV", "XEPDB1")
    monkeypatch.setenv("ORA_USER_QUERY_DEV", "DEV_AI_QUERY")
    monkeypatch.setenv("ORA_PASSWORD_QUERY_DEV", "123456")
    monkeypatch.delenv("ORA_HOST", raising=False)
    monkeypatch.delenv("ORA_PORT", raising=False)

    config = MODULE._load_config("DEV")

    assert config["service"] == "XEPDB1"
    assert config["user"] == "DEV_AI_QUERY"
    assert config["password"] == "123456"
    assert config["dsn"] == "XEPDB1"
