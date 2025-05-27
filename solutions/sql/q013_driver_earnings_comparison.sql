/*
Solution to Question 9.3.2: Driver Earnings Comparison

Write a SQL query to calculate, for each driver, the average earnings per hour 
when handling batched orders versus single orders over the past 90 days. 
Include only drivers who have completed at least 10 of each order type.
*/

-- Assumed tables:
-- `orders`: `order_id`, `driver_id`, `order_placed_timestamp`, `order_delivered_timestamp`, 
--           `is_batched` (BOOLEAN), `order_earnings` (DECIMAL, total earnings for driver from this order)
--           `actual_pickup_timestamp`, `actual_dropoff_timestamp` (more precise for time on task)
-- For simplicity, we'll use `order_placed_timestamp` to `order_delivered_timestamp` for duration for single orders.
-- For batched orders, defining "time spent" is more complex. If a batch has its own start/end time, that's ideal.
-- If not, we might have to sum durations of orders within a batch or use driver's first pickup to last dropoff for a batch.
-- This query will assume `order_delivered_timestamp - order_placed_timestamp` as a proxy for time_spent_on_order.
-- A more realistic model for batched orders would track time per batch/trip rather than summing individual order durations that overlap.

WITH RelevantOrders AS (
    SELECT
        o.order_id,
        o.driver_id,
        o.is_batched,
        o.order_earnings,
        EXTRACT(EPOCH FROM (o.order_delivered_timestamp - o.order_placed_timestamp)) AS delivery_duration_seconds
        -- Note: For batched orders, this duration is for the individual order, not necessarily the whole batch trip time.
        -- A more accurate `time_spent_on_task_seconds` would be better here if available, especially for batches.
    FROM
        orders o
    WHERE
        o.order_placed_timestamp >= CURRENT_DATE - INTERVAL '90 days'
        AND o.order_placed_timestamp < CURRENT_DATE
        AND o.order_delivered_timestamp IS NOT NULL
        AND o.order_earnings IS NOT NULL
        AND EXTRACT(EPOCH FROM (o.order_delivered_timestamp - o.order_placed_timestamp)) > 0 -- Avoid zero or negative duration
),
DriverOrderTypeCounts AS (
    SELECT
        driver_id,
        SUM(CASE WHEN is_batched = TRUE THEN 1 ELSE 0 END) AS batched_order_count,
        SUM(CASE WHEN is_batched = FALSE THEN 1 ELSE 0 END) AS single_order_count
    FROM
        RelevantOrders
    GROUP BY
        driver_id
),
EligibleDrivers AS (
    SELECT driver_id
    FROM DriverOrderTypeCounts
    WHERE batched_order_count >= 10 AND single_order_count >= 10
),
DriverEarningsPerType AS (
    SELECT
        ro.driver_id,
        ro.is_batched,
        SUM(ro.order_earnings) AS total_earnings_for_type,
        SUM(ro.delivery_duration_seconds) AS total_duration_seconds_for_type
    FROM
        RelevantOrders ro
    JOIN
        EligibleDrivers ed ON ro.driver_id = ed.driver_id
    GROUP BY
        ro.driver_id,
        ro.is_batched
)
SELECT
    dep.driver_id,
    MAX(CASE WHEN dep.is_batched = TRUE THEN (dep.total_earnings_for_type * 3600.0 / dep.total_duration_seconds_for_type) ELSE NULL END) AS avg_hourly_earnings_batched,
    MAX(CASE WHEN dep.is_batched = FALSE THEN (dep.total_earnings_for_type * 3600.0 / dep.total_duration_seconds_for_type) ELSE NULL END) AS avg_hourly_earnings_single
FROM
    DriverEarningsPerType dep
WHERE dep.total_duration_seconds_for_type > 0 -- Ensure we don't divide by zero for duration
GROUP BY
    dep.driver_id
ORDER BY
    dep.driver_id;

/*
Explanation:

1.  `RelevantOrders` CTE:
    *   Filters orders from the last 90 days that have been delivered and have earnings data.
    *   Calculates `delivery_duration_seconds` for each order (time from placement to delivery).
    *   Important Caveat: For batched orders, this individual order duration isn't the true "time spent by driver on batch". A better metric would be time from first pickup of batch to last dropoff of batch. This query uses order duration as a proxy due to typical `orders` table structure. If batch-level timing is available (`fact_batched_trips`), it should be used for batched calculations.
    *   Filters out orders with zero or negative duration.

2.  `DriverOrderTypeCounts` CTE:
    *   Counts the number of batched and single orders completed by each driver using data from `RelevantOrders`.

3.  `EligibleDrivers` CTE:
    *   Selects `driver_id`s who meet the criteria: at least 10 batched orders AND at least 10 single orders.

4.  `DriverEarningsPerType` CTE:
    *   For eligible drivers only, it sums up `total_earnings` and `total_duration_seconds` separately for their batched orders and their single orders.

5.  Final `SELECT` Statement:
    *   Pivots the data from `DriverEarningsPerType` to show batched and single hourly earnings in separate columns for each driver.
    *   `MAX(CASE ...)` is used with `GROUP BY driver_id` to achieve this pivot.
    *   Calculates average hourly earnings: (`total_earnings_for_type` / `total_duration_seconds_for_type`) * 3600 (to convert seconds to hours).
    *   Filters out cases where `total_duration_seconds_for_type` is zero to prevent division by zero errors.
    *   Orders by `driver_id`.

Challenges & Assumptions:
*   **Time on Task for Batched Orders:** The most significant challenge is accurately measuring "time spent" for batched orders. Summing individual order durations in a batch is incorrect as they overlap. Ideally, a batch-level table (`fact_batched_trips` with `batch_start_time`, `batch_end_time`, `total_batch_earnings_for_driver`) would be used for the batched part of the calculation.
*   **Definition of Earnings:** `order_earnings` is assumed to be the driver's pay for that specific order.
*   **Data Granularity:** Assumes the `orders` table contains all necessary fields.

Schema Assumptions:
orders:
- order_id (PK)
- driver_id (FK)
- order_placed_timestamp
- order_delivered_timestamp
- is_batched (BOOLEAN)
- order_earnings (DECIMAL, driver's earnings for this order)

Example DDL & DML for testing (PostgreSQL syntax):

DROP TABLE IF EXISTS orders;
CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    driver_id INTEGER,
    order_placed_timestamp TIMESTAMP,
    order_delivered_timestamp TIMESTAMP,
    is_batched BOOLEAN,
    order_earnings DECIMAL(10,2)
);

-- Insert data for Driver 1 (eligible)
DO $$ 
BEGIN
  FOR i IN 1..10 LOOP
    INSERT INTO orders (driver_id, order_placed_timestamp, order_delivered_timestamp, is_batched, order_earnings) VALUES
    (1, NOW() - (i+5||' days')::interval, NOW() - (i+5||' days')::interval + '30 minutes', FALSE, 5.00 + i*0.1); -- Single, 30min, ~ $5-6
    INSERT INTO orders (driver_id, order_placed_timestamp, order_delivered_timestamp, is_batched, order_earnings) VALUES
    (1, NOW() - (i||' days')::interval, NOW() - (i||' days')::interval + '45 minutes', TRUE, 7.00 + i*0.1); -- Batched, 45min, ~ $7-8
  END LOOP;
END $$;

-- Insert data for Driver 2 (not enough single orders)
DO $$ 
BEGIN
  FOR i IN 1..10 LOOP
    INSERT INTO orders (driver_id, order_placed_timestamp, order_delivered_timestamp, is_batched, order_earnings) VALUES
    (2, NOW() - (i||' days')::interval, NOW() - (i||' days')::interval + '50 minutes', TRUE, 8.00);
  END LOOP;
  INSERT INTO orders (driver_id, order_placed_timestamp, order_delivered_timestamp, is_batched, order_earnings) VALUES
  (2, NOW() - '1 day', NOW() - '1 day' + '20 minutes', FALSE, 3.00); -- Only 1 single order
END $$;

-- Expected Analysis for Driver 1:
-- Single: 10 orders, each 1800s (0.5 hr). Total time = 5 hrs. Avg earning ~$5.5. Total earning ~$55. Hourly ~$11.
-- Batched: 10 orders, each 2700s (0.75 hr). Total time = 7.5 hrs. Avg earning ~$7.5. Total earning ~$75. Hourly ~$10.

-- Expected output for Driver 1 (exact earnings will vary slightly due to loop increment):
-- driver_id | avg_hourly_earnings_batched | avg_hourly_earnings_single
-- ----------|-----------------------------|----------------------------
-- 1         | <around 10.xx>              | <around 11.xx>
-- (Driver 2 will not appear as they don't have >= 10 single orders)
*/ 