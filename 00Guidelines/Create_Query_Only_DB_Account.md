# Create a Query-Only DB Account in Oracle (PDB: `XEPDB1`)

This guide creates a read-only query user (`DEV_AI_QUERY`) with access to dictionary metadata and data query privileges in `XEPDB1`.

---

## 1. Connect as `SYSDBA` to `XEPDB1`

Connect directly to the pluggable database `XEPDB1`:

```sql
-- Via SQLcl / SQL*Plus
sql sys/<sys_password>@localhost:1521/XEPDB1 as sysdba
```

Or switch container if connected to `CDB$ROOT`:

```sql
ALTER SESSION SET CONTAINER = XEPDB1;
```

---

## 2. Create the User

```sql
CREATE USER DEV_AI_QUERY IDENTIFIED BY "YourStrongPassword#123"
  DEFAULT TABLESPACE USERS
  TEMPORARY TABLESPACE TEMP
  QUOTA 0 ON USERS
  ACCOUNT UNLOCK;
```

---

## 3. Grant Session & Read Privileges

```sql
-- Basic logon privilege
GRANT CREATE SESSION TO DEV_AI_QUERY;

-- Allow querying any data table/view (Read-Only)
GRANT READ ANY TABLE TO DEV_AI_QUERY;

-- Allow querying data dictionary & DBMS_METADATA.GET_DDL for other schemas
GRANT SELECT_CATALOG_ROLE TO DEV_AI_QUERY;

-- Ensure all granted roles are enabled automatically at logon
ALTER USER DEV_AI_QUERY DEFAULT ROLE ALL;
```

---

## 4. (Optional) Auto-Switch Current Schema on Logon

If the user primarily queries objects in target schema `DEV`:

```sql
CREATE OR REPLACE TRIGGER DEV_AI_QUERY.trg_after_logon_set_schema
AFTER LOGON ON DEV_AI_QUERY.SCHEMA
BEGIN
    EXECUTE IMMEDIATE 'ALTER SESSION SET CURRENT_SCHEMA = DEV';
END;
/
```

---

## 5. Verification

Connect as `DEV_AI_QUERY` and verify:

```sql
-- 1. Check active session user and schema
SELECT sys_context('USERENV', 'SESSION_USER') AS session_user,
       sys_context('USERENV', 'CURRENT_SCHEMA') AS current_schema,
       sys_context('USERENV', 'CON_NAME') AS pdb_name
  FROM dual;

-- 2. Verify SELECT_CATALOG_ROLE is active
SELECT role FROM session_roles WHERE role = 'SELECT_CATALOG_ROLE';

-- 3. Verify DDL extraction on target schema
SELECT DBMS_METADATA.GET_DDL('PACKAGE_BODY', 'PKG_JTA_ERROR', 'DEV') AS ddl FROM dual;
```
