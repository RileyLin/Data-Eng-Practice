/*
Question 3.3.2: User Viewing Patterns and Binge Behavior

Write a SQL query to analyze user viewing behaviors including binge-watching patterns,
session lengths, and content discovery methods.

Schema Reference:
- fact_viewing_sessions: session_key, user_key, content_key, session_start_timestamp, view_duration_seconds
- dim_users: user_key, subscription_tier, preferred_language, account_created_date
- dim_content: content_key, content_type, series_id, episode_number

Expected Output:
User engagement patterns and binge-watching behavior analysis by user segment.
*/

-- Write your SQL query here: 