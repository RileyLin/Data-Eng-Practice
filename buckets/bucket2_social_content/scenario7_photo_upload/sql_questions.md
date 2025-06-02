# Scenario 7: Photo Upload (Instagram/Snapchat) - SQL Questions

## Database Schema Reference

Based on the Photo Upload data model:

### Dimension Tables
-   **`dim_users`**: `user_key`, `user_id`, `registration_date`, `user_segment`, `region`
-   **`dim_devices`**: `device_key`, `device_id`, `device_model`, `os_version`, `app_version`, `network_type`
-   **`dim_image_attributes`**: `image_attributes_key`, `original_width_px`, `original_height_px`, `original_size_bytes`, `original_format`, `uploaded_width_px`, `uploaded_height_px`, `uploaded_size_bytes`, `uploaded_format`, `has_hdr`, `color_profile`, `exif_data`
-   **`dim_edit_actions`**: `edit_action_key`, `action_name`, `action_category`
-   **`dim_upload_status`**: `upload_status_key`, `status_code`, `status_description`, `is_successful`, `is_terminal_failure`, `failure_category`
-   **`dim_date`**: `date_key`, `full_date`, `hour`, `minute`

### Fact Tables
-   **`fact_photo_uploads`**: `upload_attempt_key`, `upload_session_id`, `user_key`, `device_key`, `image_attributes_key`, `date_key`, `upload_start_timestamp`, `upload_end_timestamp`, `duration_ms`, `final_upload_status_key`, `retry_count`, `used_background_upload`, `source_application`
-   **`fact_upload_editing_steps`**: `upload_attempt_key`, `edit_action_key`, `sequence_order`, `action_timestamp`, `action_parameters`
-   **`fact_upload_progress_events`**: `event_key`, `upload_attempt_key`, `event_timestamp`, `event_name`, `bytes_transferred`, `current_progress_pct`, `event_metadata`

---

## Question 1: Upload Success Rate by Device and Network

**Problem**: Analyze photo upload success rates, segmenting by device model, OS version, app version, and network type to identify problematic combinations.

**Expected Output**: Device model, OS version, app version, network type, total attempts, successful uploads, success rate.

### Solution (Adapted from `src/sql/q004_upload_success_by_device.sql`):
```sql
SELECT 
    dd.device_model,
    dd.os_version,
    dd.app_version,
    dd.network_type,
    COUNT(fpu.upload_attempt_key) as total_upload_attempts,
    SUM(CASE WHEN dus.is_successful THEN 1 ELSE 0 END) as successful_uploads,
    ROUND(SUM(CASE WHEN dus.is_successful THEN 1 ELSE 0 END) * 100.0 / COUNT(fpu.upload_attempt_key), 2) as success_rate_pct
FROM fact_photo_uploads fpu
JOIN dim_devices dd ON fpu.device_key = dd.device_key
JOIN dim_upload_status dus ON fpu.final_upload_status_key = dus.upload_status_key
JOIN dim_date d_date ON fpu.date_key = d_date.date_key
WHERE d_date.full_date >= CURRENT_DATE - 30 -- Analyze last 30 days
GROUP BY 
    dd.device_model,
    dd.os_version,
    dd.app_version,
    dd.network_type
HAVING COUNT(fpu.upload_attempt_key) > 50 -- Only include segments with significant attempt volume
ORDER BY success_rate_pct ASC, total_upload_attempts DESC
LIMIT 200;
```

---

## Question 2: Impact of Image Attributes on Upload Performance

**Problem**: Investigate how original image attributes (size, format, dimensions) affect upload duration and success rates.

**Expected Output**: Image size bucket, format, average duration, success rate.

### Solution:
```sql
SELECT 
    CASE 
        WHEN dia.original_size_bytes < 1024*1024 THEN 'Under 1MB'
        WHEN dia.original_size_bytes BETWEEN 1024*1024 AND 5*1024*1024-1 THEN '1-5MB'
        WHEN dia.original_size_bytes BETWEEN 5*1024*1024 AND 10*1024*1024-1 THEN '5-10MB'
        ELSE 'Over 10MB'
    END as image_size_bucket,
    dia.original_format,
    COUNT(fpu.upload_attempt_key) as total_attempts,
    ROUND(AVG(fpu.duration_ms) / 1000.0, 2) as avg_upload_duration_seconds,
    SUM(CASE WHEN dus.is_successful THEN 1 ELSE 0 END) as successful_uploads,
    ROUND(SUM(CASE WHEN dus.is_successful THEN 1 ELSE 0 END) * 100.0 / COUNT(fpu.upload_attempt_key), 2) as success_rate_pct,
    ROUND(AVG(CASE WHEN dus.is_successful THEN fpu.duration_ms ELSE NULL END)/1000.0, 2) as avg_successful_upload_duration_seconds
FROM fact_photo_uploads fpu
JOIN dim_image_attributes dia ON fpu.image_attributes_key = dia.image_attributes_key
JOIN dim_upload_status dus ON fpu.final_upload_status_key = dus.upload_status_key
JOIN dim_date d_date ON fpu.date_key = d_date.date_key
WHERE d_date.full_date >= CURRENT_DATE - 30
GROUP BY image_size_bucket, dia.original_format
HAVING COUNT(fpu.upload_attempt_key) > 100
ORDER BY image_size_bucket, success_rate_pct ASC;
```

---

## Question 3: Editing Tool Adoption and Its Correlation with Upload Time/Success

**Problem**: Analyze the adoption of different editing actions (filters, adjustments) and see if using more editing steps correlates with longer upload times or different success rates.

**Expected Output**: Edit action name, usage count, average number of edits per upload session where this action was used, average total upload duration for these sessions, success rate for these sessions.

### Solution:
```sql
WITH upload_edit_summary AS (
    SELECT 
        fpu.upload_attempt_key,
        fpu.duration_ms as total_upload_duration_ms,
        dus.is_successful as upload_is_successful,
        dea.action_name,
        COUNT(fues.edit_action_key) OVER (PARTITION BY fpu.upload_attempt_key) as total_edits_in_session
    FROM fact_photo_uploads fpu
    JOIN fact_upload_editing_steps fues ON fpu.upload_attempt_key = fues.upload_attempt_key
    JOIN dim_edit_actions dea ON fues.edit_action_key = dea.edit_action_key
    JOIN dim_upload_status dus ON fpu.final_upload_status_key = dus.upload_status_key
    JOIN dim_date d_date ON fpu.date_key = d_date.date_key
    WHERE d_date.full_date >= CURRENT_DATE - 30
)
SELECT 
    action_name,
    COUNT(DISTINCT upload_attempt_key) as sessions_using_action, -- Number of unique upload sessions that used this action
    ROUND(AVG(total_edits_in_session), 1) as avg_total_edits_when_action_used,
    ROUND(AVG(total_upload_duration_ms) / 1000.0, 2) as avg_session_duration_seconds,
    ROUND(SUM(CASE WHEN upload_is_successful THEN 1 ELSE 0 END) * 100.0 / COUNT(DISTINCT upload_attempt_key), 2) as session_success_rate_pct
FROM upload_edit_summary
GROUP BY action_name
ORDER BY sessions_using_action DESC;

-- Overall correlation between number of edits and performance
SELECT 
    CASE 
        WHEN edit_counts.num_edits = 0 THEN '0 edits'
        WHEN edit_counts.num_edits BETWEEN 1 AND 3 THEN '1-3 edits'
        WHEN edit_counts.num_edits BETWEEN 4 AND 6 THEN '4-6 edits'
        ELSE '7+ edits'
    END as number_of_edits_bucket,
    COUNT(DISTINCT fpu.upload_attempt_key) as total_upload_sessions,
    ROUND(AVG(fpu.duration_ms)/1000.0,2) as avg_total_duration_seconds,
    ROUND(SUM(CASE WHEN dus.is_successful THEN 1 ELSE 0 END) * 100.0 / COUNT(DISTINCT fpu.upload_attempt_key), 2) as success_rate_pct
FROM fact_photo_uploads fpu
LEFT JOIN (
    SELECT upload_attempt_key, COUNT(edit_action_key) as num_edits 
    FROM fact_upload_editing_steps 
    GROUP BY upload_attempt_key
) edit_counts ON fpu.upload_attempt_key = edit_counts.upload_attempt_key
JOIN dim_upload_status dus ON fpu.final_upload_status_key = dus.upload_status_key
JOIN dim_date d_date ON fpu.date_key = d_date.date_key
WHERE d_date.full_date >= CURRENT_DATE - 30
GROUP BY number_of_edits_bucket
ORDER BY number_of_edits_bucket;
```

---

## Question 4: Upload Funnel Analysis - Identifying Drop-off Points

**Problem**: Analyze the photo upload funnel using progress events to identify where users or the system experience the most failures or delays.

**Expected Output**: Event name (funnel stage), total attempts reaching this stage, success rate from this stage, average time to next significant stage.

### Solution:
```sql
WITH ranked_progress_events AS (
    SELECT 
        upload_attempt_key,
        event_name,
        event_timestamp,
        LEAD(event_name, 1) OVER (PARTITION BY upload_attempt_key ORDER BY event_timestamp) as next_event_name,
        LEAD(event_timestamp, 1) OVER (PARTITION BY upload_attempt_key ORDER BY event_timestamp) as next_event_timestamp
    FROM fact_upload_progress_events
    WHERE upload_attempt_key IN (SELECT upload_attempt_key FROM fact_photo_uploads WHERE date_key >= (SELECT date_key FROM dim_date WHERE full_date = CURRENT_DATE - 7))
),
funnel_stage_summary AS (
    SELECT 
        event_name as current_stage,
        COUNT(DISTINCT rpe.upload_attempt_key) as attempts_reaching_stage,
        COUNT(DISTINCT CASE WHEN dus.is_successful THEN rpe.upload_attempt_key ELSE NULL END) as successful_uploads_from_stage,
        AVG(EXTRACT(EPOCH FROM (next_event_timestamp - event_timestamp))) as avg_time_to_next_stage_seconds
    FROM ranked_progress_events rpe
    JOIN fact_photo_uploads fpu ON rpe.upload_attempt_key = fpu.upload_attempt_key
    JOIN dim_upload_status dus ON fpu.final_upload_status_key = dus.upload_status_key
    -- Define significant stages for time to next event analysis or filter specific event_name for cleaner output
    WHERE rpe.event_name IN ('upload_initiated', 'transcoding_started', 'server_processing_started', 'post_created') 
      AND (rpe.next_event_name IN ('transcoding_started', 'server_processing_started', 'post_created') OR rpe.next_event_name IS NULL)
    GROUP BY event_name
)
SELECT 
    current_stage,
    attempts_reaching_stage,
    ROUND(successful_uploads_from_stage * 100.0 / attempts_reaching_stage, 2) as success_rate_from_this_stage_pct,
    ROUND(avg_time_to_next_stage_seconds, 2) as avg_time_to_next_stage_seconds
FROM funnel_stage_summary
ORDER BY 
    CASE current_stage 
        WHEN 'upload_initiated' THEN 1 
        WHEN 'transcoding_started' THEN 2 
        WHEN 'server_processing_started' THEN 3 
        WHEN 'post_created' THEN 4 
        ELSE 5 
    END;
```

---

## Question 5: Retry Behavior Analysis

**Problem**: Understand how retry attempts affect upload success and duration. Are retries generally successful? Do they significantly prolong the process?

**Expected Output**: Retry count bucket, total attempts in bucket, success rate for this bucket, average total duration for attempts in bucket.

### Solution:
```sql
SELECT 
    CASE 
        WHEN fpu.retry_count = 0 THEN '0 Retries'
        WHEN fpu.retry_count = 1 THEN '1 Retry'
        WHEN fpu.retry_count = 2 THEN '2 Retries'
        ELSE '3+ Retries'
    END as retry_count_bucket,
    COUNT(fpu.upload_attempt_key) as total_attempts,
    SUM(CASE WHEN dus.is_successful THEN 1 ELSE 0 END) as successful_uploads,
    ROUND(SUM(CASE WHEN dus.is_successful THEN 1 ELSE 0 END) * 100.0 / COUNT(fpu.upload_attempt_key), 2) as success_rate_pct,
    ROUND(AVG(fpu.duration_ms) / 1000.0, 2) as avg_total_duration_seconds,
    ROUND(AVG(CASE WHEN dus.is_successful THEN fpu.duration_ms ELSE NULL END) / 1000.0, 2) as avg_duration_for_successful_seconds
FROM fact_photo_uploads fpu
JOIN dim_upload_status dus ON fpu.final_upload_status_key = dus.upload_status_key
JOIN dim_date d_date ON fpu.date_key = d_date.date_key
WHERE d_date.full_date >= CURRENT_DATE - 30
GROUP BY retry_count_bucket
ORDER BY 
    CASE retry_count_bucket
        WHEN '0 Retries' THEN 0
        WHEN '1 Retry' THEN 1
        WHEN '2 Retries' THEN 2
        ELSE 3
    END;
```

---

## Question 6: Analysis of Uploads from Different Sources (In-App Camera vs. Gallery)

**Problem**: Compare the characteristics and success rates of uploads originating from the in-app camera versus those selected from the device gallery or shared from external apps.

**Expected Output**: Source application, total uploads, success rate, average original image size, average number of edit steps.

### Solution:
```sql
SELECT 
    fpu.source_application,
    COUNT(fpu.upload_attempt_key) as total_uploads,
    ROUND(SUM(CASE WHEN dus.is_successful THEN 1 ELSE 0 END) * 100.0 / COUNT(fpu.upload_attempt_key), 2) as success_rate_pct,
    ROUND(AVG(dia.original_size_bytes) / (1024.0*1024.0), 2) as avg_original_image_size_mb,
    ROUND(AVG(fpu.duration_ms)/1000.0, 2) as avg_upload_duration_seconds,
    COALESCE(ROUND(AVG(edit_counts.num_edits),1), 0) as avg_edit_steps_per_upload
FROM fact_photo_uploads fpu
JOIN dim_upload_status dus ON fpu.final_upload_status_key = dus.upload_status_key
JOIN dim_image_attributes dia ON fpu.image_attributes_key = dia.image_attributes_key
LEFT JOIN (
    SELECT upload_attempt_key, COUNT(edit_action_key) as num_edits 
    FROM fact_upload_editing_steps 
    GROUP BY upload_attempt_key
) edit_counts ON fpu.upload_attempt_key = edit_counts.upload_attempt_key
JOIN dim_date d_date ON fpu.date_key = d_date.date_key
WHERE d_date.full_date >= CURRENT_DATE - 30
GROUP BY fpu.source_application
ORDER BY total_uploads DESC;
``` 