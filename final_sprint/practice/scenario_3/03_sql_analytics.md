# Problem 3: SQL Analytics - Attribution & ROAS Calculation Queries
**Time Limit: 8 minutes**

## Scenario
Write SQL queries to calculate ad attribution metrics and advertiser ROAS (Return on Ad Spend). Focus on handling complex customer journeys and multiple attribution models at Meta's advertising scale.

## Sample Schema (Use this for your queries)
```sql
-- Fact Tables
fact_ad_events (
    event_id VARCHAR(50),
    user_hash VARCHAR(64), -- Privacy-safe user identifier
    device_id VARCHAR(50),
    campaign_id BIGINT,
    ad_group_id BIGINT,
    ad_id BIGINT,
    event_type VARCHAR(30), -- 'impression', 'click', 'view'
    event_timestamp TIMESTAMP,
    placement VARCHAR(20), -- 'feed', 'story', 'reels'
    cost_micros BIGINT, -- Cost in micros (1M = $1)
    date_partition DATE
);

fact_conversions (
    conversion_id VARCHAR(50),
    user_hash VARCHAR(64),
    device_id VARCHAR(50),
    conversion_type VARCHAR(30), -- 'purchase', 'signup', 'download'
    conversion_timestamp TIMESTAMP,
    conversion_value_micros BIGINT, -- Revenue in micros
    source_campaign_id BIGINT, -- Last-click attribution
    advertiser_id BIGINT,
    date_partition DATE
);

fact_touchpoints (
    touchpoint_id VARCHAR(50),
    user_hash VARCHAR(64),
    campaign_id BIGINT,
    touchpoint_timestamp TIMESTAMP,
    touchpoint_order INT, -- 1st, 2nd, 3rd interaction
    time_to_conversion_hours INT,
    attribution_weight DECIMAL(5,4), -- For fractional attribution
    date_partition DATE
);

-- Dimension Tables
dim_campaigns (
    campaign_id BIGINT PRIMARY KEY,
    advertiser_id BIGINT,
    campaign_name VARCHAR(255),
    campaign_objective VARCHAR(50), -- 'conversions', 'traffic', 'awareness'
    daily_budget_micros BIGINT,
    start_date DATE,
    end_date DATE
);

dim_advertisers (
    advertiser_id BIGINT PRIMARY KEY,
    business_name VARCHAR(255),
    industry VARCHAR(50),
    country_code VARCHAR(2),
    total_lifetime_spend_micros BIGINT
);
```

## Your Task

### Query 1: Multi-Touch Attribution Analysis (4 minutes)
**Business Question**: Calculate ROAS for each campaign using last-click, first-click, and linear attribution models for the last 30 days.

**Requirements**:
- Compare 3 attribution models side by side
- Calculate ROAS = (Revenue / Ad Spend) for each
- Include conversion count and total spend
- Show significant differences between models
- Focus on campaigns with 100+ conversions

*Write the SQL query*

### Query 2: Cross-Device Attribution Gap Analysis (2 minutes)
**Business Question**: Identify the revenue gap between same-device and cross-device attributed conversions by campaign.

**Cross-device Conversion**: Conversion happens on different device than the last ad click.

**Requirements**:
- Calculate same-device vs cross-device conversion value
- Show the attribution gap as percentage of total revenue
- Focus on mobile-to-desktop conversion patterns
- Include campaigns with significant cross-device activity

*Write the SQL query*

### Query 3: Campaign Performance Optimization (2 minutes)
**Business Question**: Identify underperforming campaigns that should pause or get budget reallocation.

**Criteria for Review**:
- ROAS < 2.0 (spending more than 50% of revenue on ads)
- Spent >$10,000 in last 7 days
- Conversion rate < 1%

**Requirements**:
- Rank campaigns by worst ROAS first
- Include total spend, conversions, and revenue
- Show days since campaign started

*Write the SQL query*

## Follow-up Questions
Be prepared to discuss:
- How would you optimize these queries for hourly dashboard updates?
- What approach would you take to handle late-arriving conversion data?
- How would you modify attribution windows for different business verticals?
- What incremental analysis would you add to measure true ad effectiveness?

## Technical Constraints
- **Data Volume**: 1B+ ad events and 100M+ conversions daily
- **Performance**: Queries must complete in <10 seconds for advertiser dashboards
- **Accuracy**: Attribution calculations must be consistent across time windows
- **Real-time**: Support near real-time ROAS calculations for campaign optimization

## Success Criteria
- **Accurate attribution logic** across multiple models
- **Efficient query structure** leveraging proper partitioning
- **Clear business insights** for campaign optimization decisions
- **Scalable approach** for Meta's advertising volume

## Meta Context
- Attribution queries power advertiser dashboards used by millions of businesses
- ROAS calculations directly influence automated bidding algorithms
- Cross-device attribution is critical competitive differentiator
- Privacy changes require sophisticated query approaches for user matching 