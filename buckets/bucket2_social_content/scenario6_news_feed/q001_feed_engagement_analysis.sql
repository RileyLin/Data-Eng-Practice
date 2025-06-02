/*
Question 6.3.1: News Feed Engagement Analysis

Write a SQL query to analyze user engagement with news feed posts,
including click-through rates, time spent, and interaction patterns.

Schema Reference:
- dim_posts: post_key, post_id, content_type, source_key, creation_timestamp
- fact_feed_events: post_key, user_key, event_type, view_time_ms, position_in_feed
- dim_content_sources: source_key, source_type, category

Expected Output:
Feed engagement metrics by content type and source with performance rankings.
*/

-- Write your SQL query here: 