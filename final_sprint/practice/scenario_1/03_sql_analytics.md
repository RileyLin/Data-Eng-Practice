# Problem 3: SQL Analytics - DAU/MAU Calculation Queries
**Time Limit: 8 minutes**

## Scenario
Write SQL queries to calculate DAU/MAU metrics and analyze user engagement patterns. Focus on performance at Meta scale with billions of user activity records.

## Sample Schema (Use this for your queries)
```sql
-- Fact Tables
fact_user_sessions (
    session_id VARCHAR(50),
    user_id BIGINT,
    platform VARCHAR(20), -- 'facebook', 'instagram', 'whatsapp'
    session_start_ts TIMESTAMP,
    session_end_ts TIMESTAMP,
    session_duration_seconds INT,
    total_interactions INT,
    date_partition DATE
);

fact_user_interactions (
    interaction_id VARCHAR(50),
    user_id BIGINT,
    platform VARCHAR(20),
    interaction_type VARCHAR(30), -- 'post_like', 'post_share', 'story_view', etc.
    content_id BIGINT,
    interaction_timestamp TIMESTAMP,
    session_id VARCHAR(50),
    date_partition DATE
);

-- Dimension Tables
dim_users (
    user_id BIGINT PRIMARY KEY,
    registration_date DATE,
    country_code VARCHAR(2),
    age_group VARCHAR(20),
    user_status VARCHAR(20) -- 'active', 'deactivated', 'deleted'
);

dim_content (
    content_id BIGINT PRIMARY KEY,
    content_type VARCHAR(20), -- 'post', 'story', 'ad'
    creator_user_id BIGINT,
    creation_timestamp TIMESTAMP
);
```

## Your Task

### Query 1: Rolling DAU/MAU Calculation (3 minutes)
**Business Question**: Calculate the DAU/MAU ratio for each of the last 30 days, showing the trend over time.

**Requirements**:
- Calculate DAU (distinct users active on each day)
- Calculate MAU (distinct users active in 30-day window ending on each day)
- Show ratio as percentage
- Include breakdown by platform (Facebook, Instagram)
- Order by date

*Write the SQL query*

### Query 2: User Cohort Retention Analysis (3 minutes)
**Business Question**: For users who joined in January 2025, calculate their Day 1, Day 7, Day 30 retention rates.

**Retention Definition**: User is retained on Day N if they had any activity on Day N after registration.

**Requirements**:
- Focus on users registered in January 2025
- Calculate retention for Day 1, 7, 30
- Show both count and percentage retained
- Include overall cohort size

*Write the SQL query*

### Query 3: Churn Risk Identification (2 minutes)
**Business Question**: Identify users at risk of churning (no activity in last 14 days but were active in previous 30 days).

**Requirements**:
- Users with no activity in last 14 days
- But had activity in days 15-44 (30-day window before the 14-day gap)
- Include user details and last activity date
- Rank by days since last activity

*Write the SQL query*

## Follow-up Questions
Be prepared to discuss:
- How would you optimize these queries for daily automated runs?
- What indexes would you create for better performance?
- How would you handle these calculations across multiple time zones?
- What approach would you use for real-time DAU tracking?

## Technical Constraints
- **Data Volume**: 10B+ rows in fact tables
- **Performance**: Queries must complete in <30 seconds for dashboards
- **Accuracy**: Results must be consistent across different time windows
- **Scalability**: Support concurrent execution by multiple analysts

## Success Criteria
- **Correct SQL logic** for DAU/MAU calculations
- **Efficient query structure** using proper partitioning
- **Accurate retention math** with proper date handling
- **Scalable approach** considering Meta's data volume

## Meta Context
- DAU/MAU queries run automatically every hour
- Results feed into executive dashboards and ML models
- Cross-platform aggregation is critical for overall Meta metrics
- Accuracy is essential for investor reporting and product decisions 