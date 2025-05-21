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

### Question 1.3.2: Drivers Preferring Carpool

**Description:**  
Calculate the percentage of distinct drivers who complete more carpool rides than regular (non-carpool) rides in a given period (e.g., last 30 days).

## Scenario 2: Short Video (TikTok/Reels) - Sharing Focus

### Question 2.3.1: Posts with Zero Engagement on Creation Day

**Description:**  
Write a SQL query to find post_ids for posts that received zero 'like' or 'react' events on the same calendar day they were created.

### Question 2.3.2: Posts with Reactions but No Comments

**Description:**  
Calculate the percentage of content items (e.g., posts, videos) created today that received at least one 'reaction' event but zero 'comment' events on the same day.

## Scenario 3: Streaming Platform (Netflix/Hulu)

### Question 3.3.1: User Cumulative Snapshot Update

**Description:**  
Describe the logic and write/outline SQL for a batch process to update a user_cumulative_snapshot table (with total view time) using data from the daily fact_viewing_sessions. Address how to avoid scanning the full fact table for the daily delta and optimize the update.

### Question 3.3.2: Content Aggregation

**Description:**  
Given a watch_fact table (content_id, user_id, total_watch_time_seconds, date_key), write a query to get the distinct user count and sum of total watch time per content_id for a specific date.

## Scenario 4: Cloud File Storage (Dropbox/Google Drive)

### Question 4.3.1: Top Collaborative Files

**Description:**  
Write a SQL query to find the top 10 files with the most unique users who performed any action on them in the last 7 days.

## Scenario 5: DAU/MAU Analysis

### Question 5.3.1: DAU Over MAU Ratio

**Description:**  
Write a SQL query to calculate the DAU/MAU ratio (stickiness) for each of the last 30 days, showing the trend over time.

## Scenario 6: News Feed

### Question 6.3.1: Valid Post Reads

**Description:**  
Write a SQL query to count the number of valid post reads per user for the last 7 days. A valid read is defined as either:
1. The post was viewed for at least 5 seconds
2. The post reached at least 80% visibility on screen

## Scenario 7: Photo Upload (Instagram-like)

### Question 7.3.1: Upload Success Rate by Device

**Description:**  
Write a SQL query to calculate the upload success rate by device type for the past 30 days. Include the total number of attempts and successful uploads in the result.

## Scenario 8: FB Messenger

### Question 8.3.1: User Message Activity

**Description:**  
Write a SQL query to find the top 5 user_ids who sent the most messages in the last 30 days, along with their message count and the percentage of the total messages they represent.

## Scenario 9: Food Delivery (DoorDash) - Order Batching

### Question 9.3.1: Batched vs. Single Orders

**Description:**  
Write a SQL query to compare the average delivery time (order_delivered_timestamp - order_placed_timestamp) for batched orders versus single orders over the past 90 days. Include the percentage difference.

### Question 9.3.2: Driver Earnings Comparison

**Description:**  
Write a SQL query to calculate, for each driver, the average earnings per hour when handling batched orders versus single orders over the past 90 days. Include only drivers who have completed at least 10 of each order type. 