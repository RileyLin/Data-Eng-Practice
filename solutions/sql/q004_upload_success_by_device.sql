/*
Solution to Question 7.3.1: Upload Success Rate by Device

Write a SQL query to calculate the upload success rate by device type for the past 30 days.
Include the total number of attempts and successful uploads in the result.
*/

SELECT 
    d.device_type,
    COUNT(pu.upload_id) AS total_attempts,
    SUM(CASE WHEN pu.upload_status = 'success' THEN 1 ELSE 0 END) AS successful_uploads,
    ROUND(
        SUM(CASE WHEN pu.upload_status = 'success' THEN 1 ELSE 0 END) * 100.0 / 
        NULLIF(COUNT(pu.upload_id), 0), 
        2
    ) AS success_rate_percentage
FROM 
    photo_uploads pu
JOIN 
    devices d ON pu.device_id = d.device_id
WHERE 
    pu.upload_timestamp >= CURRENT_DATE - INTERVAL '30 days'
    AND pu.upload_timestamp < CURRENT_DATE
GROUP BY 
    d.device_type
ORDER BY 
    success_rate_percentage DESC,
    total_attempts DESC;

/*
Explanation:

1.  Tables and Join:
    *   `photo_uploads` (aliased as `pu`): Assumed to contain records of each upload attempt. Key columns: `upload_id`, `device_id` (FK), `upload_status` ('success', 'failure'), `upload_timestamp`.
    *   `devices` (aliased as `d`): Assumed to contain device details. Key columns: `device_id` (PK), `device_type` (e.g., 'iOS', 'Android', 'Web').
    *   The tables are joined on `device_id`.

2.  Time Filtering:
    *   `WHERE pu.upload_timestamp >= CURRENT_DATE - INTERVAL '30 days' AND pu.upload_timestamp < CURRENT_DATE` filters for uploads that occurred in the last 30 full days (up to, but not including, the current day).

3.  Aggregation and Metrics Calculation (Grouped by `d.device_type`):
    *   `COUNT(pu.upload_id) AS total_attempts`: Counts all upload attempts for each device type.
    *   `SUM(CASE WHEN pu.upload_status = 'success' THEN 1 ELSE 0 END) AS successful_uploads`: Counts only the successful uploads for each device type.
    *   `success_rate_percentage`: Calculated as (`successful_uploads` * 100.0) / `total_attempts`.
        *   Multiplying by `100.0` ensures floating-point arithmetic for the percentage.
        *   `NULLIF(COUNT(pu.upload_id), 0)` prevents division by zero if a device type had no attempts.
        *   `ROUND(..., 2)` formats the percentage to two decimal places.

4.  Ordering:
    *   The results are ordered first by `success_rate_percentage` in descending order (highest success rate first).
    *   Then, by `total_attempts` in descending order as a tie-breaker.

Schema Assumptions:
photo_uploads:
- upload_id (PK)
- device_id (FK -> devices)
- user_id
- upload_timestamp
- upload_status ('success', 'failure')
- ...

devices:
- device_id (PK)
- device_type ('iOS', 'Android', 'Web', etc.)
- device_model
- ...

Example DDL & DML for testing:

DROP TABLE IF EXISTS devices;
CREATE TABLE devices (
    device_id INTEGER PRIMARY KEY,
    device_type TEXT NOT NULL,
    device_model TEXT
);

DROP TABLE IF EXISTS photo_uploads;
CREATE TABLE photo_uploads (
    upload_id INTEGER PRIMARY KEY AUTOINCREMENT,
    device_id INTEGER,
    user_id INTEGER,
    upload_timestamp TIMESTAMP,
    upload_status TEXT, -- 'success', 'failure'
    FOREIGN KEY (device_id) REFERENCES devices(device_id)
);

INSERT INTO devices (device_id, device_type, device_model) VALUES
(1, 'iOS', 'iPhone 14'),
(2, 'Android', 'Samsung S22'),
(3, 'Web', 'Chrome Browser'),
(4, 'iOS', 'iPhone 13');

-- Sample data for roughly the last 30 days
INSERT INTO photo_uploads (device_id, user_id, upload_timestamp, upload_status) VALUES
(1, 101, CURRENT_DATE - INTERVAL '2 days', 'success'),
(1, 102, CURRENT_DATE - INTERVAL '3 days', 'failure'),
(1, 103, CURRENT_DATE - INTERVAL '4 days', 'success'),
(2, 104, CURRENT_DATE - INTERVAL '5 days', 'success'),
(2, 105, CURRENT_DATE - INTERVAL '6 days', 'success'),
(2, 106, CURRENT_DATE - INTERVAL '7 days', 'failure'),
(2, 107, CURRENT_DATE - INTERVAL '8 days', 'success'),
(3, 108, CURRENT_DATE - INTERVAL '10 days', 'success'),
(4, 109, CURRENT_DATE - INTERVAL '12 days', 'failure'),
(4, 110, CURRENT_DATE - INTERVAL '15 days', 'failure'),
(1, 111, CURRENT_DATE - INTERVAL '40 days', 'success'); -- Outside 30-day window

-- Expected Analysis (for uploads within last 30 days):
-- iOS (devices 1 & 4):
--   Device 1: 2 success, 1 failure (Total 3)
--   Device 4: 0 success, 2 failure (Total 2)
--   Total iOS: 2 success, 3 failure (Total 5 attempts). Rate = (2/5)*100 = 40.00%
-- Android (device 2):
--   Device 2: 3 success, 1 failure (Total 4 attempts). Rate = (3/4)*100 = 75.00%
-- Web (device 3):
--   Device 3: 1 success, 0 failure (Total 1 attempt). Rate = (1/1)*100 = 100.00%

-- Expected Output (order might vary slightly based on exact ties if rates are same):
-- device_type | total_attempts | successful_uploads | success_rate_percentage
-- -------------|----------------|--------------------|--------------------------
-- Web         | 1              | 1                  | 100.00
-- Android     | 4              | 3                  | 75.00
-- iOS         | 5              | 2                  | 40.00
*/

-- Calculate photo upload success rates broken down by device type (e.g., iOS, Android) or device model.

-- Assumptions:
-- 1. `fact_upload_attempts` table: Contains records of each upload attempt, with columns like
--    `upload_attempt_id` (PK), `device_key` (FK), `status` ('success', 'failure'), `timestamp_event`.
-- 2. `dim_devices` table: Contains device details, with columns like
--    `device_key` (PK), `device_model`, `os_type` (e.g., 'iOS', 'Android', 'Web').
-- 3. We are interested in the success rate per `os_type`.

-- Methodology:
-- 1. Join `fact_upload_attempts` with `dim_devices` to get the `os_type` for each attempt.
-- 2. Group by `os_type`.
-- 3. For each `os_type`, count the total number of upload attempts.
-- 4. For each `os_type`, count the number of successful upload attempts (where `status = 'success'`).
-- 5. Calculate the success rate: (Successful Attempts / Total Attempts) * 100.

SELECT
    dd.os_type,
    COUNT(fua.upload_attempt_id) AS total_attempts,
    SUM(CASE WHEN fua.status = 'success' THEN 1 ELSE 0 END) AS successful_attempts,
    CASE
        WHEN COUNT(fua.upload_attempt_id) = 0 THEN 0
        ELSE (SUM(CASE WHEN fua.status = 'success' THEN 1 ELSE 0 END) * 100.0 / COUNT(fua.upload_attempt_id))
    END AS success_rate_percentage
FROM
    fact_upload_attempts fua
JOIN
    dim_devices dd ON fua.device_key = dd.device_key
-- Optional: Filter for a specific period
-- WHERE DATE(fua.timestamp_event) BETWEEN '2023-01-01' AND '2023-01-31'
GROUP BY
    dd.os_type
ORDER BY
    dd.os_type;

-- Example of how to create and populate dummy tables for this query:
/*
DROP TABLE IF EXISTS fact_upload_attempts;
CREATE TABLE fact_upload_attempts (
    upload_attempt_id INTEGER PRIMARY KEY,
    user_key INTEGER,
    device_key INTEGER,
    status TEXT, -- 'success', 'failure'
    failure_reason TEXT,
    timestamp_event TEXT
);

DROP TABLE IF EXISTS dim_devices;
CREATE TABLE dim_devices (
    device_key INTEGER PRIMARY KEY,
    device_model TEXT,
    os_type TEXT, -- 'iOS', 'Android', 'Web'
    app_version TEXT
);

INSERT INTO dim_devices (device_key, device_model, os_type, app_version) VALUES
(1, 'iPhone 13', 'iOS', '1.2.0'),
(2, 'Samsung Galaxy S21', 'Android', '1.2.1'),
(3, 'iPhone 12', 'iOS', '1.1.5'),
(4, 'Google Pixel 6', 'Android', '1.2.0'),
(5, 'Web Browser', 'Web', 'N/A');

INSERT INTO fact_upload_attempts (upload_attempt_id, user_key, device_key, status, failure_reason, timestamp_event) VALUES
(1, 101, 1, 'success', NULL, '2023-03-01 10:00:00'),
(2, 102, 2, 'success', NULL, '2023-03-01 10:05:00'),
(3, 101, 1, 'failure', 'network_timeout', '2023-03-01 10:10:00'),
(4, 103, 3, 'success', NULL, '2023-03-01 10:15:00'),
(5, 104, 4, 'success', NULL, '2023-03-01 10:20:00'),
(6, 102, 2, 'failure', 'server_error', '2023-03-01 10:25:00'),
(7, 105, 5, 'success', NULL, '2023-03-01 10:30:00'),
(8, 101, 1, 'success', NULL, '2023-03-01 10:35:00'),
(9, 104, 4, 'failure', 'file_too_large', '2023-03-01 10:40:00'),
(10, 102, 2, 'success', NULL, '2023-03-01 10:45:00');

-- Expected output for the sample data:
-- os_type | total_attempts | successful_attempts | success_rate_percentage
-- --------|----------------|---------------------|-------------------------
-- Android | 4              | 2                   | 50.0
-- iOS     | 4              | 3                   | 75.0
-- Web     | 1              | 1                   | 100.0
-- (Assuming the 10th record for Android makes its success 2/4=50%, and iOS 3/4=75% if 8th record is iOS success)
-- Corrected counts from sample:
-- Android: Attempts: (2,Galaxy S21), (6,Galaxy S21), (10,Galaxy S21), (5,Pixel 6), (9,Pixel 6) -- Wait, device_key 2 & 4 are Android
--   Device 2 (Samsung Galaxy S21): 3 attempts (1 success, 1 failure, 1 success) -> 2/3 success
--   Device 4 (Google Pixel 6): 2 attempts (1 success, 1 failure) -> 1/2 success
-- Total Android: 5 attempts. Successful: 2 (from S21) + 1 (from Pixel 6) = 3.
--   Success rate Android: 3/5 = 60.0%

-- iOS: Attempts: (1,iPhone 13), (3,iPhone 13), (4,iPhone 12), (8,iPhone 13) -- device_key 1 & 3 are iOS
--   Device 1 (iPhone 13): 3 attempts (1 success, 1 failure, 1 success) -> 2/3 success
--   Device 3 (iPhone 12): 1 attempt (1 success) -> 1/1 success
-- Total iOS: 4 attempts. Successful: 2 (from D1) + 1 (from D3) = 3.
--   Success rate iOS: 3/4 = 75.0%

-- Web: Device 5: 1 attempt (1 success) -> 1/1 success. Success rate: 100.0%

-- Expected Output (Recalculated based on sample data logic):
-- os_type | total_attempts | successful_attempts | success_rate_percentage
-- --------|----------------|---------------------|-------------------------
-- Android | 5              | 3                   | 60.0
-- iOS     | 4              | 3                   | 75.0
-- Web     | 1              | 1                   | 100.0
*/ 