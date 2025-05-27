# SQL Questions

This document contains SQL questions from the study guide, organized by scenario.

## Scenario 1: Ride Sharing (Uber/Lyft) - Carpooling Feature

### Question 1.3.1: Carpool Segment Percentage

**Description:**  
Write a SQL query to calculate the percentage of ride segments that belong to a 'Carpool' ride type. Assume fact_ride_segments links to fact_rides, and fact_rides links to dim_ride_type.

**Schema:**
```
fact_ride_segments:
- ride_segment_id (PK)
- ride_id (FK -> fact_rides)
- rider_user_key
- ...

fact_rides:
- ride_id (PK)
- ride_type_key (FK -> dim_ride_type)
- driver_user_key
- ...

dim_ride_type:
- ride_type_key (PK)
- ride_type_name ('Carpool', 'Regular', etc.)
- ...
```

**Expected Output:**  
The query should return a single row with a percentage value showing what proportion of all ride segments (from fact_ride_segments) belong to 'Carpool' rides.

**Solution Summary:**
The query joins `fact_ride_segments` with `fact_rides` and `dim_ride_type`. It then calculates the percentage by dividing the count of segments belonging to 'Carpool' rides by the total count of all segments, multiplying by 100.0. `NULLIF` is used to prevent division by zero.
*See `solutions/sql/q001_carpool_segment_percentage.sql` for the full query and explanation.*

### Question 1.3.2: Drivers Preferring Carpool

**Description:**  
Calculate the percentage of distinct drivers who complete more carpool rides than regular (non-carpool) rides in a given period (e.g., last 30 days).

**Solution Summary:**
The query uses CTEs to:
1.  Count carpool and regular rides per driver in the last 30 days (`DriverRideCounts`).
2.  Count total distinct drivers active in the period (`TotalDistinctDriversInPeriod`).
3.  Count drivers who had more carpool rides than regular rides (`DriversPreferringCarpool`).
The final percentage is `(DriversPreferringCarpool / TotalDistinctDriversInPeriod) * 100`.
*See `solutions/sql/q005_drivers_preferring_carpool.sql` for the full query and explanation.*

## Scenario 2: Short Video (TikTok/Reels) - Sharing Focus

### Question 2.3.1: Posts with Zero Engagement on Creation Day

**Description:**  
Write a SQL query to find post_ids for posts that received zero 'like' or 'react' events on the same calendar day they were created.

**Solution Summary:**
The query selects `post_id` from a `posts` table where no corresponding 'like' or 'react' event exists in an `engagement_events` table for the same `post_id` and on the same calendar day as the post's creation. This is typically done using a `NOT EXISTS` clause or a `LEFT JOIN` checking for `NULL`.
*See `solutions/sql/q002_posts_zero_engagement.sql` for the full query and explanation.*

### Question 2.3.2: Posts with Reactions but No Comments

**Description:**  
Calculate the percentage of content items (e.g., posts, videos) created today that received at least one 'reaction' event but zero 'comment' events on the same day.

**Solution Summary:**
The query uses CTEs to:
1.  Identify posts created today (`PostsCreatedToday`).
2.  Identify posts created today that received reactions today (`ReactionsToday`).
3.  Identify posts created today that received comments today (`CommentsToday`).
4.  Find eligible posts by selecting from `ReactionsToday` and ensuring they are not in `CommentsToday` (via `LEFT JOIN ... WHERE IS NULL`).
The final percentage is (`COUNT(EligiblePosts)` / `COUNT(PostsCreatedToday)`) * 100.
*See `solutions/sql/q006_posts_reactions_no_comments.sql` for the full query and explanation.*

## Scenario 3: Streaming Platform (Netflix/Hulu)

### Question 3.3.1: User Cumulative Snapshot Update

**Description:**  
Describe the logic and write/outline SQL for a batch process to update a user_cumulative_snapshot table (with total view time) using data from the daily fact_viewing_sessions. Address how to avoid scanning the full fact table for the daily delta and optimize the update.

**Solution Summary:**
The logic involves:
1.  Aggregating daily view time per user from `fact_viewing_sessions` for the specific processing date (e.g., yesterday).
2.  Using this daily summary to update `user_cumulative_snapshot`.
3.  For existing users in the snapshot, their `total_view_time_seconds` is incremented. For new users, a new row is inserted.
This is achieved efficiently using `MERGE` (if available) or `INSERT ... ON CONFLICT DO UPDATE` to avoid full table scans and process only the daily delta. Indexing on user IDs and dates is crucial.
*See `solutions/sql/q007_user_cumulative_snapshot.sql` for the detailed logic and SQL outline.*

### Question 3.3.2: Content Aggregation

**Description:**  
Given a watch_fact table (content_id, user_id, total_watch_time_seconds, date_key), write a query to get the distinct user count and sum of total watch time per content_id for a specific date.

**Solution Summary:**
The query filters the `watch_fact` table for a specific `date_key`. It then groups the results by `content_id` and uses `COUNT(DISTINCT user_id)` to get the unique user count and `SUM(total_watch_time_seconds)` for the total watch time for each content item on that day.
*See `solutions/sql/q008_content_aggregation.sql` for the full query and explanation.*

## Scenario 4: Cloud File Storage (Dropbox/Google Drive)

### Question 4.3.1: Top Collaborative Files

**Description:**  
Write a SQL query to find the top 10 files with the most unique users who performed any action on them in the last 7 days.

**Solution Summary:**
The query filters `file_actions` for the last 7 days. It then groups by `file_id` and counts the `DISTINCT user_id` for each file. The results are ordered by this count in descending order, and `LIMIT 10` is used to get the top 10 files.
*See `solutions/sql/q009_top_collaborative_files.sql` for the full query and explanation.*

## Scenario 5: DAU/MAU Analysis

### Question 5.3.1: DAU Over MAU Ratio

**Description:**  
Write a SQL query to calculate the DAU/MAU ratio (stickiness) for each of the last 30 days, showing the trend over time.

**Solution Summary:**
The query involves:
1.  Generating a series of dates for the last 30 days (`date_series`).
2.  Calculating Daily Active Users (DAU) for each date.
3.  Calculating a rolling 30-day Monthly Active Users (MAU) ending on each date in the series.
4.  Joining these results and computing `DAU / MAU` for each day, ordered by date to show the trend.
*See `solutions/sql/q003_dau_mau_ratio.sql` for the full query and explanation.*

## Scenario 6: News Feed

### Question 6.3.1: Valid Post Reads

**Description:**  
Write a SQL query to count the number of valid post reads per user for the last 7 days. A valid read is defined as either:
1. The post was viewed for at least 5 seconds
2. The post reached at least 80% visibility on screen

**Solution Summary:**
The query first identifies relevant feed events (e.g., views, impressions with metrics) in the last 7 days. Then, for each user and content item, it checks if any of these events meet the valid read criteria (view time >= 5s OR visibility >= 80%). Finally, it counts the number of distinct validly read content items per user.
*See `solutions/sql/q010_valid_post_reads.sql` for the full query and explanation.*

## Scenario 7: Photo Upload (Instagram-like)

### Question 7.3.1: Upload Success Rate by Device

**Description:**  
Write a SQL query to calculate the upload success rate by device type for the past 30 days. Include the total number of attempts and successful uploads in the result.

**Solution Summary:**
The query joins `photo_uploads` with `devices` and filters for uploads in the past 30 days. It then groups by `device_type` and calculates total attempts, successful uploads (`status = 'success'`), and the success rate percentage `(successful_uploads * 100.0 / total_attempts)`.
*See `solutions/sql/q004_upload_success_by_device.sql` for the full query and explanation.*

## Scenario 8: FB Messenger

### Question 8.3.1: User Message Activity

**Description:**  
Write a SQL query to find the top 5 user_ids who sent the most messages in the last 30 days, along with their message count and the percentage of the total messages they represent.

**Solution Summary:**
The query uses CTEs to:
1.  Count messages sent per user in the last 30 days (`UserMessageCounts`).
2.  Calculate the total messages sent in the period by all users (`TotalMessagesInPeriod`).
It then selects the top 5 users by message count, their count, and their message count as a percentage of the total messages.
*See `solutions/sql/q011_user_message_activity.sql` for the full query and explanation.*

## Scenario 9: Food Delivery (DoorDash) - Order Batching

### Question 9.3.1: Batched vs. Single Orders

**Description:**  
Write a SQL query to compare the average delivery time (order_delivered_timestamp - order_placed_timestamp) for batched orders versus single orders over the past 90 days. Include the percentage difference.

**Solution Summary:**
The query calculates delivery times for orders in the last 90 days. It then computes the average delivery time separately for batched and single orders. Finally, it presents these averages and the percentage difference: `((avg_batched - avg_single) / avg_single) * 100`.
*See `solutions/sql/q012_batched_vs_single_orders.sql` for the full query and explanation.*

### Question 9.3.2: Driver Earnings Comparison

**Description:**  
Write a SQL query to calculate, for each driver, the average earnings per hour when handling batched orders versus single orders over the past 90 days. Include only drivers who have completed at least 10 of each order type. 

**Solution Summary:**
The query identifies drivers who completed >=10 batched and >=10 single orders in the last 90 days. For these drivers, it calculates total earnings and total duration (delivery time) for batched orders and single orders separately. It then computes average hourly earnings for each type (`total_earnings / total_hours`). A key challenge is accurately defining "time spent" for batched orders; the solution uses individual order durations as a proxy, noting that batch-level timing would be more accurate.
*See `solutions/sql/q013_driver_earnings_comparison.sql` for the full query and explanation.* 