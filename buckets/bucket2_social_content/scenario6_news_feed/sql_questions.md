# Scenario 6: News Feed (Facebook/LinkedIn) - SQL Questions

## Database Schema Reference

Based on the News Feed data model:

### Dimension Tables
-   **`dim_users`**: `user_key`, `user_id`, `user_name`, `registration_date`, `region`, `user_preferences`
-   **`dim_content_sources`**: `source_key`, `source_id`, `source_type`, `source_name`, `category`
-   **`dim_posts`**: `post_key`, `post_id`, `source_key`, `creation_timestamp`, `content_type`, `post_text`, `media_url`, `post_metadata`, `is_sponsored`
-   **`dim_engagement_types`**: `engagement_type_key`, `engagement_name`, `engagement_weight`
-   **`dim_date`**: `date_key`, `full_date`, `year`, `month`, `day_of_month`, `hour`, `minute`, `is_peak_hour`

### Fact Tables
-   **`fact_feed_impressions`**: `impression_id`, `user_key`, `post_key`, `date_key`, `impression_timestamp`, `position_in_feed`, `feed_context`, `predicted_engagement_score`
-   **`fact_post_engagements`**: `engagement_id`, `user_key`, `post_key`, `engagement_type_key`, `date_key`, `engagement_timestamp`, `time_spent_seconds`, `comment_text`, `engagement_metadata`
-   **`fact_user_feedback`**: `feedback_id`, `user_key`, `post_key`, `date_key`, `feedback_type`, `feedback_reason`

---

## Question 1: Valid Post Reads & Engagement Analysis

**Problem**: Identify "valid post reads" (posts viewed for at least 3 seconds or posts with any other form of engagement like like/comment/share). Calculate engagement rates for these valid reads.

**Expected Output**: Post ID, total impressions, valid reads, valid read rate, and engagement rates (like, comment, share) per valid read.

### Solution (Adapted from `src/sql/q010_valid_post_reads.sql`):
```sql
WITH post_interactions AS (
    SELECT
        fi.post_key,
        fi.user_key,
        MAX(CASE 
            WHEN fe.engagement_type_key IS NOT NULL THEN 1
            ELSE 0
        END) as has_engagement,
        MAX(CASE 
            WHEN det.engagement_name = 'view' AND fe.time_spent_seconds >= 3 THEN 1
            ELSE 0 
        END) as has_sufficient_view_time
    FROM fact_feed_impressions fi
    LEFT JOIN fact_post_engagements fe ON fi.post_key = fe.post_key AND fi.user_key = fe.user_key
    LEFT JOIN dim_engagement_types det ON fe.engagement_type_key = det.engagement_type_key
    GROUP BY fi.post_key, fi.user_key
),
valid_reads_summary AS (
    SELECT 
        post_key,
        COUNT(*) as total_impressions,
        SUM(CASE WHEN has_engagement = 1 OR has_sufficient_view_time = 1 THEN 1 ELSE 0 END) as valid_reads
    FROM post_interactions
    GROUP BY post_key
),
engagement_counts AS (
    SELECT
        fe.post_key,
        det.engagement_name,
        COUNT(DISTINCT fe.user_key) as engagement_count -- Count distinct users engaging
    FROM fact_post_engagements fe
    JOIN dim_engagement_types det ON fe.engagement_type_key = det.engagement_type_key
    WHERE det.engagement_name IN ('like', 'comment', 'share')
    GROUP BY fe.post_key, det.engagement_name
)
SELECT 
    dp.post_id,
    vrs.total_impressions,
    vrs.valid_reads,
    ROUND(vrs.valid_reads * 100.0 / NULLIF(vrs.total_impressions, 0), 2) as valid_read_rate_pct,
    ROUND(MAX(CASE WHEN ec.engagement_name = 'like' THEN ec.engagement_count ELSE 0 END) * 100.0 / NULLIF(vrs.valid_reads, 0), 2) as like_rate_per_valid_read_pct,
    ROUND(MAX(CASE WHEN ec.engagement_name = 'comment' THEN ec.engagement_count ELSE 0 END) * 100.0 / NULLIF(vrs.valid_reads, 0), 2) as comment_rate_per_valid_read_pct,
    ROUND(MAX(CASE WHEN ec.engagement_name = 'share' THEN ec.engagement_count ELSE 0 END) * 100.0 / NULLIF(vrs.valid_reads, 0), 2) as share_rate_per_valid_read_pct
FROM dim_posts dp
JOIN valid_reads_summary vrs ON dp.post_key = vrs.post_key
LEFT JOIN engagement_counts ec ON dp.post_key = ec.post_key
WHERE vrs.total_impressions > 10 -- Filter for posts with some baseline visibility
GROUP BY dp.post_id, vrs.total_impressions, vrs.valid_reads
ORDER BY valid_read_rate_pct DESC, vrs.total_impressions DESC
LIMIT 100;
```

---

## Question 2: Content Source Performance

**Problem**: Analyze the performance of different content sources (users, pages, groups) in terms of engagement generated per post.

**Expected Output**: Source ID, source type, total posts, average likes per post, average comments per post, average shares per post.

### Solution:
```sql
WITH source_post_engagement AS (
    SELECT
        dcs.source_id,
        dcs.source_type,
        dp.post_key,
        SUM(CASE WHEN det.engagement_name = 'like' THEN 1 ELSE 0 END) as likes,
        SUM(CASE WHEN det.engagement_name = 'comment' THEN 1 ELSE 0 END) as comments,
        SUM(CASE WHEN det.engagement_name = 'share' THEN 1 ELSE 0 END) as shares
    FROM dim_content_sources dcs
    JOIN dim_posts dp ON dcs.source_key = dp.source_key
    LEFT JOIN fact_post_engagements fpe ON dp.post_key = fpe.post_key
    LEFT JOIN dim_engagement_types det ON fpe.engagement_type_key = det.engagement_type_key
    WHERE dp.creation_timestamp >= CURRENT_DATE - 30 -- Analyze recent posts
    GROUP BY dcs.source_id, dcs.source_type, dp.post_key
)
SELECT 
    source_id,
    source_type,
    COUNT(post_key) as total_posts,
    ROUND(AVG(likes), 2) as avg_likes_per_post,
    ROUND(AVG(comments), 2) as avg_comments_per_post,
    ROUND(AVG(shares), 2) as avg_shares_per_post,
    ROUND(AVG(likes + comments*2 + shares*3), 2) as avg_weighted_engagement_per_post -- Example weighted score
FROM source_post_engagement
GROUP BY source_id, source_type
HAVING COUNT(post_key) >= 5 -- Only sources with a minimum number of posts
ORDER BY avg_weighted_engagement_per_post DESC
LIMIT 100;
```

---

## Question 3: Feed Personalization Effectiveness (Negative Feedback Analysis)

**Problem**: Identify posts or content types that receive high negative feedback (hides, unfollows) relative to their impressions, indicating poor personalization for certain users.

**Expected Output**: Post ID, content type, impressions, negative feedback count, negative feedback rate.

### Solution:
```sql
WITH post_feedback_summary AS (
    SELECT
        fuf.post_key,
        COUNT(*) as total_negative_feedback_actions,
        SUM(CASE WHEN fuf.feedback_type = 'hide_post' THEN 1 ELSE 0 END) as hide_actions,
        SUM(CASE WHEN fuf.feedback_type = 'unfollow_source' THEN 1 ELSE 0 END) as unfollow_source_actions,
        SUM(CASE WHEN fuf.feedback_type = 'report_content' THEN 1 ELSE 0 END) as report_actions
    FROM fact_user_feedback fuf
    JOIN dim_date dd ON fuf.date_key = dd.date_key
    WHERE dd.full_date >= CURRENT_DATE - 30
    GROUP BY fuf.post_key
),
post_impression_summary AS (
    SELECT 
        post_key,
        COUNT(DISTINCT user_key) as total_impressions -- Unique users impressed
    FROM fact_feed_impressions
    WHERE impression_timestamp >= CURRENT_DATE - 30
    GROUP BY post_key
)
SELECT
    dp.post_id,
    dp.content_type,
    dcs.source_name as content_source_name,
    pis.total_impressions,
    COALESCE(pfs.total_negative_feedback_actions, 0) as total_negative_feedback,
    COALESCE(pfs.hide_actions, 0) as hides,
    COALESCE(pfs.unfollow_source_actions, 0) as unfollows,
    ROUND(COALESCE(pfs.total_negative_feedback_actions, 0) * 1000.0 / NULLIF(pis.total_impressions, 0), 2) as negative_feedback_per_1k_impressions
FROM dim_posts dp
JOIN post_impression_summary pis ON dp.post_key = pis.post_key
LEFT JOIN post_feedback_summary pfs ON dp.post_key = pfs.post_key
JOIN dim_content_sources dcs ON dp.source_key = dcs.source_key
WHERE pis.total_impressions > 100 -- Analyze posts with significant reach
ORDER BY negative_feedback_per_1k_impressions DESC, total_negative_feedback DESC
LIMIT 100;
```

---

## Question 4: Engagement by Feed Position and Context

**Problem**: Analyze how user engagement (e.g., click-through rate, time spent) varies by the position of the post in the feed and the context in which it was shown (organic, friend_activity, suggested).

**Expected Output**: Feed position bucket, feed context, average CTR, average time spent.

### Solution:
```sql
WITH impression_engagements AS (
    SELECT 
        ffi.impression_id,
        ffi.post_key,
        ffi.user_key,
        ffi.position_in_feed,
        ffi.feed_context,
        MAX(CASE WHEN det.engagement_name = 'click' THEN 1 ELSE 0 END) as has_click,
        MAX(CASE WHEN det.engagement_name = 'view' THEN fpe.time_spent_seconds ELSE 0 END) as time_spent_on_post
    FROM fact_feed_impressions ffi
    LEFT JOIN fact_post_engagements fpe ON ffi.post_key = fpe.post_key AND ffi.user_key = fpe.user_key AND ffi.impression_timestamp <= fpe.engagement_timestamp
    LEFT JOIN dim_engagement_types det ON fpe.engagement_type_key = det.engagement_type_key
    WHERE ffi.impression_timestamp >= CURRENT_DATE - 7
    GROUP BY ffi.impression_id, ffi.post_key, ffi.user_key, ffi.position_in_feed, ffi.feed_context
)
SELECT 
    CASE 
        WHEN position_in_feed BETWEEN 1 AND 3 THEN '1-3'
        WHEN position_in_feed BETWEEN 4 AND 10 THEN '4-10'
        WHEN position_in_feed BETWEEN 11 AND 20 THEN '11-20'
        ELSE '20+'
    END as feed_position_bucket,
    feed_context,
    COUNT(*) as total_impressions,
    ROUND(AVG(has_click) * 100.0, 2) as click_through_rate_pct,
    ROUND(AVG(time_spent_on_post), 1) as avg_time_spent_seconds
FROM impression_engagements
GROUP BY feed_position_bucket, feed_context
ORDER BY 
    CASE feed_position_bucket
        WHEN '1-3' THEN 1
        WHEN '4-10' THEN 2
        WHEN '11-20' THEN 3
        ELSE 4
    END,
    feed_context;
```

---

## Question 5: Peak Hour vs. Off-Peak Hour Engagement Patterns

**Problem**: Compare user engagement patterns (e.g., types of interactions, content types engaged with) during peak hours versus off-peak hours.

**Expected Output**: Time period (peak/off-peak), content type, average engagement counts (likes, comments, shares), total interactions.

### Solution:
```sql
SELECT 
    dd.is_peak_hour,
    dp.content_type,
    det.engagement_name,
    COUNT(fpe.engagement_id) as total_engagements,
    COUNT(DISTINCT fpe.user_key) as unique_engaging_users,
    ROUND(AVG(fpe.time_spent_seconds),1) as avg_time_spent_on_engagement
FROM fact_post_engagements fpe
JOIN dim_date dd ON fpe.date_key = dd.date_key
JOIN dim_posts dp ON fpe.post_key = dp.post_key
JOIN dim_engagement_types det ON fpe.engagement_type_key = det.engagement_type_key
WHERE dd.full_date >= CURRENT_DATE - 14
GROUP BY dd.is_peak_hour, dp.content_type, det.engagement_name
ORDER BY dd.is_peak_hour DESC, dp.content_type, total_engagements DESC;

-- Deeper dive into overall engagement per content type by peak hours
SELECT
    dd.is_peak_hour,
    dp.content_type,
    COUNT(DISTINCT fpe.post_key) as total_posts_engaged_with,
    COUNT(fpe.engagement_id) as total_engagement_actions,
    SUM(CASE WHEN det.engagement_name = 'like' THEN 1 ELSE 0 END) as total_likes,
    SUM(CASE WHEN det.engagement_name = 'comment' THEN 1 ELSE 0 END) as total_comments,
    SUM(CASE WHEN det.engagement_name = 'share' THEN 1 ELSE 0 END) as total_shares,
    SUM(fpe.time_spent_seconds) / 3600.0 as total_time_spent_hours
FROM fact_post_engagements fpe
JOIN dim_date dd ON fpe.date_key = dd.date_key
JOIN dim_posts dp ON fpe.post_key = dp.post_key
JOIN dim_engagement_types det ON fpe.engagement_type_key = det.engagement_type_key
WHERE dd.full_date >= CURRENT_DATE - 14
GROUP BY dd.is_peak_hour, dp.content_type
ORDER BY dd.is_peak_hour DESC, total_engagement_actions DESC;
```

---

## Question 6: Sponsored Post Performance vs. Organic Posts

**Problem**: Compare the engagement metrics (CTR, conversion rates if applicable, engagement types) of sponsored posts versus organic posts within similar content categories.

**Expected Output**: Content category, post type (sponsored/organic), average CTR, average engagement rate.

### Solution:
```sql
WITH post_engagement_summary AS (
    SELECT
        dp.post_key,
        dp.is_sponsored,
        dcs.category as content_category, -- Assuming content_sources has a category
        COUNT(DISTINCT ffi.impression_id) as total_impressions,
        COUNT(DISTINCT CASE WHEN det.engagement_name = 'click' THEN fpe.engagement_id END) as total_clicks,
        COUNT(DISTINCT fpe.engagement_id) as total_engagements -- All types of engagements
    FROM dim_posts dp
    JOIN dim_content_sources dcs ON dp.source_key = dcs.source_key
    LEFT JOIN fact_feed_impressions ffi ON dp.post_key = ffi.post_key
    LEFT JOIN fact_post_engagements fpe ON dp.post_key = fpe.post_key AND ffi.user_key = fpe.user_key
    LEFT JOIN dim_engagement_types det ON fpe.engagement_type_key = det.engagement_type_key
    WHERE dp.creation_timestamp >= CURRENT_DATE - 30
    GROUP BY dp.post_key, dp.is_sponsored, dcs.category
)
SELECT 
    content_category,
    CASE WHEN is_sponsored THEN 'Sponsored' ELSE 'Organic' END as post_origin_type,
    COUNT(post_key) as number_of_posts,
    SUM(total_impressions) as sum_total_impressions,
    SUM(total_engagements) as sum_total_engagements,
    SUM(total_clicks) as sum_total_clicks,
    ROUND(SUM(total_clicks) * 100.0 / NULLIF(SUM(total_impressions), 0), 3) as avg_click_through_rate_pct,
    ROUND(SUM(total_engagements) * 100.0 / NULLIF(SUM(total_impressions), 0), 3) as avg_engagement_rate_pct -- Engagements per impression
FROM post_engagement_summary
WHERE total_impressions > 50 -- Filter for posts with sufficient impressions
GROUP BY content_category, post_origin_type
ORDER BY content_category, post_origin_type;
``` 