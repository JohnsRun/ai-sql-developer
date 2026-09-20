"""Oracle database connector — credentials from OS environment variables.

Required environment variables:
    ORA_HOST      Oracle hostname or IP
    ORA_PORT      Oracle listener port (e.g. 1521)
    ORA_SERVICE_DEV      DEV Oracle service name (e.g. XEPDB1)
    ORA_USER_ACTION_DEV      DEV query username
    ORA_PASSWORD_ACTION_DEV  DEV query password
    ORA_SERVICE_UAT      UAT Oracle service name (e.g. XE)
    ORA_USER_ACTION_UAT      UAT query username
    ORA_PASSWORD_ACTION_UAT  UAT query password

Optional environment variables:
    ORACLE_CLIENT_LIB_DIR Path to Oracle Instant Client libs (enables Thick mode)
"""
import os
import base64
import json
import oracledb
import pandas as pd
from datetime import datetime, date
from decimal import Decimal

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

_ENVIRONMENT_VARIABLES = {
    "DEV": ("ORA_SERVICE_DEV", "ORA_USER_ACTION_DEV", "ORA_PASSWORD_ACTION_DEV"),
    "UAT": ("ORA_SERVICE_UAT", "ORA_USER_ACTION_UAT", "ORA_PASSWORD_ACTION_UAT"),
}


def _load_config(environment: str) -> dict:
    """Load the selected environment's connection settings without exposing values."""
    service_variable, user_variable, password_variable = _ENVIRONMENT_VARIABLES[environment]
    required = ("ORA_HOST", "ORA_PORT", service_variable, user_variable, password_variable)
    missing = [variable for variable in required if not os.environ.get(variable)]
    if missing:
        raise ValueError(
            f"Missing required {environment} environment variable(s): " + ", ".join(missing)
        )
    try:
        port = int(os.environ["ORA_PORT"])
    except ValueError as error:
        raise ValueError("ORA_PORT must be an integer.") from error
    return {
        "host": os.environ["ORA_HOST"],
        "port": port,
        "service": os.environ[service_variable],
        "user": os.environ[user_variable],
        "password": os.environ[password_variable],
    }

# Thick mode — only if ORACLE_CLIENT_LIB_DIR is set
_client_lib = os.environ.get("ORACLE_CLIENT_LIB_DIR")
if _client_lib:
    oracledb.init_oracle_client(lib_dir=_client_lib)

DISPLAY_ROWS = 1_000    # max rows shown in notebook output

pd.set_option("display.max_columns", None)


# ---------------------------------------------------------------------------
# save ddl to file
# ---------------------------------------------------------------------------

def save_ddl(df: pd.DataFrame, filename: str):
    """Save a DataFrame to a CSV file."""
    with open(filename, 'w') as f:
        f.write(df)
    print(f"DataFrame saved to ./{filename}")


# ---------------------------------------------------------------------------
# Serialization
# ---------------------------------------------------------------------------

def _serialize_value(val):
    if val is None:
        return None
    # Oracle BLOB / raw bytes
    if isinstance(val, (bytes, bytearray)):
        return "<BLOB:" + base64.b64encode(val).decode("utf-8") + ">"
    if isinstance(val, memoryview):
        return "<BLOB:" + base64.b64encode(bytes(val)).decode("utf-8") + ">"
    # Oracle LOB (has .read())
    if hasattr(val, "read"):
        try:
            raw = val.read()
            if isinstance(raw, bytes):
                return "<BLOB:" + base64.b64encode(raw).decode("utf-8") + ">"
            try:
                return json.loads(raw)
            except (json.JSONDecodeError, TypeError):
                return str(raw)
        except Exception as e:
            return f"<LOB_ERROR:{e}>"
    if isinstance(val, (datetime, date)):
        return val.isoformat()
    if isinstance(val, Decimal):
        return float(val)
    if isinstance(val, str):
        stripped = val.strip()
        if stripped and stripped[0] in ("{", "["):
            try:
                return json.loads(stripped)
            except json.JSONDecodeError:
                pass
        return val
    return val


# ---------------------------------------------------------------------------
# Oracle
# ---------------------------------------------------------------------------

def query_oracle(sql: str, params=None, config: dict | None = None) -> pd.DataFrame | None:
    """Execute SQL against Oracle and return a pandas DataFrame."""
    cfg = config or _load_config("DEV")
    dsn = f"{cfg['host']}:{cfg['port']}/{cfg['service']}"
    try:
        with oracledb.connect(user=cfg["user"], password=cfg["password"], dsn=dsn) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, params or [])
                columns = [col[0].lower() for col in cur.description]
                rows = [
                    {col: _serialize_value(v) for col, v in zip(columns, row)}
                    for row in cur.fetchall()
                ]
                return pd.DataFrame(rows) if rows else pd.DataFrame(columns=columns)
    except oracledb.DatabaseError as e:
        (err,) = e.args
        print(f"Oracle error: {err}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def run_sql_dev(sql: str, params=None, config: dict | None = None) -> pd.DataFrame | None:
    """Execute SQL against Oracle and display up to DISPLAY_ROWS rows.

    Args:
        sql:    SQL statement to execute.
        params: Bind parameters (list or dict).
        config: Override connection config; uses ORA env vars by default.
    """
    sql = sql.replace(";", "")
    df = query_oracle(sql, params=params, config=config)
    if df is None:
        return None
    total = len(df)
    if total > DISPLAY_ROWS:
        print(f"Showing {DISPLAY_ROWS:,} of {total:,} rows.")
        return df.head(DISPLAY_ROWS)
    return df


def _register_notebook_magic() -> None:
    """Register %%dev and %%uat when loaded from an IPython notebook."""
    try:
        from IPython import get_ipython
        from IPython.core.magic import register_cell_magic
    except ImportError:
        return
    if get_ipython() is None:
        return

    def _run_notebook_sql(environment: str, sql: str):
        if not sql.strip():
            raise ValueError(f"%%{environment.lower()} requires a SQL statement.")
        return run_sql_dev(sql, config=_load_config(environment))

    @register_cell_magic
    def dev(line: str, cell: str):
        return _run_notebook_sql("DEV", cell)

    @register_cell_magic
    def uat(line: str, cell: str):
        return _run_notebook_sql("UAT", cell)


_register_notebook_magic()


def get_ddl_dev(object_type: str, object_name: str, schema: str='DEV') -> pd.DataFrame | None:
    """Get the DDL for a database object (table, view, package, etc.) in DEV schema.

    Args:
        object_type: Type of the object (e.g., 'TABLE', 'VIEW', 'PACKAGE').
        object_name: Name of the object.
        schema:      Optional schema name; defaults to DEV if not provided.
    """
    schema = schema or "DEV"
    sql = f"SELECT DBMS_METADATA.GET_DDL(:object_type, :object_name, :schema) AS ddl FROM DUAL"
    params = {"object_type": object_type.upper(), "object_name": object_name.upper(), "schema": schema.upper()}
    df = run_sql_dev(sql, params=params)
    if df is None or df.empty:
        print(f"No DDL found for {object_type} {schema}.{object_name}.")
        return None
    return df.iloc[0,0].strip() 

def exec_ddl(sql: str):
    """Execute a DDL statement (CREATE, ALTER, DROP)."""
    cfg = _load_config("DEV")
    dsn = f"{cfg['host']}:{cfg['port']}/{cfg['service']}"
    try:
        with oracledb.connect(user=cfg["user"], password=cfg["password"], dsn=dsn) as conn:
            with conn.cursor() as cur:
                cur.execute(sql)
                conn.commit()
                print("DDL executed successfully.")
    except oracledb.DatabaseError as e:
        (err,) = e.args
        print(f"Oracle error: {err}")
