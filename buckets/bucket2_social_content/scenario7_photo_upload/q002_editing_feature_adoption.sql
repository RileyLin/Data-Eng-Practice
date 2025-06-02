/*
Question 7.3.2: Photo Editing Feature Adoption

Write a SQL query to analyze adoption rates of photo editing features
and their impact on user engagement and content quality.

Schema Reference:
- fact_photo_edits: photo_key, user_key, edit_action_key, edit_timestamp
- dim_edit_actions: edit_action_key, action_name, action_category
- fact_photo_uploads: photo_key, upload_duration_ms, final_file_size

Expected Output:
Editing feature usage patterns and their correlation with upload success and user retention.
*/

-- Write your SQL query here: 