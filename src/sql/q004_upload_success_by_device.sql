/*
Question 7.3.1: Upload Success Rate by Device

Write a SQL query to calculate the upload success rate by device type for the past 30 days.
Include the total number of attempts and successful uploads in the result.

Schema based on setup_scripts/scenario_7_photo_upload_setup.sql:

fact_photo_uploads:
- upload_attempt_id (INTEGER PRIMARY KEY AUTOINCREMENT)
- photo_id (VARCHAR(50) UNIQUE)
- user_key (INTEGER, FK to dim_users_photo)
- device_key (INTEGER, FK to dim_devices_photo)
- app_version_key (INTEGER, FK to dim_app_versions_photo)
- upload_status_key (INTEGER, FK to dim_upload_status_photo)
- attempt_start_timestamp (TEXT NOT NULL, ISO 8601 format)
- attempt_end_timestamp (TEXT)
- upload_duration_ms (INTEGER)
- file_size_bytes (INTEGER)
- photo_width_px (INTEGER)
- photo_height_px (INTEGER)
- mime_type (TEXT)
- network_type (TEXT)
- failure_reason (TEXT)
- date_key (INTEGER, FK to dim_date)
- time_key (INTEGER, FK to dim_time)
- FOREIGN KEY (user_key) REFERENCES dim_users_photo(user_key)
- FOREIGN KEY (device_key) REFERENCES dim_devices_photo(device_key)
- FOREIGN KEY (app_version_key) REFERENCES dim_app_versions_photo(app_version_key)
- FOREIGN KEY (upload_status_key) REFERENCES dim_upload_status_photo(upload_status_key)
- FOREIGN KEY (date_key) REFERENCES dim_date(date_key)
- FOREIGN KEY (time_key) REFERENCES dim_time(time_key)

dim_devices_photo:
- device_key (INTEGER PRIMARY KEY AUTOINCREMENT)
- device_id (VARCHAR(50) UNIQUE NOT NULL)
- device_type (TEXT) -- 'Mobile', 'Tablet', 'Web'
- platform (TEXT) -- 'iOS', 'Android', 'Web'
- os_version (TEXT)

dim_upload_status_photo:
- upload_status_key (INTEGER PRIMARY KEY AUTOINCREMENT)
- status_name (TEXT UNIQUE NOT NULL)
- is_success (BOOLEAN NOT NULL)

Expected Output:
A result set with columns:
- device_type: The type of device (e.g., smartphone, tablet, desktop)
- total_attempts: Total number of upload attempts
- successful_uploads: Number of successful uploads
- success_rate: Percentage of successful uploads (0-100)
Ordered by success_rate in descending order
*/

-- Write your SQL query here:
SELECT 
    d.device_type,
    COUNT(p.upload_attempt_id) AS total_attempts,
    SUM(CASE WHEN dus.is_success = true THEN 1 ELSE 0 END) AS successful_uploads,
    ROUND(
        SUM(CASE WHEN dus.is_success = true THEN 1 ELSE 0 END)::decimal / 
        NULLIF(COUNT(p.upload_attempt_id), 0) * 100, 
        2
    ) AS success_rate
FROM 
    fact_photo_uploads p
JOIN 
    dim_devices_photo d ON p.device_key = d.device_key
JOIN
    dim_upload_status_photo dus ON p.upload_status_key = dus.upload_status_key
WHERE 
    p.attempt_start_timestamp >= CURRENT_DATE - INTERVAL '30 days'
GROUP BY 
    d.device_type
ORDER BY 
    success_rate DESC,
    total_attempts DESC;

/*
Explanation:

1. We join the fact_photo_uploads table with the dim_devices_photo table to get the device_type
   and with dim_upload_status_photo to get the is_success flag.

2. We filter for uploads that started in the last 30 days using the attempt_start_timestamp field.

3. We count the total number of upload attempts (upload_attempt_id) for each device_type.

4. For successful uploads, we use a CASE statement on dus.is_success to count only records where it's true.

5. To calculate the success rate, we:
   - Divide the number of successful uploads by the total attempts
   - Multiply by 100 to get a percentage
   - Convert to decimal type to ensure proper division (preventing integer division)
   - Use NULLIF to handle cases where there are no attempts (to avoid division by zero)
   - Round to 2 decimal places

6. We group by device_type to get metrics for each type of device.

7. We order by success_rate in descending order to see the most successful device types first,
   with a secondary sort on total_attempts to show higher-volume device types first in case of ties.

Alternative version for databases that don't support NULLIF:
   ROUND(
       CASE 
           WHEN COUNT(p.upload_attempt_id) = 0 THEN 0
           ELSE SUM(CASE WHEN dus.is_success = true THEN 1 ELSE 0 END)::decimal / 
                COUNT(p.upload_attempt_id) * 100
       END, 
       2
   ) AS success_rate
*/ 