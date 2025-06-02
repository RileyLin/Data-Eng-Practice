/*
Question 4.3.2: File Sharing and Collaboration Analysis

Write a SQL query to analyze file sharing patterns and collaboration effectiveness
including share rates, collaboration intensity, and team productivity metrics.

Schema Reference:
- fact_sharing_collaboration: share_id, file_key, shared_by_user_key, shared_with_user_key, permission_level
- fact_file_activity: activity_key, file_key, user_key, activity_type, activity_timestamp
- dim_files_folders: file_key, owner_user_key, file_type, is_shared

Expected Output:
Collaboration patterns and sharing effectiveness metrics by file type and user behavior.
*/

-- Write your SQL query here: 