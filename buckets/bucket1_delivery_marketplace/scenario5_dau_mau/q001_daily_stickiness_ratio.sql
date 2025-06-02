/*
Question 5.3.1: Daily Stickiness Ratio (DAU/MAU)

Write a SQL query to calculate the DAU/MAU stickiness ratio for each day in the last 30 days.
Show the trend of user engagement over time.

Schema Reference:
- fact_user_activity: user_key, date_key, session_count, total_actions
- dim_users: user_key, user_id, registration_date, user_segment
- dim_date: date_key, full_date, year, month, day_of_month

Expected Output:
Daily stickiness ratios showing engagement trends over the past 30 days.
*/

-- Write your SQL query here: 