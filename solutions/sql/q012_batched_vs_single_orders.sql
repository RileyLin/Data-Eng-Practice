/*
Solution to Question 9.3.1: Batched vs. Single Orders Delivery Time

Write a SQL query to compare the average delivery time (order_delivered_timestamp - order_placed_timestamp) 
for batched orders versus single orders over the past 90 days. Include the percentage difference.
*/

-- Assume an `orders` table: `order_id`, `order_placed_timestamp`, `order_delivered_timestamp`, `is_batched` (BOOLEAN)
-- Or, `batch_id` (NULL if not batched, populated if batched).
-- For this example, let's use `is_batched` BOOLEAN.

WITH OrderDeliveryTimes AS (
    SELECT
        o.order_id,
        o.is_batched,
        -- Calculate delivery time in seconds. Adjust for other units or SQL dialects if needed.
        -- For PostgreSQL: EXTRACT(EPOCH FROM (o.order_delivered_timestamp - o.order_placed_timestamp))
        -- For SQL Server: DATEDIFF(second, o.order_placed_timestamp, o.order_delivered_timestamp)
        -- For MySQL: TIMESTAMPDIFF(SECOND, o.order_placed_timestamp, o.order_delivered_timestamp)
        EXTRACT(EPOCH FROM (o.order_delivered_timestamp - o.order_placed_timestamp)) AS delivery_time_seconds
    FROM
        orders o
    WHERE
        o.order_placed_timestamp >= CURRENT_DATE - INTERVAL '90 days'
        AND o.order_placed_timestamp < CURRENT_DATE
        AND o.order_delivered_timestamp IS NOT NULL -- Only consider delivered orders
),
AverageDeliveryTimes AS (
    SELECT
        odt.is_batched,
        AVG(odt.delivery_time_seconds) AS avg_delivery_time_seconds
    FROM
        OrderDeliveryTimes odt
    GROUP BY
        odt.is_batched
)
SELECT
    batched.avg_delivery_time_seconds AS avg_delivery_time_batched,
    single.avg_delivery_time_seconds AS avg_delivery_time_single,
    CASE
        WHEN single.avg_delivery_time_seconds = 0 THEN NULL -- Avoid division by zero, or could be 0 or 100% if batched is also 0 or not
        ELSE ROUND(((batched.avg_delivery_time_seconds - single.avg_delivery_time_seconds) * 100.0) / single.avg_delivery_time_seconds, 2)
    END AS percentage_difference_batched_vs_single
    -- Positive percentage means batched orders are slower.
    -- Negative percentage means batched orders are faster.
FROM
    (SELECT avg_delivery_time_seconds FROM AverageDeliveryTimes WHERE is_batched = TRUE) batched,
    (SELECT avg_delivery_time_seconds FROM AverageDeliveryTimes WHERE is_batched = FALSE) single;

/*
Explanation:

1.  `OrderDeliveryTimes` CTE:
    *   Selects from the `orders` table (aliased as `o`).
    *   Filters for orders placed within the last 90 full days.
    *   Ensures `order_delivered_timestamp` is not NULL, meaning the order was actually delivered.
    *   Calculates `delivery_time_seconds` for each order. The exact function for timestamp difference varies by SQL dialect (examples for PostgreSQL, SQL Server, MySQL are commented).
        For PostgreSQL, `EXTRACT(EPOCH FROM (timestamp_end - timestamp_start))` gives the difference in seconds.
    *   Keeps the `is_batched` flag to distinguish order types.

2.  `AverageDeliveryTimes` CTE:
    *   Calculates the average `delivery_time_seconds` from the `OrderDeliveryTimes` CTE.
    *   Groups by `is_batched` to get separate averages for batched (TRUE) and single (FALSE) orders.

3.  Final `SELECT` Statement:
    *   Retrieves the average delivery time for batched orders by selecting from `AverageDeliveryTimes` where `is_batched = TRUE` (subquery aliased as `batched`).
    *   Retrieves the average delivery time for single orders similarly (subquery aliased as `single`).
    *   Calculates `percentage_difference_batched_vs_single`:
        *   Formula: `((avg_batched - avg_single) / avg_single) * 100.0`.
        *   A positive result indicates batched orders are slower on average than single orders.
        *   A negative result indicates batched orders are faster.
        *   A `CASE` statement handles potential division by zero if `avg_delivery_time_single` is 0.
        *   `ROUND(..., 2)` formats the percentage to two decimal places.

Schema Assumptions:
orders:
- order_id (PK)
- user_id
- driver_id
- restaurant_id
- order_placed_timestamp
- order_delivered_timestamp
- is_batched (BOOLEAN: TRUE if part of a batch, FALSE otherwise)
  OR batch_id (INTEGER: NULL if not batched, Batch ID if batched - query would need slight change for this)

Example DDL & DML for testing (PostgreSQL syntax for intervals and EXTRACT):

DROP TABLE IF EXISTS orders;
CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    order_placed_timestamp TIMESTAMP,
    order_delivered_timestamp TIMESTAMP,
    is_batched BOOLEAN
);

INSERT INTO orders (order_placed_timestamp, order_delivered_timestamp, is_batched) VALUES
-- Single Orders (Last 90 days)
(CURRENT_DATE - INTERVAL '10 days' + INTERVAL '10 hours', CURRENT_DATE - INTERVAL '10 days' + INTERVAL '10 hours' + INTERVAL '30 minutes', FALSE), -- 30 min = 1800s
(CURRENT_DATE - INTERVAL '12 days' + INTERVAL '11 hours', CURRENT_DATE - INTERVAL '12 days' + INTERVAL '11 hours' + INTERVAL '25 minutes', FALSE), -- 25 min = 1500s
(CURRENT_DATE - INTERVAL '15 days' + INTERVAL '12 hours', CURRENT_DATE - INTERVAL '15 days' + INTERVAL '12 hours' + INTERVAL '35 minutes', FALSE), -- 35 min = 2100s
-- Batched Orders (Last 90 days)
(CURRENT_DATE - INTERVAL '5 days' + INTERVAL '13 hours', CURRENT_DATE - INTERVAL '5 days' + INTERVAL '13 hours' + INTERVAL '45 minutes', TRUE),  -- 45 min = 2700s
(CURRENT_DATE - INTERVAL '6 days' + INTERVAL '14 hours', CURRENT_DATE - INTERVAL '6 days' + INTERVAL '14 hours' + INTERVAL '50 minutes', TRUE),  -- 50 min = 3000s
(CURRENT_DATE - INTERVAL '7 days' + INTERVAL '15 hours', CURRENT_DATE - INTERVAL '7 days' + INTERVAL '15 hours' + INTERVAL '40 minutes', TRUE),  -- 40 min = 2400s
-- Order outside 90 days
(CURRENT_DATE - INTERVAL '100 days', CURRENT_DATE - INTERVAL '100 days' + INTERVAL '30 minutes', FALSE);

-- Calculations:
-- Avg Single Delivery Time: (1800 + 1500 + 2100) / 3 = 5400 / 3 = 1800 seconds.
-- Avg Batched Delivery Time: (2700 + 3000 + 2400) / 3 = 8100 / 3 = 2700 seconds.
-- Percentage Difference: ((2700 - 1800) / 1800) * 100 = (900 / 1800) * 100 = 0.5 * 100 = 50.00%

-- Expected Output:
-- avg_delivery_time_batched | avg_delivery_time_single | percentage_difference_batched_vs_single
-- ---------------------------|--------------------------|------------------------------------------
-- 2700.0                     | 1800.0                   | 50.00
*/ 