/*
Question 7.3.1: Upload Success Rate by Device

Write a SQL query to calculate the upload success rate by device type for the past 30 days.
Include the total number of attempts and successful uploads in the result.

Schema:
photo_uploads:
- upload_id (PK)
- user_id
- device_id (FK -> devices)
- start_timestamp
- end_timestamp
- is_success
- file_size_kb
- upload_duration_ms
- error_code
- error_message
- ...

devices:
- device_id (PK)
- device_type
- os_name
- os_version
- manufacturer
- model
- ...

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
    COUNT(p.upload_id) AS total_attempts,
    SUM(CASE WHEN p.is_success = true THEN 1 ELSE 0 END) AS successful_uploads,
    ROUND(
        SUM(CASE WHEN p.is_success = true THEN 1 ELSE 0 END)::decimal / 
        NULLIF(COUNT(p.upload_id), 0) * 100, 
        2
    ) AS success_rate
FROM 
    photo_uploads p
JOIN 
    devices d ON p.device_id = d.device_id
WHERE 
    p.start_timestamp >= CURRENT_DATE - INTERVAL '30 days'
GROUP BY 
    d.device_type
ORDER BY 
    success_rate DESC,
    total_attempts DESC;

/*
Explanation:

1. We join the photo_uploads table with the devices table to get the device_type
   for each upload attempt.

2. We filter for uploads that started in the last 30 days using the start_timestamp field.

3. We count the total number of upload attempts for each device_type.

4. For successful uploads, we use a CASE statement to count only records where is_success is true.

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
           WHEN COUNT(p.upload_id) = 0 THEN 0
           ELSE SUM(CASE WHEN p.is_success = true THEN 1 ELSE 0 END)::decimal / 
                COUNT(p.upload_id) * 100
       END, 
       2
   ) AS success_rate
*/ 