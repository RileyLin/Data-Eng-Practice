/*
Solution to Question 1.3.1 (Carpool Segment Percentage)

Write a SQL query to calculate the percentage of ride segments that belong to a 'Carpool' ride type.
Assume fact_ride_segments links to fact_rides, and fact_rides links to dim_ride_type.
*/

-- Calculate percentage of ride segments that belong to 'Carpool' ride type
SELECT
    (COUNT(CASE WHEN drt.ride_type_name = 'Carpool' THEN frs.ride_segment_id ELSE NULL END) * 100.0)
    / NULLIF(COUNT(frs.ride_segment_id), 0) AS carpool_segment_percentage
FROM
    fact_ride_segments frs
JOIN
    fact_rides fr ON frs.ride_id = fr.ride_id
JOIN
    dim_ride_type drt ON fr.ride_type_key = drt.ride_type_key;

/*
Explanation:

1.  The query starts from the `fact_ride_segments` table (aliased as `frs`), which is assumed to contain individual segments of rides.
2.  It joins `fact_ride_segments` with `fact_rides` (aliased as `fr`) using `ride_id`. This step is necessary to link segments to their overall ride characteristics, specifically the `ride_type_key`.
3.  It then joins `fact_rides` with `dim_ride_type` (aliased as `drt`) using `ride_type_key`. This allows access to the `ride_type_name` (e.g., 'Carpool', 'Regular').
4.  In the SELECT clause:
    *   `COUNT(CASE WHEN drt.ride_type_name = 'Carpool' THEN frs.ride_segment_id ELSE NULL END)`: This part counts only those ride segments where the corresponding `ride_type_name` is 'Carpool'. If the condition is met, `ride_segment_id` is counted; otherwise, `NULL` is returned, which `COUNT` ignores for specific columns.
    *   `COUNT(frs.ride_segment_id)`: This counts all ride segments in the `fact_ride_segments` table, serving as the total number of segments.
    *   The result of the carpool segment count is multiplied by `100.0` to convert it into a percentage. The `.0` ensures floating-point division.
    *   `NULLIF(COUNT(frs.ride_segment_id), 0)`: This is a safeguard against division by zero. If the total count of ride segments is zero, `NULLIF` will return `NULL`, and the overall division will result in `NULL` instead of an error.
5.  The final result is a single value representing the percentage of all ride segments that are part of 'Carpool' rides.

Schema Assumptions:
fact_ride_segments:
- ride_segment_id (PK)
- ride_id (FK -> fact_rides)
- ...

fact_rides:
- ride_id (PK)
- ride_type_key (FK -> dim_ride_type)
- ...

dim_ride_type:
- ride_type_key (PK)
- ride_type_name ('Carpool', 'Regular', etc.)
- ...

Example DDL & DML for testing:

DROP TABLE IF EXISTS dim_ride_type;
CREATE TABLE dim_ride_type (
    ride_type_key INTEGER PRIMARY KEY,
    ride_type_name TEXT NOT NULL
);

DROP TABLE IF EXISTS fact_rides;
CREATE TABLE fact_rides (
    ride_id INTEGER PRIMARY KEY,
    ride_type_key INTEGER,
    FOREIGN KEY (ride_type_key) REFERENCES dim_ride_type(ride_type_key)
);

DROP TABLE IF EXISTS fact_ride_segments;
CREATE TABLE fact_ride_segments (
    ride_segment_id INTEGER PRIMARY KEY,
    ride_id INTEGER,
    rider_user_key INTEGER,
    FOREIGN KEY (ride_id) REFERENCES fact_rides(ride_id)
);

INSERT INTO dim_ride_type (ride_type_key, ride_type_name) VALUES
(1, 'Regular'),
(2, 'Carpool'),
(3, 'Premium');

INSERT INTO fact_rides (ride_id, ride_type_key) VALUES
(101, 1), -- Regular
(102, 2), -- Carpool
(103, 1), -- Regular
(104, 2); -- Carpool

INSERT INTO fact_ride_segments (ride_segment_id, ride_id, rider_user_key) VALUES
(1001, 101, 1), -- Regular ride segment
(1002, 102, 2), -- Carpool ride segment 1
(1003, 102, 3), -- Carpool ride segment 2 (same ride as 1002)
(1004, 103, 4), -- Regular ride segment
(1005, 104, 5), -- Carpool ride segment 3
(1006, 104, 6); -- Carpool ride segment 4

-- Expected output with this data:
-- Total segments = 6
-- Carpool segments = 4 (1002, 1003, 1005, 1006)
-- Percentage = (4 / 6) * 100.0 = 66.666...
-- carpool_segment_percentage
-- --------------------------
-- 66.66666666666667

*/

-- Calculate the percentage of rides that are carpool rides.

-- Assumptions:
-- 1. We have a `fact_rides` table with a `ride_id` and a `ride_type_key`.
-- 2. We have a `dim_ride_type` table with `ride_type_key` and `ride_type_name` 
--    (e.g., 'Standard', 'Carpool', 'Premium').
-- 3. Carpool rides are identified by `ride_type_name = 'Carpool'` in the `dim_ride_type` table.

-- Methodology:
-- 1. Count the total number of rides.
-- 2. Count the number of rides where the ride_type is 'Carpool'.
-- 3. Calculate the percentage: (Carpool Rides / Total Rides) * 100.

WITH RideCounts AS (
    SELECT
        COUNT(fr.ride_id) AS total_rides,
        SUM(CASE WHEN drt.ride_type_name = 'Carpool' THEN 1 ELSE 0 END) AS carpool_rides
    FROM
        fact_rides fr
    JOIN
        dim_ride_type drt ON fr.ride_type_key = drt.ride_type_key
)
SELECT
    (CAST(rc.carpool_rides AS REAL) / rc.total_rides) * 100 AS percentage_carpool_rides
FROM
    RideCounts rc;

-- Example of how to create and populate dummy tables for this query:
/*
DROP TABLE IF EXISTS fact_rides;
CREATE TABLE fact_rides (
    ride_id INTEGER PRIMARY KEY,
    driver_user_key INTEGER,
    ride_type_key INTEGER,
    start_timestamp TEXT,
    end_timestamp TEXT
);

DROP TABLE IF EXISTS dim_ride_type;
CREATE TABLE dim_ride_type (
    ride_type_key INTEGER PRIMARY KEY,
    ride_type_name TEXT NOT NULL -- e.g., 'Standard', 'Carpool', 'Premium'
);

INSERT INTO dim_ride_type (ride_type_key, ride_type_name) VALUES
(1, 'Standard'),
(2, 'Carpool'),
(3, 'Premium');

INSERT INTO fact_rides (ride_id, driver_user_key, ride_type_key, start_timestamp, end_timestamp) VALUES
(101, 1, 1, '2023-01-01 10:00:00', '2023-01-01 10:30:00'),
(102, 2, 2, '2023-01-01 10:15:00', '2023-01-01 10:45:00'),
(103, 1, 1, '2023-01-01 11:00:00', '2023-01-01 11:20:00'),
(104, 3, 2, '2023-01-01 11:30:00', '2023-01-01 12:00:00'),
(105, 4, 2, '2023-01-01 12:10:00', '2023-01-01 12:55:00'),
(106, 2, 3, '2023-01-01 12:30:00', '2023-01-01 13:00:00'),
(107, 1, 1, '2023-01-02 09:00:00', '2023-01-02 09:25:00'),
(108, 5, 2, '2023-01-02 09:30:00', '2023-01-02 10:10:00');

-- Expected output for the sample data (4 carpool rides / 8 total rides = 50.0%):
-- percentage_carpool_rides
-- 50.0
*/ 