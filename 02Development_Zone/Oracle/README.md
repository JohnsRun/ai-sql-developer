# Grocery Market Oracle PL/SQL Example

This project is an Oracle PL/SQL database example for a grocery-market business. It models products, inventory, suppliers, staff, payroll, customer bills, payments, purchase orders, and operational events.

The example is based on the retail activities of JTA Supermarkets in Trinidad and Tobago. It is an educational database-design project and is not affiliated with JTA Supermarkets.

## Project Files

- `JTA_Create_Database.sql` drops and recreates the tables, constraints, sequences, and sample data.
- `JTA_Packages.sql` creates the error-handling package, business package, and database triggers.
- `JTA_Test_Code.sql` runs anonymous blocks and queries that exercise the package API and trigger behavior.
- `ERD_High_quality.png` contains the database entity-relationship diagram.

## Execution Order

Run the scripts in this order in the target Oracle schema:

1. `JTA_Create_Database.sql`
2. `JTA_Packages.sql`
3. `JTA_Test_Code.sql`

The test script performs inserts, updates, payments, inventory changes, and tax changes. Run it against a freshly initialized schema when repeatable results are required.

## Troubleshooting Compilation Errors

Errors such as `ORA-00942: table or view does not exist` or `PLS-00201` while compiling `pkg_jta_error`, `pkg_jta`, or the triggers normally mean that `JTA_Create_Database.sql` was not run, failed, or was run in a different schema.

Check the current schema and required objects before compiling the packages:

```sql
SELECT USER FROM dual;

SELECT object_name, object_type, status
FROM user_objects
WHERE object_name IN (
  'JTA_ERRORS',
  'COST_SALES_TRACKER',
  'STAFF',
  'INVENTORY_BY_LOCATION',
  'JTA_EVENTS'
)
ORDER BY object_type, object_name;
```

Run `JTA_Create_Database.sql` and `JTA_Packages.sql` as the same schema, in that order. Do not run `JTA_Test_Code.sql` until both packages and all triggers compile successfully. The database script is destructive because it drops and recreates the example objects, so use a dedicated development schema.

## Object Naming Rules

The SQL objects in this example follow these prefixes:

| Object type | Required prefix | Example |
| --- | --- | --- |
| Package | `pkg_` | `pkg_jta` |
| Stored procedure | `sp_` | `sp_update_inventory` |
| Function | `fn_` | `fn_receive_payment` |
| Sequence | `seq_` | `seq_product_id` |

Package members follow the same procedure and function rules. Exception identifiers remain descriptive names such as `invalid_input` and `missing_data` because they are not procedures or functions. Trigger names remain descriptive and use the existing names in this example.

## Packages

### `pkg_jta_error`

This package centralizes application errors:

- `sp_throw` raises an application error.
- `sp_log_error` writes an error to `jta_errors`.
- `sp_show_in_console` writes a non-fatal message to the console.
- `invalid_input` and `missing_data` are the public exception identifiers.

### `pkg_jta`

This package contains the grocery-market business operations.

#### Payroll and staff

- `sp_process_payroll`
- `sp_payout`
- `sp_sunday_check`
- `fn_get_name`

#### Inventory and purchasing

- `sp_update_inventory`
- `sp_restock_urgent`
- `sp_evaluate_po_order_line`
- `sp_update_sales`
- `sp_stock_check`

#### Bills and payments

- `sp_lookup_barcode`
- `sp_add_item_to_bill`
- `sp_update_from_bill`
- `fn_receive_payment`
- `fn_get_last_cashier_payout`
- `fn_get_money_inflow`

#### Prices, taxes, and reporting

- `sp_update_taxes`
- `fn_get_price_changes`
- `sp_get_profits_for`
- `sp_get_recommended_price_for`
- `fn_get_tax_payment_due`
- `fn_get_quantity_sold`

The private package procedures `sp_get_hours` and `sp_get_date` support payroll and diagnostic operations inside `pkg_jta`.

## Triggers

The trigger names are not part of the package, procedure, function, or sequence naming rules. They remain:

- `update_job_history_trigger` updates job-history records when a staff member changes job.
- `email_on_inv_trigger` reports inventory that falls below its minimum level. The example writes the intended email to `DBMS_OUTPUT`.
- `logon_trigger` records schema logons in `jta_events` and checks the authorized IP list.
- `logoff_trigger` records schema logoffs in `jta_events`.

Triggers are tested indirectly. Updating `staff.job_id` tests the job-history trigger, and updating inventory quantities tests the inventory trigger. Logon and logoff triggers require reconnecting to the schema.

When testing the job-history trigger, leave at least one second between consecutive job changes for the same staff member because `job_posts_history` uses `(staff_id, date_started)` as its primary key and the trigger uses `SYSDATE`.

## Database Design Notes

The model distinguishes transactional values from values that must remain historically accurate. For example, the tax rate and price stored on a billed item remain unchanged after the sale, even when current tax rates or prices change.

Some frequently used values are stored redundantly to avoid repeatedly deriving them from large transactional tables. The `cost_sales_tracker` table keeps inventory totals and average costs, while `sold_products` stages sales for the daily `sp_update_sales` operation.

Most successful operations in `pkg_jta` commit their changes. This behavior is intentional for the educational example, but production applications should define transaction ownership and commit boundaries explicitly.

## Business Scope

The model supports the following business areas:

- Product catalog, categories, barcodes, price lookup codes, tax rates, prices, and stock thresholds.
- Branch and warehouse inventory, missing items, stock checks, and restocking.
- Suppliers, supplier contacts, purchase orders, invoices, and invoice payments.
- Staff details, job history, work hours, payroll, deductions, and payout reporting.
- Cashier stations, drawer assignments, customer bills, payment methods, and payment status.

The design can be extended for additional branches, independent warehouses, product transfers, and more detailed accounting rules.

## Barcodes and PLUs

Pre-packaged products use a barcode. Weighted or individually priced products use a price lookup code (PLU). In this example, a PLU begins with `2` and contains a product identifier, check digits, and a five-digit price component.

Example layout:

```text
2 | 1234 | 5 | 01206 | 7
  | item |   | price | check
```

The test script exercises both a PLU lookup and a regular barcode lookup through `pkg_jta.sp_lookup_barcode`.

## Oracle Setup

The scripts must run in an Oracle schema with permission to create tables, sequences, packages, and triggers. For local Oracle Express testing, create and grant a dedicated schema from an administrative account, then reconnect as that schema before running the scripts.

The scripts are educational examples. Review grants, email configuration, trigger behavior, transaction ownership, indexes, and error handling before adapting them for production use.
