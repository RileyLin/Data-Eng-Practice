/*
Solution to Question 7.3.1: Upload Success Rate by Device

Write a SQL query to calculate the upload success rate by device type for the past 30 days.
Include the total number of attempts and successful uploads in the result.
*/

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

This query calculates the success rate of photo uploads grouped by device type. Here's a detailed breakdown:

1. Table joins:
   - We start with the photo_uploads table (p) which contains individual upload attempts
   - We join with the devices table (d) using device_id to get the device_type information

2. Time filtering:
   - The WHERE clause limits results to uploads that started in the last 30 days
   - This creates a rolling 30-day window for analysis

3. Metrics calculation:
   - total_attempts: Simple COUNT of upload_id, giving us the total number of attempts per device type
   - successful_uploads: SUM with a CASE statement that counts only when is_success = true
   - success_rate: Division of successful_uploads by total_attempts, converted to percentage

4. Key technical aspects:
   - Using NULLIF to prevent division by zero (in case there are no attempts for a device type)
   - Cast to decimal (::decimal) to ensure proper floating-point division rather than integer division
   - ROUND to 2 decimal places for readability
   - GROUP BY device_type to get aggregates per device category

5. Sorting:
   - Primary sort by success_rate DESC (highest success rate first)
   - Secondary sort by total_attempts DESC (for tied success rates, show devices with more data first)

This query provides valuable insights for:
- Identifying problematic device types with lower success rates
- Prioritizing engineering efforts to improve upload reliability on specific devices
- Monitoring the impact of app updates or infrastructure changes on upload success

Alternative implementation for databases that don't support NULLIF:

SELECT 
    d.device_type,
    COUNT(p.upload_id) AS total_attempts,
    SUM(CASE WHEN p.is_success = true THEN 1 ELSE 0 END) AS successful_uploads,
    ROUND(
        CASE 
            WHEN COUNT(p.upload_id) = 0 THEN 0
            ELSE SUM(CASE WHEN p.is_success = true THEN 1 ELSE 0 END)::decimal / 
                 COUNT(p.upload_id) * 100
        END, 
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
*/ 