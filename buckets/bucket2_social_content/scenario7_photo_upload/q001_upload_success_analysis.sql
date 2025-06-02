/*
Question 7.3.1: Photo Upload Success Analysis

Write a SQL query to analyze photo upload success rates by device type,
network connection, and file characteristics to identify improvement opportunities.

Schema Reference:
- fact_upload_attempts: upload_id, user_key, device_key, file_size_bytes, upload_status
- dim_devices: device_key, device_model, os_version, app_version
- dim_network_connections: network_key, network_type, connection_speed

Expected Output:
Upload success rates and failure patterns by device and network characteristics.
*/

-- Write your SQL query here: 