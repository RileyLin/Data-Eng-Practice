/*
Question 3.3.1: Content Popularity and Engagement Analysis

Write a SQL query to analyze content popularity trends including view counts,
completion rates, and user ratings across different content categories.

Schema Reference:
- dim_content: content_key, title, content_type, duration_seconds, release_year
- fact_viewing_sessions: session_key, content_key, user_key, view_duration_seconds, completion_percentage
- fact_user_ratings: rating_key, content_key, user_key, rating_value

Expected Output:
Content performance rankings with engagement metrics and popularity trends.
*/

-- Write your SQL query here: 