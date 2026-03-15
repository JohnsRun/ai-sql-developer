# #1 Dependency Analysis: *get_date()* in *jta*

#### Upstream Procedures
1. **`get_profits_for`**
   - **Call Line**: `jta.get_date(v_current_time);` [JTA_Packages.sql:951](../02Development_Zone/Oracle_Package/JTA_Packages.sql#L951)
   - **Procedure Body**: [JTA_Packages.sql:904-963](../02Development_Zone/Oracle_Package/JTA_Packages.sql#L904-L963)
   - **Reads**: `billed_items`, `customer_bills`, `cost_sales_tracker`
2. **`stock_check`**
   - **Call Line**: `jta.get_date(v_current_time);` [JTA_Packages.sql:1782](../02Development_Zone/Oracle_Package/JTA_Packages.sql#L1782)
   - **Procedure Body**: [JTA_Packages.sql:1734-1797](../02Development_Zone/Oracle_Package/JTA_Packages.sql#L1734-L1797)
   - **Reads**: `inventory_by_location`

#### Downstream Procedures
1. **`get_hours()`**
   - **Call Line**: [get_hours(v_staff_id, v_start_date, v_end_date, v_basic, v_overtime, v_doubletime)](../02Development_Zone/Oracle_Package/JTA_Packages.sql#L1141)
   - **Procedure Body**: [JTA_Packages.sql:255-288](../02Development_Zone/Oracle_Package/JTA_Packages.sql#L255-L288)
   - **Reads**: `work_hours`
2. **`jta_error.log_error()`**
   - **Call Line**: [jta_error.log_error(SQLCODE, SQLERRM)](../02Development_Zone/Oracle_Package/JTA_Packages.sql#L1151)
   - **Procedure Body**: [JTA_Packages.sql:58-72](../02Development_Zone/Oracle_Package/JTA_Packages.sql#L58-L72)
   - **Reads**: None
----
# #2 Mechanism Analysis for *get_date()*
## 1.Preparation
- Input Parameters: `p_local_time OUT NOCOPY DATE`; local variables initialized for hours and date range (`v_basic`, `v_overtime`, `v_doubletime`, `v_staff_id`, `v_start_date`, `v_end_date`). [JTA_Packages.sql:1119-1129](../02Development_Zone/Oracle_Package/JTA_Packages.sql#L1119-L1129)
- Output Parameters: `p_local_time` returns database server local datetime (or `NULL` on exception). [JTA_Packages.sql:1132-1133](../02Development_Zone/Oracle_Package/JTA_Packages.sql#L1132-L1133)
## 2.Load Data
- Loads current server datetime using `SELECT SYSDATE ... FROM DUAL` into `p_local_time`. [JTA_Packages.sql:1132](../02Development_Zone/Oracle_Package/JTA_Packages.sql#L1132)
- Computes weekly window (`TRUNC(p_local_time, 'DAY')` to `+ 6`) for hour retrieval. [JTA_Packages.sql:1138-1139](../02Development_Zone/Oracle_Package/JTA_Packages.sql#L1138-L1139)
## 3.Transform and Logic Condition
- Calls `get_hours(...)` with fixed `v_staff_id := 1` and computed week window to populate basic/overtime/doubletime values. [JTA_Packages.sql:1141](../02Development_Zone/Oracle_Package/JTA_Packages.sql#L1141)
- Emits informational output lines for current local time, staff id, period, and calculated hours via `dbms_output.put_line`. [JTA_Packages.sql:1135-1146](../02Development_Zone/Oracle_Package/JTA_Packages.sql#L1135-L1146)
- On failure, logs with `jta_error.log_error(SQLCODE, SQLERRM)` and sets `p_local_time := NULL`. [JTA_Packages.sql:1149-1152](../02Development_Zone/Oracle_Package/JTA_Packages.sql#L1149-L1152)
## 4.Final Output
- Returns control to caller with `p_local_time` populated from `SYSDATE`, plus console diagnostics; no table writes occur in this procedure body. [JTA_Packages.sql:1132-1146](../02Development_Zone/Oracle_Package/JTA_Packages.sql#L1132-L1146)
----
# #3 Body Script of *get_date()*
```sql
PROCEDURE get_date (
    p_local_time OUT NOCOPY DATE
)
IS
    v_basic INTEGER;
    v_overtime INTEGER;
    v_doubletime INTEGER;
    v_staff_id staff.staff_id%TYPE := 1; -- example staff_id
    v_start_date DATE;
    v_end_date DATE;
BEGIN
    -- retrieve current date and time from the database server
    SELECT SYSDATE INTO p_local_time FROM DUAL;
    
    -- display current date and time
    dbms_output.put_line('Current local time: ' || TO_CHAR(p_local_time, 'yyyy-Mon-dd HH24:MI:SS'));
    
    -- set date range (example: current week)
    v_start_date := TRUNC(p_local_time, 'DAY');
    v_end_date := v_start_date + 6;
    
    -- call get_hours to retrieve and display hours worked
    get_hours(v_staff_id, v_start_date, v_end_date, v_basic, v_overtime, v_doubletime);
    
    -- display hours information
    dbms_output.put_line('Staff ID: ' || v_staff_id);
    dbms_output.put_line('Period: ' || TO_CHAR(v_start_date, 'yyyy-Mon-dd') || ' to ' || TO_CHAR(v_end_date, 'yyyy-Mon-dd'));
    dbms_output.put_line('Basic hours: ' || v_basic || ', Overtime: ' || v_overtime || ', Double time: ' || v_doubletime);
    
EXCEPTION
    WHEN OTHERS THEN
        -- log error and set output to NULL
        jta_error.log_error(SQLCODE, SQLERRM);
        p_local_time := NULL;
        dbms_output.put_line('Error retrieving date and hours information');
END get_date;
```