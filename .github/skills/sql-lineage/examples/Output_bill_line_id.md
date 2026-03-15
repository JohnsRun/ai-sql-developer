# #1 Field Lineage Graph: bill_line_id

#### add_item_to_bill
```text
[1] bill_line_id_seq.NEXTVAL
    |
    | (L:1427 INSERT VALUES)
    v
[2] billed_items.bill_line_id
    |
    | (L:1406 SELECT INTO)
    v
[3] v_line_id
    |
    v
[4] [-- terminal --]
```
bill_line_id originates from bill_line_id_seq.NEXTVAL and flows to billed_items.bill_line_id, then is read into v_line_id.

#### get_profits_for
```text
[1] billed_items.bill_line_id
    |
    | (L:919 SELECT CTE COLUMN)
    v
[2] avg_cost.bill_line_id
    |
    | (L:939 SELECT CTE COLUMN)
    v
[3] net_gain.bill_line_id
    |
    v
[4] [-- terminal --]
```
bill_line_id originates from billed_items.bill_line_id and flows through CTE columns in get_profits_for.

# #2 Occurrence Detail

#### Upstream — ASSIGNED FROM

| # | Line | Statement | Source |
|---|---|---|---|
| 1 | [L:919](../../../../02Development_Zone/Oracle_Package/JTA_Packages.sql#L919) | SELECT bi.bill_line_id, ... FROM billed_items bi JOIN customer_bills cb ON (cb.bill_id = bi.bill_id) | billed_items.bill_line_id |
| 2 | [L:933](../../../../02Development_Zone/Oracle_Package/JTA_Packages.sql#L933) | SELECT bi.bill_line_id, ... FROM billed_items bi JOIN avg_cost av ON (bi.bill_line_id = av.bill_line_id) | billed_items.bill_line_id |
| 3 | [L:939](../../../../02Development_Zone/Oracle_Package/JTA_Packages.sql#L939) | SELECT av.bill_line_id, ... FROM avg_cost av JOIN total_cost co ON (av.bill_line_id = co.bill_line_id) | avg_cost.bill_line_id |
| 4 | [L:1406](../../../../02Development_Zone/Oracle_Package/JTA_Packages.sql#L1406) | SELECT bill_line_id INTO v_line_id FROM billed_items WHERE product_id = v_product_id AND bill_id = p_bill_id | billed_items.bill_line_id |

#### Downstream — WRITTEN TO / PASSED TO / RETURNED

| # | Line | Statement | Destination |
|---|---|---|---|
| 1 | [L:919](../../../../02Development_Zone/Oracle_Package/JTA_Packages.sql#L919) | WITH avg_cost AS (SELECT bi.bill_line_id, ...) | avg_cost.bill_line_id |
| 2 | [L:933](../../../../02Development_Zone/Oracle_Package/JTA_Packages.sql#L933) | total_cost AS (SELECT bi.bill_line_id, ...) | total_cost.bill_line_id |
| 3 | [L:939](../../../../02Development_Zone/Oracle_Package/JTA_Packages.sql#L939) | net_gain AS (SELECT av.bill_line_id, ...) | net_gain.bill_line_id |
| 4 | [L:1423](../../../../02Development_Zone/Oracle_Package/JTA_Packages.sql#L1423) | INSERT INTO billed_items (bill_line_id, bill_id, product_id, quantity, price_rate, tax_code, tax_rate) VALUES (bill_line_id_seq.NEXTVAL, p_bill_id, v_product_id, 1, v_price, v_tax_code, v_tax_rate) | billed_items.bill_line_id |
