# Scenario 2: Short Video (TikTok/Reels) - SQL Questions

## Database Schema Reference

Based on the data model for short video platforms:

### Dimension Tables
- **dim_users**: user_key, user_id, registration_date, user_type, creator_tier, region, follower_count, following_count
- **dim_content**: content_key, content_id, content_type, category, duration_seconds, music_id, hashtags, effects_used, upload_timestamp
- **dim_date**: date_key, full_date, year, month, day_of_month, day_of_week, hour, is_weekend
- **dim_engagement_type**: engagement_key, engagement_type, engagement_weight, counts_as_view

### Fact Tables
- **fact_content_engagements**: engagement_id, user_key, content_key, engagement_key, date_key, engagement_timestamp, watch_duration_seconds, completion_percentage, engagement_context
- **fact_content_performance**: content_key, date_key, total_views, unique_viewers, total_likes, total_comments, total_shares, total_saves, avg_watch_duration, completion_rate, viral_score
- **fact_creator_analytics**: user_key, date_key, content_posted, total_views_received, total_engagements_received, new_followers, follower_churn, engagement_rate, trending_content_ids

---

## Question 1: Viral Content Identification

**Problem**: Identify content that has gone viral in the last 48 hours (content with engagement 10x above creator's average).

**Expected Output**: Content details with viral metrics and performance comparison to creator baseline.

### Solution:
```sql
WITH creator_baselines AS (
    SELECT 
        du.user_key,
        du.user_id,
        AVG(fca.total_views_received) as avg_daily_views,
        AVG(fca.total_engagements_received) as avg_daily_engagements
    FROM fact_creator_analytics fca
    JOIN dim_users du ON fca.user_key = du.user_key  
    JOIN dim_date dd ON fca.date_key = dd.date_key
    WHERE dd.full_date >= CURRENT_DATE - 30
    GROUP BY du.user_key, du.user_id
),
recent_content_performance AS (
    SELECT 
        dc.content_id,
        dc.category,
        du.user_id as creator_id,
        du.user_key as creator_key,
        SUM(fcp.total_views) as total_views_48h,
        SUM(fcp.total_likes + fcp.total_comments * 5 + fcp.total_shares * 10) as engagement_score,
        AVG(fcp.completion_rate) as avg_completion_rate,
        MAX(fcp.viral_score) as max_viral_score
    FROM fact_content_performance fcp
    JOIN dim_content dc ON fcp.content_key = dc.content_key
    JOIN dim_users du ON dc.creator_user_key = du.user_key
    JOIN dim_date dd ON fcp.date_key = dd.date_key
    WHERE dd.full_date >= CURRENT_DATE - 2
    GROUP BY dc.content_id, dc.category, du.user_id, du.user_key
)
SELECT 
    rcp.content_id,
    rcp.creator_id,
    rcp.category,
    rcp.total_views_48h,
    rcp.engagement_score,
    rcp.avg_completion_rate,
    cb.avg_daily_views as creator_avg_views,
    cb.avg_daily_engagements as creator_avg_engagements,
    ROUND(rcp.engagement_score / NULLIF(cb.avg_daily_engagements, 0), 2) as viral_multiplier,
    CASE 
        WHEN rcp.engagement_score > cb.avg_daily_engagements * 10 THEN 'Viral'
        WHEN rcp.engagement_score > cb.avg_daily_engagements * 5 THEN 'Trending'
        ELSE 'Normal'
    END as content_status
FROM recent_content_performance rcp
JOIN creator_baselines cb ON rcp.creator_key = cb.user_key
WHERE rcp.engagement_score > cb.avg_daily_engagements * 5  -- At least trending
ORDER BY viral_multiplier DESC
LIMIT 50;
```

---

## Question 2: Creator Tier Performance Analysis

**Problem**: Compare engagement rates and growth metrics across different creator tiers.

**Expected Output**: Performance metrics segmented by creator tier showing tier-specific trends.

### Solution:
```sql
WITH creator_metrics AS (
    SELECT 
        du.creator_tier,
        du.user_key,
        AVG(fca.engagement_rate) as avg_engagement_rate,
        AVG(fca.total_views_received) as avg_daily_views,
        AVG(fca.new_followers - fca.follower_churn) as avg_net_follower_growth,
        COUNT(DISTINCT fca.date_key) as active_days,
        SUM(fca.content_posted) as total_content_posted
    FROM fact_creator_analytics fca
    JOIN dim_users du ON fca.user_key = du.user_key
    JOIN dim_date dd ON fca.date_key = dd.date_key
    WHERE dd.full_date >= CURRENT_DATE - 30
      AND du.user_type IN ('creator', 'both')
      AND du.creator_tier IS NOT NULL
    GROUP BY du.creator_tier, du.user_key
)
SELECT 
    creator_tier,
    COUNT(DISTINCT user_key) as total_creators,
    ROUND(AVG(avg_engagement_rate), 4) as avg_engagement_rate,
    ROUND(AVG(avg_daily_views), 0) as avg_daily_views,
    ROUND(AVG(avg_net_follower_growth), 1) as avg_net_follower_growth,
    ROUND(AVG(total_content_posted::DECIMAL / active_days), 2) as avg_content_per_day,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY avg_engagement_rate) as median_engagement_rate,
    PERCENTILE_CONT(0.9) WITHIN GROUP (ORDER BY avg_daily_views) as p90_daily_views
FROM creator_metrics
GROUP BY creator_tier
ORDER BY 
    CASE creator_tier 
        WHEN 'top' THEN 1 
        WHEN 'established' THEN 2 
        WHEN 'rising' THEN 3 
        WHEN 'casual' THEN 4 
    END;
```

---

## Question 3: Content Category Trends

**Problem**: Analyze trending content categories by completion rates and engagement patterns.

**Expected Output**: Category performance with trend indicators and seasonal patterns.

### Solution:
```sql
WITH category_performance AS (
    SELECT 
        dc.category,
        dd.full_date,
        dd.day_of_week,
        dd.is_weekend,
        SUM(fcp.total_views) as daily_views,
        SUM(fcp.total_likes + fcp.total_comments + fcp.total_shares) as daily_engagements,
        AVG(fcp.completion_rate) as avg_completion_rate,
        COUNT(DISTINCT fcp.content_key) as content_count
    FROM fact_content_performance fcp
    JOIN dim_content dc ON fcp.content_key = dc.content_key
    JOIN dim_date dd ON fcp.date_key = dd.date_key
    WHERE dd.full_date >= CURRENT_DATE - 14
    GROUP BY dc.category, dd.full_date, dd.day_of_week, dd.is_weekend
),
category_trends AS (
    SELECT 
        category,
        AVG(daily_views) as avg_daily_views,
        AVG(daily_engagements) as avg_daily_engagements,
        AVG(avg_completion_rate) as overall_completion_rate,
        AVG(CASE WHEN is_weekend = TRUE THEN daily_views ELSE NULL END) as avg_weekend_views,
        AVG(CASE WHEN is_weekend = FALSE THEN daily_views ELSE NULL END) as avg_weekday_views,
        
        -- Calculate 7-day trend
        AVG(CASE WHEN full_date >= CURRENT_DATE - 7 THEN daily_views ELSE NULL END) as recent_avg_views,
        AVG(CASE WHEN full_date < CURRENT_DATE - 7 THEN daily_views ELSE NULL END) as older_avg_views
    FROM category_performance
    GROUP BY category
)
SELECT 
    category,
    ROUND(avg_daily_views, 0) as avg_daily_views,
    ROUND(avg_daily_engagements, 0) as avg_daily_engagements,
    ROUND(overall_completion_rate, 3) as completion_rate,
    ROUND((avg_daily_engagements / NULLIF(avg_daily_views, 0)) * 100, 2) as engagement_rate_pct,
    
    -- Weekend vs weekday performance
    ROUND((avg_weekend_views / NULLIF(avg_weekday_views, 0) - 1) * 100, 1) as weekend_boost_pct,
    
    -- 7-day trend analysis
    ROUND((recent_avg_views / NULLIF(older_avg_views, 0) - 1) * 100, 1) as week_over_week_growth_pct,
    
    CASE 
        WHEN recent_avg_views > older_avg_views * 1.1 THEN 'Growing'
        WHEN recent_avg_views < older_avg_views * 0.9 THEN 'Declining'
        ELSE 'Stable'
    END as trend_direction
FROM category_trends
WHERE avg_daily_views > 1000  -- Filter for significant categories
ORDER BY avg_daily_views DESC;
```

---

## Question 4: Discovery Source Effectiveness

**Problem**: Analyze how different discovery sources (For You, Following, Hashtag, etc.) perform in terms of engagement conversion.

**Expected Output**: Discovery source performance metrics with conversion rates.

### Solution:
```sql
WITH discovery_analysis AS (
    SELECT 
        fde.discovery_source,
        fde.position_in_feed,
        fde.user_key,
        fde.content_key,
        fde.clicked_through,
        fde.time_to_engagement,
        -- Check if user engaged after discovery
        CASE WHEN fce.engagement_id IS NOT NULL THEN 1 ELSE 0 END as engaged_after_discovery
    FROM fact_discovery_events fde
    LEFT JOIN fact_content_engagements fce ON (
        fde.user_key = fce.user_key 
        AND fde.content_key = fce.content_key
        AND fce.engagement_timestamp > fde.discovery_timestamp
        AND fce.engagement_timestamp <= fde.discovery_timestamp + INTERVAL '1 hour'
    )
    JOIN dim_date dd ON fde.date_key = dd.date_key
    WHERE dd.full_date >= CURRENT_DATE - 7
),
source_performance AS (
    SELECT 
        discovery_source,
        COUNT(*) as total_discoveries,
        SUM(clicked_through::INT) as total_clicks,
        SUM(engaged_after_discovery) as total_engagements,
        AVG(position_in_feed) as avg_position,
        AVG(time_to_engagement) as avg_time_to_engagement
    FROM discovery_analysis
    GROUP BY discovery_source
)
SELECT 
    discovery_source,
    total_discoveries,
    total_clicks,
    total_engagements,
    ROUND(avg_position, 1) as avg_position_in_feed,
    
    -- Conversion rates
    ROUND((total_clicks::DECIMAL / total_discoveries) * 100, 2) as click_through_rate_pct,
    ROUND((total_engagements::DECIMAL / total_discoveries) * 100, 2) as discovery_to_engagement_rate_pct,
    ROUND((total_engagements::DECIMAL / NULLIF(total_clicks, 0)) * 100, 2) as click_to_engagement_rate_pct,
    
    -- Performance metrics
    ROUND(avg_time_to_engagement, 1) as avg_seconds_to_engagement,
    
    -- Efficiency score (engagements per discovery, weighted by position)
    ROUND(
        (total_engagements::DECIMAL / total_discoveries) / NULLIF(avg_position, 0) * 10, 
        3
    ) as efficiency_score
FROM source_performance
WHERE total_discoveries >= 100  -- Filter for statistical significance
ORDER BY discovery_to_engagement_rate_pct DESC;
```

---

## Question 5: User Engagement Journey Analysis

**Problem**: Track user engagement patterns within 24 hours of account creation to identify successful onboarding.

**Expected Output**: New user behavior patterns and success indicators.

### Solution:
```sql
WITH new_users AS (
    SELECT 
        user_key,
        user_id,
        registration_date
    FROM dim_users
    WHERE registration_date >= CURRENT_DATE - 30
),
user_first_day_activity AS (
    SELECT 
        nu.user_key,
        nu.user_id,
        nu.registration_date,
        
        -- Content consumption
        COUNT(CASE WHEN det.engagement_type = 'view' THEN fce.engagement_id ELSE NULL END) as views_first_day,
        COUNT(CASE WHEN det.engagement_type = 'like' THEN fce.engagement_id ELSE NULL END) as likes_first_day,
        COUNT(CASE WHEN det.engagement_type = 'share' THEN fce.engagement_id ELSE NULL END) as shares_first_day,
        COUNT(CASE WHEN det.engagement_type = 'follow' THEN fce.engagement_id ELSE NULL END) as follows_first_day,
        
        -- Content creation  
        COUNT(DISTINCT dc.content_key) as content_created_first_day,
        
        -- Engagement depth
        AVG(fce.completion_percentage) as avg_completion_rate,
        SUM(fce.watch_duration_seconds) as total_watch_time,
        
        -- Discovery sources used
        COUNT(DISTINCT fde.discovery_source) as discovery_sources_tried
        
    FROM new_users nu
    LEFT JOIN fact_content_engagements fce ON (
        nu.user_key = fce.user_key 
        AND fce.engagement_timestamp >= nu.registration_date
        AND fce.engagement_timestamp < nu.registration_date + INTERVAL '1 day'
    )
    LEFT JOIN dim_engagement_type det ON fce.engagement_key = det.engagement_key
    LEFT JOIN dim_content dc ON (
        fce.content_key = dc.content_key 
        AND dc.creator_user_key = nu.user_key
    )
    LEFT JOIN fact_discovery_events fde ON (
        nu.user_key = fde.user_key
        AND fde.discovery_timestamp >= nu.registration_date
        AND fde.discovery_timestamp < nu.registration_date + INTERVAL '1 day'
    )
    GROUP BY nu.user_key, nu.user_id, nu.registration_date
),
user_retention AS (
    SELECT 
        nu.user_key,
        -- Check if user was active in days 2-7
        CASE WHEN COUNT(fce2.engagement_id) > 0 THEN 1 ELSE 0 END as active_week_2_7
    FROM new_users nu
    LEFT JOIN fact_content_engagements fce2 ON (
        nu.user_key = fce2.user_key
        AND fce2.engagement_timestamp >= nu.registration_date + INTERVAL '1 day'
        AND fce2.engagement_timestamp < nu.registration_date + INTERVAL '7 days'
    )
    GROUP BY nu.user_key
)
SELECT 
    -- Segment by first-day activity level
    CASE 
        WHEN views_first_day >= 20 AND likes_first_day >= 5 THEN 'High Engagement'
        WHEN views_first_day >= 10 AND likes_first_day >= 2 THEN 'Medium Engagement'  
        WHEN views_first_day >= 1 THEN 'Low Engagement'
        ELSE 'No Engagement'
    END as first_day_segment,
    
    COUNT(*) as user_count,
    AVG(views_first_day) as avg_views,
    AVG(likes_first_day) as avg_likes,
    AVG(content_created_first_day) as avg_content_created,
    AVG(total_watch_time) as avg_watch_time_seconds,
    AVG(avg_completion_rate) as avg_completion_rate,
    
    -- Retention analysis
    AVG(ur.active_week_2_7::DECIMAL) as week_2_7_retention_rate,
    
    -- Success indicators
    SUM(CASE WHEN ur.active_week_2_7 = 1 THEN 1 ELSE 0 END) as retained_users,
    AVG(discovery_sources_tried) as avg_discovery_sources_used
    
FROM user_first_day_activity ufda
JOIN user_retention ur ON ufda.user_key = ur.user_key
GROUP BY first_day_segment
ORDER BY 
    CASE first_day_segment
        WHEN 'High Engagement' THEN 1
        WHEN 'Medium Engagement' THEN 2
        WHEN 'Low Engagement' THEN 3
        WHEN 'No Engagement' THEN 4
    END;
```

---

## Question 6: Hashtag Performance Analysis

**Problem**: Find the most effective hashtags for content discovery and engagement.

**Expected Output**: Hashtag performance metrics with trend analysis.

### Solution:
```sql
WITH hashtag_extraction AS (
    SELECT 
        dc.content_key,
        dc.category,
        dc.upload_timestamp,
        -- Extract individual hashtags from JSON array
        TRIM(hashtag.value, '"') as hashtag
    FROM dim_content dc
    CROSS JOIN JSON_ARRAY_ELEMENTS(dc.hashtags) as hashtag
    WHERE dc.upload_timestamp >= CURRENT_DATE - 14
),
hashtag_performance AS (
    SELECT 
        he.hashtag,
        he.category,
        COUNT(DISTINCT he.content_key) as content_using_hashtag,
        SUM(fcp.total_views) as total_views,
        SUM(fcp.total_likes + fcp.total_comments + fcp.total_shares) as total_engagements,
        AVG(fcp.completion_rate) as avg_completion_rate,
        AVG(fcp.viral_score) as avg_viral_score
    FROM hashtag_extraction he
    JOIN fact_content_performance fcp ON he.content_key = fcp.content_key
    JOIN dim_date dd ON fcp.date_key = dd.date_key
    WHERE dd.full_date >= CURRENT_DATE - 14
    GROUP BY he.hashtag, he.category
)
SELECT 
    hashtag,
    category,
    content_using_hashtag,
    total_views,
    total_engagements,
    
    -- Performance metrics
    ROUND(total_views::DECIMAL / content_using_hashtag, 0) as avg_views_per_content,
    ROUND(total_engagements::DECIMAL / content_using_hashtag, 0) as avg_engagements_per_content,
    ROUND((total_engagements::DECIMAL / NULLIF(total_views, 0)) * 100, 2) as engagement_rate_pct,
    ROUND(avg_completion_rate, 3) as avg_completion_rate,
    ROUND(avg_viral_score, 1) as avg_viral_score,
    
    -- Hashtag effectiveness score
    ROUND(
        (total_engagements::DECIMAL / content_using_hashtag) * 
        (avg_completion_rate) * 
        (1 + avg_viral_score / 100), 
        0
    ) as effectiveness_score
    
FROM hashtag_performance
WHERE content_using_hashtag >= 5  -- Filter for statistically significant hashtags
  AND LENGTH(hashtag) > 1  -- Filter out empty hashtags
ORDER BY effectiveness_score DESC
LIMIT 50;
```

## Practice Tips

1. **Schema Understanding**: Focus on the relationships between content, users, and engagement events
2. **Time-Based Analysis**: Many queries involve time windows and trend calculations
3. **JSON Handling**: Practice extracting data from JSON arrays (hashtags, effects)
4. **Performance Optimization**: Use appropriate indexes and consider query performance
5. **Statistical Significance**: Filter results to ensure meaningful sample sizes 