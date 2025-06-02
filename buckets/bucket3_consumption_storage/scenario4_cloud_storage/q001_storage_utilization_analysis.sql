/*
Question 4.3.1: Storage Utilization and Growth Analysis

Write a SQL query to analyze user storage patterns including utilization rates,
file type distribution, and storage growth trends by user tier.

Schema Reference:
- dim_users: user_key, account_type, storage_quota_bytes, current_storage_used_bytes
- fact_file_activity: activity_key, file_key, user_key, activity_timestamp, activity_type
- dim_files_folders: file_key, file_size_bytes, file_type, creation_timestamp

Expected Output:
Storage utilization metrics and growth patterns by user segment and file type.
*/

-- Write your SQL query here: 