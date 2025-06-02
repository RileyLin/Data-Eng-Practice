/*
Question 2.3.2: Creator Performance Trends

Write a SQL query to analyze creator performance trends including follower growth,
engagement rates, and content frequency to identify top-performing creators.

Schema Reference:
- dim_users: user_key, user_id, creator_tier, follower_count
- fact_content_engagements: content_key, user_key, engagement_timestamp
- dim_content: content_key, creator_user_key, upload_timestamp

Expected Output:
Creator performance analysis with growth metrics and engagement trends.
*/

-- Write your SQL query here: 