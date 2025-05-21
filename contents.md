Product Sense, SQL & Behavioral Interview Study Guide
This document contains product sense questions, data modeling challenges, SQL problems, and common behavioral questions based on typical onsite interview scenarios. Solutions, explanations, SQL queries, and data modeling details (including conceptual diagrams and UI sketches) are provided in the final section.

General Interview Notes:

Speed is Critical: Questions might be straightforward, but you need to work through them efficiently. Don't get stuck. Aim for max 8 minutes per SQL/Python question in initial screens.

Explain Your Thought Process: Clearly articulate your reasoning, assumptions, and trade-offs, especially in data modeling and product sense questions.

Hints are Okay: Interviewers often provide hints if you're stuck. Listen carefully and show you can incorporate feedback – this demonstrates learning ability, a key hiring signal.

Data Scale: Assume datasets are large (billions of records). Mentioning data partitioning (e.g., by date on fact tables) and optimizing dashboards by reading from pre-aggregated daily/hourly tables instead of raw fact tables can earn bonus points.

Follow-up Questions: Expect "why" and "how" follow-ups. Interviewers probe for depth and specific signals (ownership, impact, technical depth, collaboration). Be prepared to elaborate.

Bonus Questions: If you finish early, you might get an additional question, potentially including ML concepts depending on the role/interviewer.

SQL Fundamentals: Be solid on GROUP BY, HAVING, sub-queries, window functions (SUM() OVER, ROW_NUMBER(), etc.), CASE statements (e.g., SUM(CASE WHEN ...)), and self-joins.

Python Fundamentals: Master lists, strings, tuples, dictionaries, and common operations/methods.

Behavioral Questions (Example Themes & Signals)
Motivation & Role Understanding:

"What does data engineering / data science mean to you?"

"Tell me about a project where you used data to make an impact or convince others."

"How do you plan to succeed at Meta?"

Execution & Prioritization:

"How do you handle prioritizing competing tasks or projects? Describe your framework."

"Tell me about a time you led a project. What was the impact?"

Self-Awareness & Learning:

"Tell me about a time you were wrong or made a mistake. How did you handle it?"

(See Solutions section for example approaches)

Scenario 1: Ride Sharing (Uber/Lyft) - Carpooling Feature Focus
1a. Product Sense:

Value Proposition & Mission Alignment: "Why would Meta (or a similar large tech company) invest in a carpooling feature for its ride-sharing service? How does it align with Meta's mission (e.g., connecting people, building community)?"

Tracking Performance: "Imagine you launched the Carpool feature. How would you track its performance? What are the key metrics, and how would you slice the data?"

1b. Data Modeling:

Challenge: How should the data model be designed to support carpool rides where a single ride (ride_id) can involve multiple passengers picked up and dropped off at potentially different locations and times within the same driver's trip? Discuss trade-offs.

1c. SQL:

Question (Original): Write a SQL query to calculate the percentage of ride segments that belong to a 'Carpool' ride type. Assume fact_ride_segments links to fact_rides, and fact_rides links to dim_ride_type.

1d. Python: (Refer to Python File: can_complete_rides - consider discussing capacity constraints as a follow-up).

1e. SQL (New):

Question: Calculate the percentage of distinct drivers who complete more carpool rides than regular (non-carpool) rides in a given period.

Scenario 2: Short Video (TikTok/Reels) - Sharing Focus
2a. Product Sense:

Measuring Success (Original): "You are launching Reels/Shorts. What are the key metrics for platform health and user engagement?"

Visualization (Original): "Visualize Daily Active Users (DAU)."

New PS Question 1: "How would you track if a user significantly changes their 'regular' location (e.g., moves cities) based on their activity?"

New PS Question 2: "How would you compare the engagement (e.g., likes) of original content versus content that is shared (i.e., a re-share of an original post)? What insights would this provide?"

Product Analytics/Dashboarding Idea: "How would you design a dashboard visualization to show how the launch of Reels is affecting engagement with other platform features (e.g., standard posts, image uploads, long-form videos)?"

2b. Data Modeling:

Challenge: Design a data model for engagement events (like, comment, share, view) that can efficiently handle posts shared potentially thousands or millions of times, across multiple layers (User A shares Post P -> User B shares A's share -> User C shares B's share, etc.). The model must support efficiently counting total shares per original post and identifying the original poster and post time. Address potential interviewer hints about using arrays and explain the trade-offs.

2c. SQL (Original):

Question: Write a SQL query to find post_ids for posts that received zero 'like' or 'react' events on the same calendar day they were created.

2d. Python (Original Stream Processing): (Refer to Python File: process_event for session-based buffering)

2e. SQL (New):

Question: Calculate the percentage of content items (e.g., posts, videos) created today that received at least one 'reaction' event but zero 'comment' events on the same day.

2f. Python (New Stream Processing with Fixed Buffer): (Refer to Python File: process_fixed_buffer_stream)

Scenario 3: Streaming Platform (Netflix/Hulu)
3a. Product Sense:

Question: For a video streaming platform, what are the different types of user engagement you could track? Define key metrics at the Platform, User, and Video levels.

3b. Data Modeling: (Focus on fact_viewing_sessions as per original study guide context)

Challenge: Design the fact_viewing_sessions table. What are its key measures and foreign keys? How would you handle tracking view duration, pauses, and completion status?

3c. SQL (Snapshot Update):

Question: Describe the logic and write/outline SQL for a batch process to update a user_cumulative_snapshot table (with total view time) using data from the daily fact_viewing_sessions. Address how to avoid scanning the full fact table for the daily delta and optimize the update.

3d. SQL (New Content Aggregation):

Question: Given a watch_fact table (content_id, user_id, total_watch_time_seconds, date_key), write a query to get the distinct user count and sum of total watch time per content_id for a specific date.

3e. Python (New - Avg Rating per Movie): (Refer to Python File: calculate_average_movie_ratings)

3f. Python (Original - Avg Rating per Category): (Refer to Python File: calculate_average_ratings)

Scenario 4: Cloud File Storage (Dropbox/Google Drive)
(Content remains as per previous version, with Data Modeling, SQL, and Product Sense questions)
...

Scenario 5: DAU/MAU Analysis
(Content remains as per previous version, with Data Modeling, SQL, and Product Sense questions)
...

Scenario 6: News Feed
(Content remains as per previous version, with Data Modeling/Logging, SQL, and Product Sense questions)
...

Scenario 7: Photo Upload (Instagram-like)
(Content remains as per previous version, with Data Modeling, SQL, and Product Sense questions)
...

Scenario 8: FB Messenger
(Content remains as per previous version, with Data Modeling, SQL, and Product Sense questions)
...

Scenario 9: Food Delivery (DoorDash) - Order Batching
(Content remains as per previous version, with Data Modeling, SQL, and Product Sense questions)
...

Solutions & Explanations (Detailed)
Behavioral Questions (Example Approaches)
"What does data engineering / data science mean to you?"

Example Answer: "To me, data engineering is about building the foundational infrastructure and pipelines that make high-quality, reliable data accessible and usable for an organization. It's not just about moving data, but about understanding the business needs, designing robust data models, ensuring data integrity and governance, and optimizing for performance and scalability. A good data engineer empowers data scientists, analysts, and product teams to derive insights and make data-driven decisions efficiently. It's about creating a trustworthy data ecosystem that fuels innovation and impact."

Signals to Convey: Understanding of the data lifecycle, focus on reliability & quality, collaboration, impact-driven, technical depth.

"Tell me about a project where you used data to make an impact or convince others."

Example Answer (STAR Method):

Situation: "At my previous role in a ride-sharing company, we noticed that a significant number of users were dropping off during the new driver onboarding process, specifically at the document verification stage. This was impacting our driver supply."

Task: "My task was to analyze the onboarding funnel data to identify specific pain points in the document verification step and propose data-backed solutions to improve the completion rate."

Action: "I first queried our event logs and database using SQL to reconstruct the user journey through the onboarding funnel, calculating drop-off rates at each sub-step of document upload and verification. I found that users on Android devices had a 15% higher drop-off rate than iOS users during image upload for their driver's license. Digging deeper with segmented analysis, I noticed this correlated with higher error rates for image processing from certain Android OS versions. I also analyzed user feedback logs related to onboarding and found many complaints about unclear image quality requirements. I then worked with a UX designer to A/B test clearer instructions and improved image capture UI specifically for the problematic Android versions. I also proposed to the backend team to enhance server-side image validation to provide more specific error feedback to users."

Result: "The A/B test with clearer instructions and UI improvements led to a 10% increase in document submission success for the targeted Android users. After the backend changes were implemented, overall document rejection rates for first-time submissions decreased by 8%. This translated to an estimated increase of 500 successfully onboarded drivers per month, directly addressing the driver supply concern."

Signals to Convey: Problem identification, analytical skills (SQL, funnel analysis), data-driven hypothesis, collaboration (UX, backend), A/B testing understanding, quantifiable impact.

"How do you plan to succeed at Meta?"

Example Answer: "My plan to succeed at Meta revolves around three key areas. First, rapidly learning and mastering Meta's specific data infrastructure, tools, and best practices. I'm eager to dive into the scale and complexity here. Second, focusing on impact. I want to understand the core business objectives of my team and prioritize projects that directly contribute to those goals, always asking 'why' we are building something. Third, strong collaboration. I believe in working closely with product managers, data scientists, and other engineers to understand their needs, share knowledge, and build effective solutions together. I'm also committed to continuous learning and seeking feedback to grow and adapt within Meta's fast-paced environment."

Signals to Convey: Eagerness to learn, impact-driven, collaborative, understanding of Meta's culture (fast-paced, scale).

"How do you handle prioritizing competing tasks or projects? Describe your framework."

Example Answer: "When faced with competing tasks, I first ensure I have a clear understanding of each task's objectives, deadlines, and dependencies. My general framework involves assessing tasks based on two main dimensions: Impact (how much value does this deliver to the team/company goals?) and Urgency/Effort (how critical is the deadline, and how much work is involved?).

For quick daily prioritization, I often use a mental Eisenhower Matrix (Urgent/Important).

For larger projects, I'd discuss with my manager and stakeholders to get their input on business priority. I'd try to quantify the potential impact (e.g., time saved, revenue generated, risk mitigated) versus the estimated effort (time, resources).

I also consider dependencies – if Task A blocks multiple other important tasks, its effective urgency increases.

Communication is key. If I can't do everything, I proactively communicate my proposed priorities, the rationale, and any potential trade-offs or risks to my manager and stakeholders to ensure alignment and manage expectations. I use tools like Jira or a shared task list to keep track of progress and maintain transparency."

Signals to Convey: Structured thinking, strategic prioritization, communication, stakeholder management, proactiveness.

"Tell me about a time you led a project. What was the impact?"

Example Answer (STAR Method):

Situation: "Our analytics team was spending excessive time manually generating weekly performance reports for different regional sales teams. The process was error-prone and slow, often delaying insights."

Task: "I took the initiative to lead the development of an automated reporting pipeline and a self-serve dashboard to replace the manual process."

Action: "I started by gathering requirements from the sales operations manager and a few regional leads to understand their key metrics and desired report formats. Then, I designed the data model for the aggregated tables that would feed the dashboard, focusing on performance and query efficiency. I wrote the ETL scripts using Python and Airflow to pull data from various sources (CRM, transaction DBs), transform it, and load it into our data warehouse daily. I then built the dashboard using Tableau, incorporating filters for region, time period, and product category. I conducted UAT with the sales ops team and provided training documentation for the regional teams."

Result: "The automated pipeline reduced the time spent on weekly reporting from approximately 8 hours of manual work per week to virtually zero. The self-serve dashboard provided sales teams with real-time access to their performance data, leading to quicker identification of trends and a 15% improvement in response time to underperforming areas reported by regional leads in the first quarter after launch. The analytics team was also freed up to work on more strategic analyses."

Signals to Convey: Initiative, ownership, technical skills (ETL, data modeling, dashboarding), requirement gathering, stakeholder management, quantifiable impact, improving efficiency.

"Tell me about a time you were wrong or made a mistake. How did you handle it?"

Example Answer: "In a project to optimize a data pipeline, I made an assumption about the distribution of a key field in the input data without thoroughly validating it against a larger historical dataset. Based on this assumption, I chose a specific partitioning strategy for an intermediate table. During initial production runs with higher data volumes, we started seeing performance degradation and data skew in certain partitions, causing job delays.

Handling it: Once the issue was flagged, I immediately took ownership. My first step was to analyze the logs and query the production data to confirm the skew and understand the actual data distribution, which was different from my sample-based assumption. I communicated the issue and my incorrect assumption to my team lead and the affected stakeholders, explaining the impact. I then re-evaluated partitioning strategies, tested a new approach (e.g., using a more robust key or salting) on a development environment with representative data, and validated its performance. After confirming the fix, I deployed the updated pipeline, closely monitored it, and documented the learning.

What I learned: This experience taught me the critical importance of rigorously validating all assumptions, especially concerning data distributions at scale, before implementing design choices. I also learned to communicate transparently and quickly when a mistake is identified and to focus on a swift, tested resolution. Now, I incorporate more extensive data profiling early in my design process."

Signals to Convey: Honesty, ownership, analytical problem-solving, learning from mistakes, technical remediation, communication.

Scenario 1: Ride Sharing (Uber/Lyft)
1a. Product Sense:

Value Proposition & Mission Alignment:

Value Proposition:

For Riders: Lower price point compared to solo rides, making transportation more accessible.

For Drivers: Potentially more earnings per trip if multiple fares are collected with minimal additional mileage/time, higher utilization.

For the Platform: Increased overall ride volume by attracting price-sensitive users, improved fleet efficiency, potentially reduced traffic congestion and environmental impact (marketable points).

For Community/City: Reduced number of cars on the road, reduced emissions per passenger.

Mission Alignment (e.g., "Connecting People"): Carpooling directly facilitates shared experiences, even if brief, potentially connecting people heading in similar directions. It can make it easier for people to access opportunities (work, social) by providing a more affordable transit option, thereby fostering community access. It can also be framed as building "efficient communities on the move."

Tracking Carpool Performance:

Thought Process: To track carpool performance, we need metrics covering adoption, efficiency, user experience (both rider and driver), and financial impact compared to regular rides. Slicing by dimensions helps identify specific areas of success or friction.

Key Metrics:

Adoption:

Carpool Ride Penetration: (Number of carpool rides / Total rides) * 100.

Carpool Request Success Rate: (Number of successfully matched carpool requests / Total carpool requests) * 100.

Active Users Utilizing Carpool: Number/percentage of DAU/MAU who take at least one carpool ride.

Efficiency & Economics:

Average Fill Rate: Average number of passengers per carpool ride.

Average Detour Time/Distance per Carpool Passenger: Additional travel incurred by carpool passengers vs. a direct route.

Driver Earnings per Hour (Carpool vs. Regular)`: To ensure driver satisfaction and participation.

Revenue per Mile (Carpool vs. Regular)`: To assess financial viability.

User Experience:

Rider CSAT/NPS for Carpool Rides: Specific satisfaction scores.

Driver CSAT/NPS for Carpool Rides.

Cancellation Rate (Carpool vs. Regular): For both riders and drivers.

Slicing Dimensions:

Time: Hour of day, day of week, weekday vs. weekend (to understand demand patterns and peak carpool usage).

Geography: City, specific zones/neighborhoods, route corridors (to identify areas with high/low carpool adoption or efficiency).

User Segment: New vs. existing users, demographics (age, etc.), price sensitivity segments (to understand who is using carpool and why).

Driver Segment: Tenure, vehicle type, rating (to see if certain drivers are better suited or more willing to do carpools).

Ride Characteristics: Trip distance, time of day, number of matched passengers (to analyze performance under different conditions).

Example Answer Script: "To track carpool performance, I'd focus on a balanced scorecard covering adoption, efficiency, user experience, and financials. Key metrics include Carpool Ride Penetration to see overall usage, Request Success Rate for matching effectiveness, and Fill Rate for efficiency. Critically, I'd monitor Average Detour Time and Rider/Driver Satisfaction scores, as these directly impact the user experience. Financially, comparing Carpool Revenue Per Mile and Contribution Margin to regular rides is essential. I'd slice this data by time, geography, and user/driver segments. For instance, looking at detour times in specific city zones during peak hours could reveal routing issues, while analyzing satisfaction scores for new vs. existing users might inform onboarding strategies."

1b. Data Modeling:

Question: How should the data model be designed to support carpool rides where a single ride (ride_id) can involve multiple passengers picked up and dropped off at potentially different locations and times within the same driver's trip? Discuss trade-offs.

Answer (Textual Explanation):

Core Tables:

fact_rides: Represents the overall trip taken by the driver. Contains ride_id (PK), driver-level metrics (total fare, duration, distance), and FKs to driver, vehicle, overall start/end locations/times, date, time, and ride_type_key.

dim_users: Stores user info (riders and drivers with a role indicator).

dim_locations, dim_date, dim_time, dim_ride_type, etc.

Handling Multiple Riders (Bridge Table - Recommended):

Create a fact_ride_segments table.

Columns: ride_segment_id (PK), ride_id (FK to fact_rides), rider_user_key (FK to dim_users), segment_pickup_timestamp, segment_dropoff_timestamp, segment_pickup_location_key (FK), segment_dropoff_location_key (FK), segment_fare, segment_distance, pickup_sequence_in_ride, dropoff_sequence_in_ride.

Each row represents one passenger's journey leg within the overall ride_id.

Trade-offs:

Bridge Table (fact_ride_segments):

Pros: Cleanly normalizes the many-to-many relationship. Allows detailed tracking and querying of each passenger's specific experience (fare, duration, detour). Scales well for analytics. Standard relational approach.

Cons: Requires joins to assemble the full picture of a ride with all its passengers.

Alternatives (e.g., Array/JSON of passenger IDs/details in fact_rides):

Pros: Might simplify fetching all passengers for a single ride without a join.

Cons: Difficult to query or index individual passenger segment details (e.g., "find all segments starting in zone X"). Makes calculating segment-specific metrics complex. Database support for array/JSON operations varies. Can lead to data redundancy or update anomalies. Generally less scalable for complex analytics.

Conclusion: The bridge table (fact_ride_segments) is generally superior for analytics and scalability due to its normalized structure and query flexibility.

Conceptual Database Diagram:

[dim_users]
  user_key (PK)
  name
  role (rider/driver)
  ...

[dim_locations]
  location_key (PK)
  address
  latitude
  longitude
  zone
  ...

[dim_ride_type]
  ride_type_key (PK)
  ride_type_name (e.g., Regular, Pool, Premium)
  ...

[dim_date]
  date_key (PK)
  full_date
  day_of_week
  ...

[dim_time]
  time_key (PK)
  time_of_day (HH:MM:SS)
  hour
  ...

--------------------------------------------------

[fact_rides] (Driver's overall trip)
  ride_id (PK)
  driver_user_key (FK) ---|> [dim_users]
  vehicle_id (FK) -----(vehicle_dim not shown)
  ride_type_key (FK) ---|> [dim_ride_type]
  overall_trip_start_time_key (FK) ---|> [dim_time]
  overall_trip_end_time_key (FK) -----|> [dim_time]
  overall_trip_date_key (FK) ---------|> [dim_date]
  driver_pickup_location_key (FK) ---|> [dim_locations] (Driver's first pickup)
  driver_final_dropoff_location_key (FK) ---|> [dim_locations] (Driver's last dropoff)
  total_ride_duration_seconds
  total_ride_distance_meters
  total_ride_fare
  ...

[fact_ride_segments] (Individual passenger legs in a carpool/ride)
  ride_segment_id (PK)
  ride_id (FK) ------------------------------------|> [fact_rides]
  rider_user_key (FK) -----------------------------|> [dim_users]
  segment_pickup_time_key (FK) -------------------|> [dim_time]
  segment_dropoff_time_key (FK) ------------------|> [dim_time]
  segment_date_key (FK) --------------------------|> [dim_date] (Date of segment start)
  segment_pickup_location_key (FK) ---------------|> [dim_locations]
  segment_dropoff_location_key (FK) --------------|> [dim_locations]
  segment_duration_seconds
  segment_distance_meters
  segment_fare_allocation
  pickup_sequence_in_ride (e.g., 1, 2)
  dropoff_sequence_in_ride (e.g., 1, 2)
  ...


Wireframe/UI Sketch (Conceptual):

Rider App - Ride History:

A list item for a completed carpool ride:

"Carpool with [Driver Name] - [Date]"

"Your Trip: [Pickup Address] to [Dropoff Address]"

"Fare: [$X.XX]"

(Upon tapping) -> Details screen showing your specific segment map, and perhaps anonymized info about the shared ride (e.g., "Shared with 1 other rider").

Driver App - Earnings Summary for a Carpool Trip:

"Trip ID: [ride_id] - Carpool"

"Total Earnings for Trip: [$Y.YY]"

"Route: [Map of entire driver route]"

"Passenger Segments:"

"1. Rider A: Pickup [Loc1] at [Time1], Dropoff [Loc2] at [Time2] - Fare portion: [$A.AA]"

"2. Rider B: Pickup [Loc3] at [Time3], Dropoff [Loc4] at [Time4] - Fare portion: [$B.BB]"

1c. SQL (Original):

Question: Write a SQL query to calculate the percentage of ride segments that belong to a 'Carpool' ride type. Assume fact_ride_segments links to fact_rides, and fact_rides links to dim_ride_type.

Answer:

-- Calculate percentage of *segments* that are part of a Carpool ride
SELECT
    (COUNT(CASE WHEN drt.ride_type_name = 'Carpool' THEN frs.ride_segment_id ELSE NULL END) * 100.0)
    / COUNT(frs.ride_segment_id) AS carpool_segment_percentage
FROM
    fact_ride_segments frs -- Start from the segment table
JOIN
    fact_rides fr ON frs.ride_id = fr.ride_id -- Join to get ride info
JOIN
    dim_ride_type drt ON fr.ride_type_key = drt.ride_type_key -- Join to get type name
-- Optional WHERE clause for specific time period, region, etc.
-- WHERE fr.overall_trip_date_key BETWEEN 'YYYYMMDD' AND 'YYYYMMDD';


Explanation:

Starts from fact_ride_segments (frs).

Joins to fact_rides (fr) and dim_ride_type (drt) to get the ride type name.

Uses conditional COUNT on ride_segment_id where ride_type_name is 'Carpool'.

Divides the carpool segment count by the total segment count (multiplying by 100.0 for percentage).

1e. SQL (New):

Question: Calculate the percentage of distinct drivers who complete more carpool rides than regular (non-carpool) rides in a given period (e.g., last 30 days).

Answer:

WITH DriverRideCounts AS (
    SELECT
        fr.driver_user_key,
        SUM(CASE WHEN drt.ride_type_name = 'Carpool' THEN 1 ELSE 0 END) AS carpool_rides_count,
        SUM(CASE WHEN drt.ride_type_name != 'Carpool' AND drt.ride_type_name IS NOT NULL THEN 1 ELSE 0 END) AS regular_rides_count -- Assuming anything not 'Carpool' is 'Regular'
    FROM
        fact_rides fr
    JOIN
        dim_ride_type drt ON fr.ride_type_key = drt.ride_type_key
    WHERE
        fr.overall_trip_date_key >= DATE('now', '-30 days') -- Example for SQLite, adjust for your SQL dialect
        AND fr.overall_trip_date_key <= DATE('now')     -- Example for SQLite
    GROUP BY
        fr.driver_user_key
),
TotalDistinctDrivers AS (
    SELECT COUNT(DISTINCT driver_user_key) as total_drivers
    FROM DriverRideCounts
),
DriversPreferringCarpool AS (
    SELECT
        COUNT(DISTINCT driver_user_key) as drivers_preferring_carpool_count
    FROM
        DriverRideCounts
    WHERE
        carpool_rides_count > regular_rides_count
)
SELECT
    CASE
        WHEN tdd.total_drivers > 0 THEN (dpc.drivers_preferring_carpool_count * 100.0) / tdd.total_drivers
        ELSE 0.0
    END AS percentage_drivers_preferring_carpool
FROM
    DriversPreferringCarpool dpc, TotalDistinctDrivers tdd;


Explanation:

DriverRideCounts CTE: Groups by driver_user_key from fact_rides (joined with dim_ride_type) within the specified date range. It counts the number of 'Carpool' rides and 'Regular' (non-carpool) rides for each driver.

TotalDistinctDrivers CTE: Counts all drivers who had any rides in the period.

DriversPreferringCarpool CTE: Selects distinct driver_user_keys from DriverRideCounts where the count of carpool rides is greater than regular rides.

Final SELECT: Calculates the percentage by dividing the count of distinct drivers preferring carpool by the total count of distinct drivers who had any rides. Includes a CASE to prevent division by zero.

Scenario 2: Short Video (TikTok/Reels)
2a. Product Sense:

Measuring Success (Original):

Key Metrics: DAU/MAU, Stickiness (DAU/MAU), New User Acquisition Rate, Retention Rate (D1, D7, D30), Churn Rate, Average Session Duration, Average Views per User, Likes/Comments/Shares/Saves per User, View Completion Rate, Follow Rate, Time Spent per DAU, Number of Videos Uploaded per Day/User, Number of Active Creators, % Users who are Creators, Ad Revenue, App Crash Rate, Average Load Time.

Visualization (Original - DAU):

Type: Line Chart. X-axis: Date. Y-axis: Count of DAU.

Enhancements: Trend Line, 7-day Moving Average, Segmentation (New vs. Returning Users, Country, Platform), Annotations for key events.

New PS Question 1: "How would you track if a user significantly changes their 'regular' location (e.g., moves cities) based on their activity?"

Answer:

Data Needed: Geotagged user activity logs (user_id, timestamp, latitude, longitude or IP-derived location_key).

Approach:

Define "Regular Location": Determine user's primary location cluster over a trailing window (e.g., last 30-90 days) - centroid of frequent clusters or most common city.

Identify New Location Activity: In a recent window (e.g., last 7-14 days), check if most activity clusters in a different significant location (e.g., new city > X miles away).

Define "Significant Change": Thresholds for distance, duration/frequency of new location activity.

Metrics: % Active Users with Recent Significant Location Change, Avg Duration in New Location before "Regular", Churn/Retention Post-Location Change.

Challenges: GPS accuracy, location disabling, distinguishing travel vs. move.

New PS Question 2: "How would you compare the engagement (e.g., likes) of original content versus content that is shared? What insights would this provide?"

Answer:

Data Needed: dim_posts (original content), fact_engagement_events (event_id, post_id (original), event_type, shared_from_event_id).

Comparison Metrics: Likes per View (Original vs. Shared Instance), Avg Likes on Original vs. Avg Likes on a Share Event, View-to-Like Conversion Rate (Original vs. Shared).

Approach: Identify engagement on original posts (shared_from_event_id IS NULL) vs. engagement on shared instances (shared_from_event_id IS NOT NULL). Aggregate metrics for both, linking to original_post_id.

Insights: Amplification factor of sharing, audience differences, content decay with re-shares, identify influential sharers.

Product Analytics/Dashboarding Idea: "How would you design a dashboard visualization to show how the launch of Reels is affecting engagement with other platform features?"

Answer:

Pre-Post Launch Comparison: Line charts for metrics of other features (avg. likes/standard post, image uploads, long video watch time) with Reels launch date annotated. Look for cannibalization or lift.

User Segmentation: Stacked Bar/Area Chart of daily time spent per user, segmented by feature (Reels, Posts, etc.). Compare Reels users vs. non-Reels users.

Cohort Analysis: Track cohorts pre/post-Reels launch; compare their engagement patterns with different features over time.

Key Metrics for Other Features: Avg time spent/user/day, items created/viewed per DAU, engagement rate.

2b. Data Modeling:

Question: Design a data model for engagement events that can efficiently handle posts shared many times across multiple layers, supporting counts of total shares per original post and identifying the original poster/time. Address array hints.

Answer (Textual Explanation):

Core Tables:

dim_posts: post_id (PK), author_user_key (FK to dim_users), creation_timestamp, creation_date_key, video_url, caption, etc.

dim_users: user_key (PK), user_name, etc.

Handling Engagement & Shares (Relational Approach - Recommended):

fact_engagement_events: event_id (PK), event_timestamp, date_key, user_key (actor - FK to dim_users), post_id (FK to dim_posts, always points to the original post), event_type (e.g., 'view', 'like', 'comment', 'share', 'react').

Add shared_from_event_id (FK, nullable, references fact_engagement_events.event_id on self). This field is key for tracking share lineage. For a direct share of an original post, it's NULL. For a re-share, it points to the event_id of the share event being re-shared.

Addressing Array Hint: "While an array on dim_posts (e.g., list_of_sharing_user_ids) might seem simple for counting direct shares, it cannot model the multi-layer sharing hierarchy (who shared whose share). It also scales poorly for high share counts. The shared_from_event_id foreign key approach in fact_engagement_events accurately models this graph structure, allowing lineage tracing via recursive queries."

Counting Shares & Finding Original:

Total Shares for Post P: SELECT COUNT(*) FROM fact_engagement_events WHERE post_id = P AND event_type = 'share';

Original Poster/Time for Post P: SELECT author_user_key, creation_timestamp FROM dim_posts WHERE post_id = P;

Optimization: Partition fact_engagement_events by date. Index key columns. Consider pre-aggregating daily share counts.

Conceptual Database Diagram:

[dim_users]
  user_key (PK)
  user_name
  ...

[dim_posts]
  post_id (PK)
  author_user_key (FK) ---|> [dim_users]
  creation_timestamp
  creation_date_key (FK) --|> [dim_date]
  ...

[dim_date] (date_key PK, ...)

--------------------------------------------------

[fact_engagement_events]
  event_id (PK)
  event_timestamp
  date_key (FK) ----------|> [dim_date]
  user_key (FK) ----------|> [dim_users] (User performing event)
  post_id (FK) -----------|> [dim_posts] (The *original* post)
  event_type (e.g., 'view', 'like', 'share')
  shared_from_event_id (FK, nullable) ---\
  ...                                     | (Self-referencing for shares)
                                          |
  ----------------------------------------/


Wireframe/UI Sketch (Conceptual):

News Feed Post UI: Shows content, original author, interaction counts. If shared: "Shared by [Sharer]" (potentially with "from [Previous Sharer]").

Share Details View (Analytics): Original Post ID, Total Shares, Share Tree/Graph Visualization.

2c. SQL (Original):

Question: Write a SQL query to find post_ids for posts that received zero 'like' or 'react' events on the same calendar day they were created.

Answer:

-- Using NOT EXISTS
SELECT dp.post_id
FROM dim_posts dp
WHERE dp.creation_date_key = 'YYYYMMDD_today' -- Use actual date or parameter
  AND NOT EXISTS (
      SELECT 1 FROM fact_engagement_events fee
      WHERE fee.post_id = dp.post_id
        AND fee.date_key = dp.creation_date_key
        AND fee.event_type IN ('like', 'react')
  );


Explanation (NOT EXISTS Approach): Selects post_id from dim_posts created on the target date where no corresponding 'like' or 'react' event exists in fact_engagement_events for that post on its creation day.

2e. SQL (New):

Question: Calculate the percentage of content items created today that received at least one 'reaction' event but zero 'comment' events on the same day.

Answer:

DECLARE target_date_key INT64 DEFAULT 20250213; -- Example: YYYYMMDD format

WITH ContentCreatedToday AS (
    SELECT post_id, creation_date_key
    FROM dim_posts
    WHERE creation_date_key = target_date_key
),
ContentWithReactionsToday AS (
    SELECT DISTINCT cct.post_id
    FROM ContentCreatedToday cct
    JOIN fact_engagement_events fee ON cct.post_id = fee.post_id
    WHERE fee.date_key = cct.creation_date_key
      AND fee.event_type = 'reaction' -- Or specific reactions
),
ContentWithCommentsToday AS (
    SELECT DISTINCT cct.post_id
    FROM ContentCreatedToday cct
    JOIN fact_engagement_events fee ON cct.post_id = fee.post_id
    WHERE fee.date_key = cct.creation_date_key
      AND fee.event_type = 'comment'
),
ContentReactionNoComment AS (
    SELECT crt.post_id
    FROM ContentWithReactionsToday crt
    LEFT JOIN ContentWithCommentsToday cct ON crt.post_id = cct.post_id
    WHERE cct.post_id IS NULL
)
SELECT
    CASE
        WHEN (SELECT COUNT(DISTINCT post_id) FROM ContentCreatedToday) > 0
        THEN ( (SELECT COUNT(DISTINCT post_id) FROM ContentReactionNoComment) * 100.0 ) /
             ( (SELECT COUNT(DISTINCT post_id) FROM ContentCreatedToday) )
        ELSE 0.0
    END AS percentage_reaction_no_comment;


Explanation: Identifies posts created today, then those with reactions today, and those with comments today. Uses a LEFT JOIN to find posts with reactions but no comments. Calculates the percentage against all posts created today.

Scenario 3: Streaming Platform (Netflix/Hulu)
3a. Product Sense:

Question: For a video streaming platform, what are the different types of user engagement you could track? Define key metrics at the Platform, User, and Video levels.

Answer:

Engagement Types: Viewing (Starts, Completions, Time Watched), Rating/Feedback (Likes, Dislikes, Stars), Discovery (Browsing, Searching, Clicking Recs), Collection (Add/Remove Watchlist), Social (Sharing), Playback Control (Pause, Seek), Profile Management.

Metrics:

Platform: DAU/MAU, Stickiness, Avg Session Duration, Content Discovery Rate, Churn Rate, Trial Conversion.

User: Avg Watch Time/User, Content Completion Rate/User, Breadth of Viewing (# Titles), Watchlist Engagement, Search Success Rate.

Video: Total Views, Unique Viewers, Avg View Duration, Completion Rate, Audience Retention Curve, Likes/Dislikes Ratio, Watch Time Contribution.

3b. Data Modeling:

Question: Design the fact_viewing_sessions table. What are its key measures and foreign keys? How would you handle tracking view duration, pauses, and completion status?

Answer (Textual Explanation):

fact_viewing_sessions: One row per distinct viewing segment.

Measures: watch_duration_seconds, max_view_percentage_reached, is_complete_view, num_pauses, total_pause_duration_seconds.

FKs: date_key, start_time_key, end_time_key, user_key, profile_key, video_key, device_key, location_key.

Handling Duration/Pauses: Store start_timestamp, end_timestamp, total_pause_duration_seconds. Calculate watch_duration = (end - start) - pause_duration.

Handling is_complete_view: ETL logic: TRUE if max_view_percentage_reached >= 95% or watch_duration is close to video_total_duration.

Conceptual Database Diagram:

[dim_users] (user_key PK, ...)
[dim_profiles] (profile_key PK, user_key FK, ...)
[dim_videos] (video_key PK, title, video_total_duration_seconds, ...)
[dim_devices], [dim_date], [dim_time], ...
--------------------------------------------------
[fact_viewing_sessions]
  viewing_session_id (PK)
  user_key (FK) ---|> [dim_users]
  profile_key (FK) --|> [dim_profiles]
  video_key (FK) ----|> [dim_videos]
  date_key (FK) -----|> [dim_date]
  start_time_key (FK) -> [dim_time]
  end_time_key (FK) ---> [dim_time]
  watch_duration_seconds
  max_view_percentage_reached
  is_complete_view (Boolean)
  num_pauses
  total_pause_duration_seconds
  ...


Wireframe/UI Sketch (Conceptual):

User's Viewing History: List of watched titles with progress bars (max_view_percentage_reached).

Content Analytics Dashboard: Audience Retention Curve for a video (derived from max_view_percentage_reached).

3c. SQL (Snapshot Update):

Question: Describe the logic and write/outline SQL for a batch process to update a user_cumulative_snapshot table (with total view time) using data from the daily fact_viewing_sessions. Address how to avoid scanning the full fact table for the daily delta and optimize the update.

Answer Logic & SQL:

Logic: 1. Aggregate today's watch time per user from fact_viewing_sessions (filtered by today's date_key - this uses partitioning). 2. MERGE this daily summary into user_cumulative_snapshot. Update existing users by adding today's watch time; insert new users.

Optimization: fact_viewing_sessions must be partitioned by date_key. user_cumulative_snapshot must be indexed on user_key.

SQL (MERGE Example):

DECLARE current_processing_date DATE DEFAULT 'YYYY-MM-DD';

MERGE INTO user_cumulative_snapshot AS target
USING (
    SELECT user_key, SUM(watch_duration_seconds) as daily_watch_seconds
    FROM fact_viewing_sessions
    WHERE date_key = current_processing_date -- This hits only one partition
    GROUP BY user_key
) AS source
ON target.user_key = source.user_key
WHEN MATCHED THEN
    UPDATE SET total_watch_seconds_to_date = target.total_watch_seconds_to_date + source.daily_watch_seconds,
               last_updated_date = current_processing_date
WHEN NOT MATCHED BY TARGET THEN
    INSERT (user_key, total_watch_seconds_to_date, last_updated_date)
    VALUES (source.user_key, source.daily_watch_seconds, current_processing_date);


3d. SQL (New Content Aggregation):

Question: Given a watch_fact table (content_id, user_id, total_watch_time_seconds, date_key), write a query to get the distinct user count and sum of total watch time per content_id for a specific date.

Answer:

SELECT
    content_id,
    COUNT(DISTINCT user_id) AS distinct_user_count,
    SUM(total_watch_time_seconds) AS sum_total_watch_time_seconds
FROM
    watch_fact
WHERE
    date_key = 'YYYYMMDD_target_date' -- Or your specific date predicate
GROUP BY
    content_id
ORDER BY
    distinct_user_count DESC, sum_total_watch_time_seconds DESC; -- Optional ordering


Explanation: Filters watch_fact for the target date, groups by content_id, then calculates COUNT(DISTINCT user_id) and SUM(total_watch_time_seconds) per content.

Scenario 4: Cloud File Storage (Dropbox/Google Drive)
4a. Product Sense:

Question: How would you evaluate the success of a cloud file storage product? What metrics are important?

Answer:

Success Metrics: DAU/MAU, Paid User Growth & Conversion Rate (Free to Paid), Total Storage Used, Average Storage per User, Number of Files Uploaded/Downloaded/Synced per User, Feature Adoption Rate (sync client, integrations), Collaboration Rate (% files shared, avg collaborators/file), Reliability (Uptime, Error Rates), User Satisfaction (CSAT/NPS), Financials (ARR, ARPU).

4b. Data Modeling:

Question: Discuss different data modeling approaches to handle file activity, file sharing, and ownership transfers. What are the key fact and dimension tables?

Answer (Textual Explanation):

Dimension Tables: dim_users, dim_files (file_key PK, original_creator_user_key, filename, current_owner_user_key), dim_activity_types ('upload', 'share'), dim_share_types ('direct_invite', 'link').

Fact Tables:

fact_file_activity: Row per action (activity_id PK, date_key, user_key, file_key, activity_type_key, measures like file_size_bytes_transferred). For 'transfer_ownership', include previous_owner_key, new_owner_key.

bridge_file_permissions (Current state): file_key (FK), user_key (FK - user with permission), permission_level ('viewer', 'editor'). PK on (file_key, user_key).

fact_storage_snapshot (Daily): snapshot_date_key, user_key, total_storage_bytes_used, num_files_owned.

Handling Sharing/Ownership: bridge_file_permissions for current access. dim_files for original creator. Ownership transfer is an event in fact_file_activity; current_owner_user_key in dim_files can be updated (Type 1 SCD).

Conceptual Database Diagram:

[dim_users] (user_key PK, ...)
[dim_files] (file_key PK, original_creator_user_key FK, filename, current_owner_user_key FK)
[dim_activity_types] (activity_type_key PK, activity_name)
--------------------------------------------------
[fact_file_activity]
  activity_id (PK), date_key, user_key (FK), file_key (FK), activity_type_key (FK), ...
[bridge_file_permissions]
  file_key (FK), user_key (FK), permission_level, PRIMARY KEY (file_key, user_key)
[fact_storage_snapshot]
  snapshot_date_key (FK), user_key (FK), total_storage_bytes_used, ...


Wireframe/UI Sketch (Conceptual):

File Browser UI: List files/folders. For each: Icon, Filename, Last Modified, Size, Owner. "Share" button.

Share Dialog UI: "Share '[Filename]'". Input: "Add people". Dropdown: "Can view"/"Can edit". "Copy link". List of "People with access".

4c. SQL:

Question 1 & 2 Answers & Explanations: (Same as provided in previous full response for this document)

Scenario 5: DAU/MAU Analysis
5a. Product Sense:

Question: You observe a sudden, significant drop in DAU/MAU. Potential causes and diagnostic process?

Answer:

Causes: Data/Tracking Issues, Technical Issues (outage, bad deployment), External Factors (holiday, competitor), Product Changes (unpopular UI/feature), Marketing Changes.

Process: 1. Verify data. 2. Check system health. 3. Correlate with deployments. 4. Segment drop (platform, region, user type). 5. Investigate external. 6. Review internal changes.

5b. Data Modeling / ETL:

Question: Describe fact/dimension tables for DAU/MAU. Outline ETL for user states (New, Retained, Churned, Resurrected).

Answer (Textual Explanation):

Dimensions: dim_users (user_key PK, first_active_date_key, last_active_date_key, current_churn_status), dim_date.

Fact: fact_user_daily_activity (date_key, user_key as composite PK; optional measures like session_count).

ETL for User States (Daily):

Identify Today's Active Users (today_active_set).

Update dim_users.last_active_date_key for these users.

New Users: In today_active_set & dim_users.first_active_date_key is today.

Retained: In today_active_set & active yesterday (or recent window).

Churned: dim_users.last_active_date_key > 30 days ago & NOT in today_active_set. Update current_churn_status.

Resurrected: In today_active_set & dim_users.last_active_date_key was > 30 days ago. Update current_churn_status.

Conceptual Database Diagram:

[dim_users]
  user_key (PK)
  first_active_date_key (FK) ---|> [dim_date]
  last_active_date_key (FK) ----|> [dim_date]
  current_churn_status
  ...
[dim_date] (date_key PK, ...)
--------------------------------------------------
[fact_user_daily_activity]
  date_key (FK) ----------|> [dim_date]
  user_key (FK) ----------|> [dim_users]
  PRIMARY KEY (date_key, user_key)
  ...


Wireframe/UI Sketch (Conceptual):

DAU/MAU Dashboard: Line charts (DAU, MAU, DAU/MAU ratio over time). Bar chart (New, Retained, Resurrected, Churned users per day/week). Filters.

5c. SQL:

Question 1 & 2 Answers & Explanations: (Same as provided in previous full response for this document)

Scenario 6: News Feed
6a. Product Sense:

Question: Define "viewed" post (>=5s OR >=80% visible). Challenges? Logging needed?

Answer:

Definition: View = (Visible Time >= 5s) OR (Max Visible Area >= 80%) during continuous on-screen period.

Challenges: Fast scrolling, partial visibility, background tabs, client-side measurement complexity, data volume.

Logging: Client logs: session_id, user_id, post_id, event_type ('impression_start'/'end'), timestamp, visible_percentage_on_screen (or time_on_screen_ms).

6b. Data Modeling / Logging:

Question: What data needs to be logged client-side for valid view definition? Describe log schema.

Answer (Textual Explanation):

Client-Side Log Event: session_id, user_id, post_id, event_timestamp_utc_ms, event_type ('impression_start', 'impression_end', 'visibility_update'), visible_percentage_on_screen.

Processed Table (newsfeed_impression_segments): impression_id PK, session_id, user_key, post_id, impression_start_timestamp, impression_end_timestamp, duration_on_screen_seconds, max_visible_percentage_during_impression, is_valid_view (Boolean, by ETL).

Conceptual Log Schema (Client-Side Event):

{
  "log_id": "unique_event_id",
  "session_id": "user_session_abc123",
  "user_id": "user_xyz789",
  "post_id": "post_def456",
  "event_timestamp_utc_ms": 1678886400123,
  "event_type": "impression_start",
  "visible_percentage": 75.5
}


Wireframe/UI Sketch (Conceptual - Internal Dashboard):

Content Performance Dashboard: Table "Post Viewability Metrics" (Post ID | Total Impressions | Valid Views | Avg. Time On Screen | Avg. Max Visibility % | Valid View Rate %).

6c. SQL:

Question & Answer & Explanation: (Same as provided in previous full response for this document)

Scenario 7: Photo Upload (Instagram-like)
7a. Product Sense:

Question: Photo upload process stages? Metrics for performance/reliability? Visualize avg upload time?

Answer:

Stages: Client Prep (select, resize/compress), Network Transfer, Server Ingestion, Server Processing (validate, thumbnails), Storage/Metadata Update.

Metrics: End-to-End Duration (P50, P90), Duration/Stage, Success Rate, Failure Rate/Stage, Upload Speed, File Size Dist.

Visualization: Line chart (Median/P90 Upload Time vs. Time), segmented by Network Type.

7b. Data Modeling:

Question: Design fact table for photo upload events. Measures? FKs?

Answer (Textual Explanation):

fact_upload_events: Row per upload attempt.

Measures: upload_duration_ms, file_size_bytes, is_success.

FKs: date_key, time_key, user_key, file_key (on success), device_key, network_type_key, failure_reason_key.

Conceptual Database Diagram:

[dim_users] (user_key PK, ...)
[dim_files] (file_key PK, ...)
[dim_devices] (device_key PK, ...)
[dim_network_types] (network_type_key PK, ...)
[dim_failure_reasons] (failure_reason_key PK, ...)
--------------------------------------------------
[fact_upload_events]
  upload_event_id (PK)
  date_key (FK), time_key (FK), user_key (FK), file_key (FK, nullable)
  device_key (FK), network_type_key (FK), failure_reason_key (FK, nullable)
  upload_duration_ms, file_size_bytes, is_success (Boolean)
  ...


Wireframe/UI Sketch (Conceptual - Internal Dashboard):

Upload Performance Dashboard: Line chart "Avg Upload Duration by Network Type". Bar chart "Upload Success Rate by App Version".

7c. SQL:

Question & Answer & Explanation: (Same as provided in previous full response for this document)

Scenario 8: FB Messenger
8a. Product Sense:

Question: DAU/MAU drop for Messenger. Specific causes?

Answer: Core send/receive issues, notification problems, connectivity, login/auth, spam changes, competitor actions, network effects, unpopular features/bugs.

8b. Data Modeling:

Question: Key fact tables for messaging app activity (messages sent, logins)?

Answer (Textual Explanation):

fact_messages_sent: Row per message (sender_user_key, recipient_user_key/chat_key, date_key, time_key, measures like message_length).

fact_user_logins (or fact_user_daily_activity): Row per login/active day (user_key, date_key, time_key, device_key).

fact_chat_participants (Bridge for group chats): chat_key, user_key.

Conceptual Database Diagram:

[dim_users] (user_key PK, ...)
[dim_chats] (chat_key PK, chat_type)
--------------------------------------------------
[fact_messages_sent]
  message_id (PK), chat_key (FK), sender_user_key (FK), date_key, time_key, ...
[fact_chat_participants]
  chat_key (FK), user_key (FK), PRIMARY KEY (chat_key, user_key), ...
[fact_user_logins]
  login_event_id (PK), user_key (FK), date_key, time_key, ...


Wireframe/UI Sketch (Conceptual - Internal Dashboard):

User Activity Dashboard: Chart "Messages Sent per User per Day". Chart "Active Chats (Group vs. Direct)".

8c. SQL:

Question & Answer & Explanation: (Same as provided in previous full response for this document)

Scenario 9: Food Delivery (DoorDash) - Order Batching
9a. Product Sense:

Value Proposition & Goals:

Goals: Increase Dasher Efficiency & Earnings, Reduce Platform Delivery Costs, Improve Delivery Times (potentially), Increase Service Availability.

Value Proposition: Dashers (higher earnings), Platform (efficiency, cost), Customers (lower fees, risk of longer waits), Restaurants (more orders).

Tracking Performance:

Dasher: Avg Batched Orders/Trip, Earnings/Hour (Batched vs. Single).

Customer: Avg Delivery Time (Batched vs. Single), Food Temp/Quality, CSAT (Batched).

Restaurant: Prep Time vs. Dasher Arrival.

Platform: % Orders Batched, Avg Cost/Delivery, Dasher Utilization.

9b. Data Modeling:

Question: Design data model for batched deliveries (trip, orders, items). Link entities, track trip/order timings.

Answer (Textual Explanation):

Dimensions: dim_dashers, dim_customers, dim_restaurants, dim_locations, dim_menu_items.

Facts:

fact_delivery_trips: trip_id PK, dasher_id FK, trip timings, number_of_orders_in_batch.

fact_orders: order_id PK, customer_id FK, restaurant_id FK, trip_id FK (links to batch), order timings, status.

fact_order_items: order_id FK, item_id FK, quantity.

Tracking: trip_id links orders to a batch. fact_orders has individual order timings. fact_delivery_trips has overall Dasher journey metrics for the batch.

Conceptual Database Diagram:

[dim_dashers] (dasher_id PK, ...)
[dim_customers] (customer_id PK, ...)
[dim_restaurants] (restaurant_id PK, ...)
[dim_menu_items] (item_id PK, restaurant_id FK, ...)
--------------------------------------------------
[fact_delivery_trips]
  trip_id (PK), dasher_id (FK), trip_start_timestamp, trip_end_timestamp, number_of_orders_in_batch, ...
[fact_orders]
  order_id (PK), trip_id (FK, nullable), customer_id (FK), restaurant_id (FK), order_placed_timestamp, order_delivered_timestamp, ...
[fact_order_items]
  order_item_id (PK), order_id (FK), item_id (FK), quantity, ...


Wireframe/UI Sketch (Conceptual):

Dasher App - Active Batched Trip: Map with multiple pins (restaurants, customers). List of stops with actions (Navigate, Mark Picked Up/Delivered).

Customer App - Order Tracking (Batched): "Your order... is part of a batched delivery... Dasher is completing another delivery nearby..." Map of Dasher.

9c. SQL:

Question & Answer & Explanation: (Same as provided in previous full response for this document)