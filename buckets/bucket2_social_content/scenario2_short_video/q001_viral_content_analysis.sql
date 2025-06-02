/*
Question 2.3.1: Viral Content Analysis

Write a SQL query to identify viral videos by analyzing engagement rates,
view completion rates, and sharing patterns across different content categories.

Schema Reference:
- dim_content: content_key, content_id, category, duration_seconds, upload_timestamp
- fact_content_engagements: content_key, user_key, engagement_type, watch_duration_seconds
- dim_engagement_type: engagement_type, engagement_weight

Expected Output:
Top viral content with engagement metrics and virality indicators.
*/

-- Write your SQL query here: 