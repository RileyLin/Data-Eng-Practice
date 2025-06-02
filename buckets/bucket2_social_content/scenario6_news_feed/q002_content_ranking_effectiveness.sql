/*
Question 6.3.2: Content Ranking Effectiveness

Write a SQL query to evaluate the effectiveness of content ranking algorithms
by analyzing engagement rates by feed position and optimizing for user satisfaction.

Schema Reference:
- fact_feed_events: post_key, user_key, position_in_feed, engagement_type, event_timestamp
- dim_engagement_types: engagement_type, engagement_weight, is_positive_signal
- dim_posts: post_key, is_sponsored, content_category

Expected Output:
Content ranking performance analysis showing position bias and engagement optimization opportunities.
*/

-- Write your SQL query here: 