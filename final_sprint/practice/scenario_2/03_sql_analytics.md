# Problem 3: SQL Analytics - Reels Performance Queries
**Time Limit: 8 minutes**

## Scenario
Using your Reels schema design, write SQL queries to answer critical business questions. Focus on performance at Meta scale (billions of rows).

## Sample Schema (Use this for your queries)
```sql
-- Fact Tables
fact_video_sessions (
    session_id VARCHAR(50),
    user_id BIGINT,
    video_id BIGINT,
    creator_id BIGINT,
    session_start_ts TIMESTAMP,
    session_end_ts TIMESTAMP,
    view_duration_seconds INT,
    engagement_events JSON,
    date_partition DATE
);

fact_engagement_events (
    event_id VARCHAR(50),
    user_id BIGINT,
    video_id BIGINT,
    creator_id BIGINT,
    event_type VARCHAR(20), -- 'view', 'like', 'share', 'comment'
    event_timestamp TIMESTAMP,
    session_id VARCHAR(50),
    date_partition DATE
);

-- Dimension Tables  
dim_users (user_id, registration_date, country, age_group);
dim_videos (video_id, creator_id, upload_timestamp, duration_seconds, category);
dim_creators (creator_id, follower_count, verification_status, join_date);
```

## Your Task

### Query 1: Session Completion Rate (3 minutes)
**Business Question**: What's the % of sessions where users watched ≥3 videos in the last 7 days?

**Requirements**:
- Filter to last 7 days
- Count distinct sessions with 3+ videos
- Calculate as percentage of total sessions
- Group by date for trending

*Write the SQL query*

### Query 2: Video Engagement Score (3 minutes)
**Business Question**: Calculate a weighted engagement score for each video uploaded in the last 30 days.

**Scoring Logic**:
- View = 1 point
- Like = 3 points  
- Share = 5 points
- Comment = 7 points

**Requirements**:
- Include video metadata (creator, duration, category)
- Rank videos by engagement score
- Only videos with 100+ views

*Write the SQL query*

### Query 3: Creator Trend Analysis (2 minutes)
**Business Question**: Show week-over-week growth in follower engagement per creator.

**Metrics Needed**:
- Total engagement events per creator per week
- % change vs previous week
- Only creators with 1000+ followers

*Write the SQL query*

## Follow-up Questions
Be prepared to discuss:
- How would you optimize these queries for a real-time dashboard?
- What indexes would you add for better performance?
- How would you handle these queries on 100TB+ of data?
- What aggregation strategies would reduce compute costs?

## Technical Constraints
- **Data Volume**: 1B+ rows per table
- **Performance**: Queries must complete in <30 seconds
- **Concurrency**: Support 100+ simultaneous dashboard users
- **Cost**: Minimize scan volume and compute time

## Success Criteria
- **Correct SQL syntax** and logic
- **Efficient query structure** with proper joins and filters
- **Meta-scale considerations** (partitioning, indexing hints)
- **Clear business metric calculations** 