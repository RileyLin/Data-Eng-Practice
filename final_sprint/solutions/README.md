# Meta Data Engineer Interview - Final Sprint Solutions
## Complete Solutions for All Practice Scenarios

**Complete solutions with Meta-level thinking and follow-up discussions**

---

## 📊 Solution Set 1: DAU/MAU Engagement Funnel

### Solution 1.1: Product Sense - Engagement Analysis

**Problem**: Meta's News Feed DAU/MAU ratio dropped from 0.65 to 0.58. Investigate root causes.

#### Part A: Key Metrics to Investigate

1. **User Retention Funnel**
   - **Day 1/7/30 Retention Rates** - % of new users returning after N days
   - *Why*: Declining stickiness often starts with poor onboarding
   - *Target*: D1 >40%, D7 >20%, D30 >10%

2. **Session Quality Metrics**
   - **Average Session Duration** - Time spent per News Feed visit
   - **Feed Scroll Depth** - How far users scroll before leaving
   - **Post Engagement Rate** - % of viewed posts receiving interactions
   - *Why*: Lower quality content leads to shorter, less engaging sessions

3. **Feature Usage Distribution**
   - **Stories vs Feed Time Split** - Are users migrating to other surfaces?
   - **Creator vs Friend Content Ratio** - Is algorithm over-indexing on creators?
   - *Why*: Users might be shifting consumption patterns

#### Part B: Root Cause Investigation Framework

1. **Algorithm Changes**
   - *Hypothesis*: Recent ranking updates reduced content relevance
   - *Evidence*: Check A/B test logs, content diversity metrics, user feedback
   - *Deep Dive*: Analyze engagement rates by content type, recency, creator tier

2. **Content Supply Issues**
   - *Hypothesis*: Friend posting frequency declined or content quality dropped
   - *Evidence*: Posts per user trends, content moderation actions, creator metrics
   - *Deep Dive*: Segment by user type (heavy posters vs lurkers)

3. **Competitive Pressure**
   - *Hypothesis*: Users migrating time to TikTok/YouTube/other platforms
   - *Evidence*: User surveys, usage patterns by demographics, retention by cohort
   - *Deep Dive*: Cross-platform usage analysis (where legally possible)

#### Part C: A/B Test Design - News Feed Relevance Experiment

**Intervention**: Increase weight of friend posts vs algorithmic recommendations

**Test Setup**:
- **Control (50%)**: Current News Feed algorithm
- **Treatment (50%)**: 70% friend posts, 30% algorithmic content (vs current 50/50)
- **Duration**: 3 weeks for statistical significance
- **Population**: Active users (logged in last 7 days)

**Primary Metrics**:
- **DAU/MAU Ratio** (target: +5% relative improvement)
- **News Feed Session Duration** (target: +10%)
- **Feed Scroll Depth** (target: +15%)

**Guardrail Metrics**:
- **Overall Platform Time** (should not decrease >2%)
- **Creator Content Engagement** (should not decrease >10%)
- **User Complaints/Negative Feedback** (should not increase >20%)

### Solution 1.2: Data Modeling - User Activity Schema

#### Part A: Core Schema Design

```sql
-- User activity fact table (high volume, time-partitioned)
fact_user_sessions (
    session_id VARCHAR(50) PRIMARY KEY,
    user_id BIGINT NOT NULL,
    session_start_ts TIMESTAMP NOT NULL,
    session_end_ts TIMESTAMP,
    
    -- Session characteristics
    platform_type VARCHAR(20), -- 'ios', 'android', 'web'
    entry_point VARCHAR(30),   -- 'notification', 'direct', 'bookmark'
    
    -- Engagement aggregates
    posts_viewed INT DEFAULT 0,
    posts_liked INT DEFAULT 0,
    posts_shared INT DEFAULT 0,
    posts_commented INT DEFAULT 0,
    stories_viewed INT DEFAULT 0,
    
    -- Session quality metrics
    total_scroll_distance_px INT DEFAULT 0,
    max_scroll_depth_pct DECIMAL(5,2) DEFAULT 0,
    session_bounce_flag BOOLEAN DEFAULT FALSE,
    
    -- For DAU/MAU calculations
    date_partition DATE NOT NULL,
    hour_partition INT NOT NULL
)
PARTITION BY date_partition;

-- User-level daily aggregation (for fast DAU/MAU queries)
fact_user_daily_activity (
    user_id BIGINT,
    activity_date DATE,
    
    -- Activity flags
    is_dau BOOLEAN DEFAULT FALSE,
    is_feed_active BOOLEAN DEFAULT FALSE,
    is_stories_active BOOLEAN DEFAULT FALSE,
    is_creator BOOLEAN DEFAULT FALSE,
    
    -- Daily aggregates
    total_sessions INT DEFAULT 0,
    total_time_spent_minutes INT DEFAULT 0,
    posts_created INT DEFAULT 0,
    engagement_events INT DEFAULT 0,
    
    PRIMARY KEY (user_id, activity_date)
)
PARTITION BY activity_date;

-- User cohort dimension (for retention analysis)
dim_user_cohorts (
    user_id BIGINT PRIMARY KEY,
    registration_date DATE NOT NULL,
    cohort_month VARCHAR(7), -- 'YYYY-MM'
    acquisition_channel VARCHAR(50),
    user_segment VARCHAR(30), -- 'creator', 'casual', 'heavy_consumer'
    
    -- Lifecycle metrics (updated daily)
    days_since_registration INT,
    lifetime_sessions INT,
    last_active_date DATE,
    is_retained_d1 BOOLEAN,
    is_retained_d7 BOOLEAN,
    is_retained_d30 BOOLEAN
);
```

#### Part B: DAU/MAU Calculation Strategy

**Real-time DAU/MAU Pipeline**:
1. **Stream Processing**: Update `fact_user_daily_activity` in real-time as events arrive
2. **Daily Batch Job**: Calculate rolling 30-day MAU for each user
3. **Hourly Aggregation**: Compute DAU/MAU ratio with 1-hour freshness

```sql
-- Optimized DAU/MAU query
WITH daily_active AS (
    SELECT 
        activity_date,
        COUNT(DISTINCT user_id) as dau
    FROM fact_user_daily_activity 
    WHERE 
        activity_date >= CURRENT_DATE - INTERVAL '30 days'
        AND is_dau = true
    GROUP BY activity_date
),
monthly_active AS (
    SELECT 
        activity_date,
        COUNT(DISTINCT user_id) as mau
    FROM fact_user_daily_activity 
    WHERE 
        activity_date BETWEEN 
            (activity_date - INTERVAL '29 days') AND activity_date
        AND is_dau = true
    GROUP BY activity_date
)
SELECT 
    d.activity_date,
    d.dau,
    m.mau,
    ROUND(d.dau::DECIMAL / m.mau, 3) as dau_mau_ratio
FROM daily_active d
JOIN monthly_active m ON d.activity_date = m.activity_date
ORDER BY d.activity_date;
```

### Solution 1.3: SQL Analytics - Retention & Funnel Analysis

#### Query 1: Cohort Retention Analysis

```sql
WITH user_cohorts AS (
    SELECT 
        user_id,
        DATE_TRUNC('month', registration_date) as cohort_month,
        registration_date
    FROM dim_user_cohorts
    WHERE registration_date >= '2024-01-01'
),
user_activity_periods AS (
    SELECT 
        c.user_id,
        c.cohort_month,
        a.activity_date,
        DATE_PART('day', a.activity_date - c.registration_date) as days_since_reg
    FROM user_cohorts c
    LEFT JOIN fact_user_daily_activity a 
        ON c.user_id = a.user_id 
        AND a.is_dau = true
        AND a.activity_date BETWEEN c.registration_date AND c.registration_date + INTERVAL '30 days'
),
retention_matrix AS (
    SELECT 
        cohort_month,
        COUNT(DISTINCT user_id) as cohort_size,
        COUNT(DISTINCT CASE WHEN days_since_reg >= 1 THEN user_id END) as retained_d1,
        COUNT(DISTINCT CASE WHEN days_since_reg >= 7 THEN user_id END) as retained_d7,
        COUNT(DISTINCT CASE WHEN days_since_reg >= 30 THEN user_id END) as retained_d30
    FROM user_activity_periods
    GROUP BY cohort_month
)
SELECT 
    cohort_month,
    cohort_size,
    ROUND(100.0 * retained_d1 / cohort_size, 2) as d1_retention_pct,
    ROUND(100.0 * retained_d7 / cohort_size, 2) as d7_retention_pct,
    ROUND(100.0 * retained_d30 / cohort_size, 2) as d30_retention_pct
FROM retention_matrix
WHERE cohort_size >= 1000  -- Filter small cohorts
ORDER BY cohort_month;
```

#### Query 2: User Engagement Funnel

```sql
WITH session_funnel AS (
    SELECT 
        s.session_id,
        s.user_id,
        s.date_partition,
        
        -- Funnel steps
        CASE WHEN s.posts_viewed > 0 THEN 1 ELSE 0 END as step_1_viewed,
        CASE WHEN s.posts_liked > 0 OR s.posts_shared > 0 OR s.posts_commented > 0 
             THEN 1 ELSE 0 END as step_2_engaged,
        CASE WHEN s.posts_shared > 0 OR s.posts_commented > 0 
             THEN 1 ELSE 0 END as step_3_shared_commented,
        CASE WHEN s.max_scroll_depth_pct > 50 THEN 1 ELSE 0 END as step_4_deep_scroll
        
    FROM fact_user_sessions s
    WHERE s.date_partition >= CURRENT_DATE - INTERVAL '7 days'
),
daily_funnel_metrics AS (
    SELECT 
        date_partition,
        COUNT(*) as total_sessions,
        SUM(step_1_viewed) as viewed_content,
        SUM(step_2_engaged) as engaged_with_content,
        SUM(step_3_shared_commented) as shared_or_commented,
        SUM(step_4_deep_scroll) as deep_scrolled
    FROM session_funnel
    GROUP BY date_partition
)
SELECT 
    date_partition,
    total_sessions,
    
    -- Conversion rates
    ROUND(100.0 * viewed_content / total_sessions, 2) as view_rate_pct,
    ROUND(100.0 * engaged_with_content / total_sessions, 2) as engagement_rate_pct,
    ROUND(100.0 * shared_or_commented / total_sessions, 2) as share_comment_rate_pct,
    ROUND(100.0 * deep_scrolled / total_sessions, 2) as deep_scroll_rate_pct,
    
    -- Drop-off analysis
    ROUND(100.0 * (total_sessions - viewed_content) / total_sessions, 2) as bounce_rate_pct
FROM daily_funnel_metrics
ORDER BY date_partition;
```

### Solution 1.4: Python Processing - Engagement Pipeline

```python
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import json
from collections import defaultdict

class UserEngagementProcessor:
    """Real-time user engagement metrics processor for DAU/MAU tracking"""
    
    def __init__(self):
        self.user_sessions = defaultdict(dict)  # user_id -> session_data
        self.daily_metrics = defaultdict(lambda: {
            'dau': set(),
            'sessions': 0,
            'total_engagement': 0
        })
        
    def process_user_event(self, event_data: Dict) -> Optional[Dict]:
        """Process user activity event and update engagement metrics"""
        try:
            user_id = event_data['user_id']
            session_id = event_data['session_id']
            event_type = event_data['event_type']
            timestamp = datetime.fromisoformat(event_data['timestamp'])
            date_key = timestamp.date()
            
            # Initialize session if not exists
            if session_id not in self.user_sessions[user_id]:
                self.user_sessions[user_id][session_id] = {
                    'start_time': timestamp,
                    'last_activity': timestamp,
                    'posts_viewed': 0,
                    'posts_liked': 0,
                    'posts_shared': 0,
                    'posts_commented': 0,
                    'scroll_events': 0,
                    'is_bounce': True
                }
                self.daily_metrics[date_key]['sessions'] += 1
            
            session = self.user_sessions[user_id][session_id]
            session['last_activity'] = timestamp
            
            # Update session metrics based on event type
            if event_type == 'post_view':
                session['posts_viewed'] += 1
                session['is_bounce'] = False
                self.daily_metrics[date_key]['dau'].add(user_id)
                
            elif event_type == 'post_like':
                session['posts_liked'] += 1
                self.daily_metrics[date_key]['total_engagement'] += 1
                
            elif event_type == 'post_share':
                session['posts_shared'] += 1
                self.daily_metrics[date_key]['total_engagement'] += 3  # Higher weight
                
            elif event_type == 'post_comment':
                session['posts_commented'] += 1
                self.daily_metrics[date_key]['total_engagement'] += 5  # Highest weight
                
            elif event_type == 'scroll':
                session['scroll_events'] += 1
                
            return self._calculate_session_health(user_id, session_id)
            
        except (KeyError, ValueError, TypeError) as e:
            return None
    
    def _calculate_session_health(self, user_id: int, session_id: str) -> Dict:
        """Calculate session engagement health score"""
        session = self.user_sessions[user_id][session_id]
        
        # Session duration in minutes
        duration_minutes = (session['last_activity'] - session['start_time']).total_seconds() / 60
        
        # Engagement score calculation
        engagement_score = (
            session['posts_viewed'] * 1 +
            session['posts_liked'] * 2 +
            session['posts_shared'] * 4 +
            session['posts_commented'] * 6
        )
        
        # Health categorization
        if engagement_score >= 20 and duration_minutes >= 5:
            health_status = 'highly_engaged'
        elif engagement_score >= 10 and duration_minutes >= 2:
            health_status = 'moderately_engaged'
        elif engagement_score >= 3:
            health_status = 'lightly_engaged'
        else:
            health_status = 'at_risk'
        
        return {
            'user_id': user_id,
            'session_id': session_id,
            'duration_minutes': round(duration_minutes, 2),
            'engagement_score': engagement_score,
            'health_status': health_status,
            'is_bounce': session['is_bounce']
        }
    
    def get_daily_metrics(self, date: datetime.date) -> Dict:
        """Get aggregated daily metrics for DAU/MAU calculation"""
        metrics = self.daily_metrics[date]
        
        return {
            'date': str(date),
            'dau_count': len(metrics['dau']),
            'total_sessions': metrics['sessions'],
            'total_engagement_events': metrics['total_engagement'],
            'avg_engagement_per_session': round(
                metrics['total_engagement'] / max(metrics['sessions'], 1), 2
            )
        }
    
    def calculate_dau_mau_ratio(self, current_date: datetime.date) -> Dict:
        """Calculate DAU/MAU ratio for current date"""
        # Get 30-day window for MAU calculation
        mau_users = set()
        total_dau = 0
        
        for i in range(30):
            check_date = current_date - timedelta(days=i)
            if check_date in self.daily_metrics:
                if i == 0:  # Today's DAU
                    total_dau = len(self.daily_metrics[check_date]['dau'])
                mau_users.update(self.daily_metrics[check_date]['dau'])
        
        mau_count = len(mau_users)
        dau_mau_ratio = total_dau / mau_count if mau_count > 0 else 0
        
        return {
            'date': str(current_date),
            'dau': total_dau,
            'mau': mau_count,
            'dau_mau_ratio': round(dau_mau_ratio, 3)
        }

def detect_engagement_anomalies(daily_metrics: List[Dict], 
                              window_days: int = 7,
                              threshold_pct: float = 15.0) -> List[Dict]:
    """Detect significant drops in engagement metrics"""
    anomalies = []
    
    if len(daily_metrics) < window_days + 1:
        return anomalies
    
    for i in range(window_days, len(daily_metrics)):
        current_day = daily_metrics[i]
        
        # Calculate baseline from previous window
        baseline_dau = sum(daily_metrics[j]['dau_count'] 
                          for j in range(i - window_days, i)) / window_days
        baseline_engagement = sum(daily_metrics[j]['avg_engagement_per_session'] 
                                for j in range(i - window_days, i)) / window_days
        
        # Check for significant drops
        dau_drop_pct = (baseline_dau - current_day['dau_count']) / baseline_dau * 100
        engagement_drop_pct = (baseline_engagement - current_day['avg_engagement_per_session']) / baseline_engagement * 100
        
        if dau_drop_pct > threshold_pct or engagement_drop_pct > threshold_pct:
            anomalies.append({
                'date': current_day['date'],
                'dau_drop_pct': round(dau_drop_pct, 2),
                'engagement_drop_pct': round(engagement_drop_pct, 2),
                'severity': 'high' if max(dau_drop_pct, engagement_drop_pct) > 25 else 'medium'
            })
    
    return anomalies

# Test the processor
if __name__ == "__main__":
    processor = UserEngagementProcessor()
    
    # Sample events
    test_events = [
        {'user_id': 1, 'session_id': 'sess_1', 'event_type': 'post_view', 'timestamp': '2024-01-15T10:00:00'},
        {'user_id': 1, 'session_id': 'sess_1', 'event_type': 'post_like', 'timestamp': '2024-01-15T10:01:00'},
        {'user_id': 2, 'session_id': 'sess_2', 'event_type': 'post_view', 'timestamp': '2024-01-15T10:02:00'},
    ]
    
    for event in test_events:
        result = processor.process_user_event(event)
        if result:
            print(f"Session Health: {result}")
    
    # Get daily metrics
    metrics = processor.get_daily_metrics(datetime(2024, 1, 15).date())
    print(f"Daily Metrics: {metrics}")
```

---

## 🎬 Solution Set 2: Reels Session Analytics Scenario

**Complete solutions with Meta-level thinking and follow-up discussions**

---

## Solution 1: Product Sense - Session Duration Analysis

### Part A: Key Metrics to Investigate

1. **Video Skip Rate** - % of videos skipped within first 3 seconds
   - *Why*: If content quality dropped, users skip faster
   - *Target*: <25% skip rate for healthy engagement

2. **Session Video Count Distribution** - # videos per session histogram  
   - *Why*: Shows where users drop off in the session
   - *Target*: Modal session should be 4-6 videos

3. **Time-to-Next-Video** - Seconds between video completions
   - *Why*: Algorithm delays or poor recommendations increase gaps
   - *Target*: <2 seconds average between videos

### Part B: Root Cause Hypotheses

1. **Algorithm Change** - Recommendation model update degraded relevance
   - *Evidence*: Check A/B test logs, recommendation click-through rates
   - *Impact*: Poor recommendations → users leave faster

2. **Content Supply Issue** - Creator uploads declined or quality dropped
   - *Evidence*: Upload volume, creator engagement rates, content moderation flags
   - *Impact*: Less engaging content available → shorter sessions

3. **Technical Performance** - Video loading latency increased
   - *Evidence*: Video start time metrics, error rates, device performance
   - *Impact*: Slow loading frustrates users → session abandonment

### Part C: A/B Test Design

**Intervention**: Reduce recommendation latency by pre-loading next 3 videos

**Test Setup**:
- **Control**: Current lazy-loading approach
- **Treatment**: Pre-load next 3 videos when user starts watching
- **Split**: 50/50 random assignment
- **Duration**: 2 weeks

**Success Metrics**:
- **Primary**: Average session duration (+10% target)
- **Secondary**: Videos per session, time-to-next-video
- **Guardrails**: App crash rate, data usage, battery drain

### Follow-up Discussion

**Prioritization Framework**:
1. **Impact × Confidence × Ease**
2. Algorithm changes first (high impact, measurable)
3. Technical issues second (quick wins)
4. Content supply last (longer-term fix)

---

## Solution 2: Data Modeling - Reels Analytics Schema

### Part A: Core Schema Design

```sql
-- Fact Tables (Event-driven, high volume)
fact_reels_events (
    event_id VARCHAR(50) PRIMARY KEY,
    user_id BIGINT NOT NULL,
    video_id BIGINT NOT NULL, 
    creator_id BIGINT NOT NULL,
    session_id VARCHAR(50) NOT NULL,
    event_type VARCHAR(20) NOT NULL, -- 'view_start', 'view_end', 'like', 'share', 'comment'
    event_timestamp TIMESTAMP NOT NULL,
    
    -- Event-specific data
    view_duration_ms INT,
    video_position_pct DECIMAL(5,2),
    device_type VARCHAR(20),
    
    -- Partitioning
    date_partition DATE NOT NULL,
    hour_partition INT NOT NULL
);

-- Session aggregation table (Pre-computed for performance)
fact_reels_sessions (
    session_id VARCHAR(50) PRIMARY KEY,
    user_id BIGINT NOT NULL,
    session_start_ts TIMESTAMP NOT NULL,
    session_end_ts TIMESTAMP NOT NULL,
    
    -- Aggregated metrics
    videos_watched INT,
    total_watch_time_seconds INT,
    unique_creators_watched INT,
    engagement_events_count INT,
    
    -- Session outcomes
    session_completed_flag BOOLEAN,
    last_video_completion_pct DECIMAL(5,2),
    
    date_partition DATE NOT NULL
);

-- Dimension Tables (Slowly changing, lower volume)
dim_videos (
    video_id BIGINT PRIMARY KEY,
    creator_id BIGINT NOT NULL,
    upload_timestamp TIMESTAMP NOT NULL,
    video_duration_seconds INT,
    video_category VARCHAR(50),
    content_rating VARCHAR(10),
    
    -- Content features for ML
    thumbnail_url VARCHAR(500),
    has_music BOOLEAN,
    video_quality VARCHAR(10)
);

dim_creators (
    creator_id BIGINT PRIMARY KEY,
    creator_username VARCHAR(100),
    follower_count BIGINT,
    verification_status VARCHAR(20),
    join_date DATE,
    creator_tier VARCHAR(20), -- 'rising', 'established', 'top'
    
    -- Creator performance (updated daily)
    avg_video_engagement_rate DECIMAL(5,4),
    total_videos_posted INT
);

dim_users (
    user_id BIGINT PRIMARY KEY,
    registration_date DATE,
    country_code VARCHAR(2),
    age_group VARCHAR(20),
    
    -- User preferences (updated in real-time)
    preferred_categories JSON,
    follower_count INT,
    avg_session_duration_minutes DECIMAL(6,2)
);
```

### Part B: Partitioning Strategy

**fact_reels_events**: 
- **Primary**: Date partition (daily) for time-based queries
- **Secondary**: Hour partition for real-time processing
- **Retention**: 90 days hot, 2 years cold storage

**fact_reels_sessions**:
- **Primary**: Date partition (daily)
- **Retention**: 1 year hot storage

**Rationale**: 
- Most queries are time-bound (last 7/30 days)
- Hourly sub-partitions enable efficient real-time aggregation
- Separate session table avoids expensive GROUP BY on raw events

### Part C: Late Data Handling

**Strategy**: Lambda architecture with reconciliation

1. **Real-time Stream**: Process events as they arrive (95% of data)
2. **Batch Reconciliation**: Daily job reprocesses last 3 days
3. **Late Data Detection**: Compare stream vs batch results
4. **Correction Pipeline**: Update downstream aggregations when discrepancies found

**Implementation**:
```python
# Pseudo-code for late data handling
def handle_late_event(event, current_time):
    if event.timestamp < current_time - 24_hours:
        # Route to batch reconciliation queue
        send_to_batch_queue(event)
    else:
        # Process in real-time stream
        process_realtime(event)
```

### Follow-up: Viral Share Chains

```sql
-- Recursive share lineage table
fact_share_chains (
    share_id VARCHAR(50) PRIMARY KEY,
    original_video_id BIGINT,
    parent_share_id VARCHAR(50), -- NULL for original post
    sharing_user_id BIGINT,
    receiving_user_id BIGINT,
    share_timestamp TIMESTAMP,
    share_depth INT, -- How many degrees from original
    
    -- Viral metrics
    views_generated_24h INT,
    subsequent_shares_24h INT
);
```

---

## Solution 3: SQL Analytics - Performance Queries

### Query 1: Session Completion Rate

```sql
WITH daily_sessions AS (
    SELECT 
        date_partition,
        session_id,
        COUNT(DISTINCT video_id) AS videos_watched
    FROM fact_reels_events 
    WHERE 
        date_partition >= CURRENT_DATE - INTERVAL '7 days'
        AND event_type = 'view_start'
    GROUP BY date_partition, session_id
),
completion_stats AS (
    SELECT 
        date_partition,
        COUNT(*) AS total_sessions,
        COUNT(CASE WHEN videos_watched >= 3 THEN 1 END) AS completed_sessions
    FROM daily_sessions
    GROUP BY date_partition
)
SELECT 
    date_partition,
    total_sessions,
    completed_sessions,
    ROUND(
        100.0 * completed_sessions / total_sessions, 
        2
    ) AS completion_rate_pct
FROM completion_stats
ORDER BY date_partition;
```

**Optimization Notes**:
- Use pre-aggregated `fact_reels_sessions` table for better performance
- Add index on `(date_partition, event_type, video_id)`

### Query 2: Video Engagement Score

```sql
WITH video_engagement AS (
    SELECT 
        e.video_id,
        v.creator_id,
        v.video_duration_seconds,
        v.video_category,
        
        -- Weighted engagement score calculation
        SUM(CASE 
            WHEN e.event_type = 'view_start' THEN 1
            WHEN e.event_type = 'like' THEN 3
            WHEN e.event_type = 'share' THEN 5
            WHEN e.event_type = 'comment' THEN 7
            ELSE 0
        END) AS engagement_score,
        
        -- View count for filtering
        COUNT(CASE WHEN e.event_type = 'view_start' THEN 1 END) AS view_count
        
    FROM fact_reels_events e
    INNER JOIN dim_videos v ON e.video_id = v.video_id
    WHERE 
        e.date_partition >= CURRENT_DATE - INTERVAL '30 days'
        AND v.upload_timestamp >= CURRENT_DATE - INTERVAL '30 days'
    GROUP BY 
        e.video_id, v.creator_id, v.video_duration_seconds, v.video_category
    HAVING 
        COUNT(CASE WHEN e.event_type = 'view_start' THEN 1 END) >= 100
)
SELECT 
    video_id,
    creator_id,
    video_duration_seconds,
    video_category,
    engagement_score,
    view_count,
    RANK() OVER (ORDER BY engagement_score DESC) AS engagement_rank
FROM video_engagement
ORDER BY engagement_score DESC
LIMIT 1000;
```

### Query 3: Creator Trend Analysis

```sql
WITH weekly_creator_engagement AS (
    SELECT 
        c.creator_id,
        c.creator_username,
        DATE_TRUNC('week', e.event_timestamp) AS week_start,
        COUNT(*) AS total_engagement_events
    FROM fact_reels_events e
    INNER JOIN dim_creators c ON e.creator_id = c.creator_id
    WHERE 
        e.date_partition >= CURRENT_DATE - INTERVAL '14 days'
        AND c.follower_count >= 1000
        AND e.event_type IN ('like', 'share', 'comment', 'view_start')
    GROUP BY 
        c.creator_id, c.creator_username, DATE_TRUNC('week', e.event_timestamp)
),
weekly_growth AS (
    SELECT 
        creator_id,
        creator_username,
        week_start,
        total_engagement_events,
        LAG(total_engagement_events) OVER (
            PARTITION BY creator_id 
            ORDER BY week_start
        ) AS prev_week_engagement,
        
        ROUND(
            100.0 * (total_engagement_events - LAG(total_engagement_events) OVER (
                PARTITION BY creator_id ORDER BY week_start
            )) / NULLIF(LAG(total_engagement_events) OVER (
                PARTITION BY creator_id ORDER BY week_start
            ), 0),
            2
        ) AS week_over_week_growth_pct
    FROM weekly_creator_engagement
)
SELECT 
    creator_id,
    creator_username,
    week_start,
    total_engagement_events,
    prev_week_engagement,
    week_over_week_growth_pct
FROM weekly_growth
WHERE 
    prev_week_engagement IS NOT NULL  -- Exclude first week (no comparison)
    AND week_start = (SELECT MAX(week_start) FROM weekly_growth)  -- Latest week only
ORDER BY week_over_week_growth_pct DESC
LIMIT 100;
```

### Performance Optimizations

**For Real-time Dashboard**:
1. **Pre-aggregated Tables**: Create hourly/daily rollups
2. **Materialized Views**: Refresh every 15 minutes
3. **Column Store**: Use Clickhouse/BigQuery for analytics
4. **Caching Layer**: Redis for frequently accessed metrics

---

## Solution 4: Python Data Processing

### Part A: Event Parser

```python
import json
from datetime import datetime
from typing import Optional, Dict, Any

def parse_event(event_json: str) -> Optional[Dict[str, Any]]:
    """
    Parse and validate Reels engagement event
    Return None for invalid events
    """
    try:
        event = json.loads(event_json)
        
        # Required fields validation
        required_fields = ['event_id', 'event_type', 'user_id', 'video_id', 'timestamp']
        for field in required_fields:
            if field not in event or event[field] is None:
                return None
        
        # Data type validation
        if not isinstance(event['user_id'], int) or event['user_id'] <= 0:
            return None
        if not isinstance(event['video_id'], int) or event['video_id'] <= 0:
            return None
        
        # Timestamp validation and conversion
        try:
            timestamp = datetime.fromisoformat(event['timestamp'].replace('Z', '+00:00'))
            event['parsed_timestamp'] = timestamp
        except (ValueError, AttributeError):
            return None
        
        # Event type validation
        valid_event_types = {'video_view', 'like', 'share', 'comment', 'follow'}
        if event['event_type'] not in valid_event_types:
            return None
        
        # Extract metadata safely
        metadata = event.get('metadata', {})
        event['view_duration_ms'] = metadata.get('view_duration_ms', 0)
        event['video_position'] = metadata.get('video_position', 0.0)
        
        return event
        
    except (json.JSONDecodeError, KeyError, TypeError):
        return None
```

### Part B: Rolling Metrics Calculator

```python
from collections import defaultdict, deque
from datetime import datetime, timedelta
from typing import Dict, Any
import threading

class UserMetricsTracker:
    def __init__(self, window_hours: int = 24):
        self.window_hours = window_hours
        self.user_events = defaultdict(deque)  # user_id -> deque of events
        self.user_metrics = defaultdict(lambda: {
            'videos_watched': 0,
            'total_engagement_time_minutes': 0.0,
            'likes': 0,
            'views': 0
        })
        self.lock = threading.RLock()  # Thread-safe for concurrent access
        
    def _clean_old_events(self, user_id: int, current_time: datetime):
        """Remove events older than window_hours"""
        cutoff_time = current_time - timedelta(hours=self.window_hours)
        user_queue = self.user_events[user_id]
        
        while user_queue and user_queue[0]['parsed_timestamp'] < cutoff_time:
            old_event = user_queue.popleft()
            self._decrement_metrics(user_id, old_event)
    
    def _decrement_metrics(self, user_id: int, event: Dict[str, Any]):
        """Remove old event from user metrics"""
        metrics = self.user_metrics[user_id]
        
        if event['event_type'] == 'video_view':
            metrics['videos_watched'] -= 1
            view_minutes = event.get('view_duration_ms', 0) / (1000 * 60)
            metrics['total_engagement_time_minutes'] -= view_minutes
            metrics['views'] -= 1
        elif event['event_type'] == 'like':
            metrics['likes'] -= 1
            
    def _increment_metrics(self, user_id: int, event: Dict[str, Any]):
        """Add new event to user metrics"""
        metrics = self.user_metrics[user_id]
        
        if event['event_type'] == 'video_view':
            metrics['videos_watched'] += 1
            view_minutes = event.get('view_duration_ms', 0) / (1000 * 60)
            metrics['total_engagement_time_minutes'] += view_minutes
            metrics['views'] += 1
        elif event['event_type'] == 'like':
            metrics['likes'] += 1
        
    def update_user_metrics(self, user_id: int, event: Dict[str, Any]):
        """Update rolling 24-hour metrics for user"""
        with self.lock:
            current_time = event['parsed_timestamp']
            
            # Clean old events first
            self._clean_old_events(user_id, current_time)
            
            # Add new event
            self.user_events[user_id].append(event)
            self._increment_metrics(user_id, event)
        
    def get_user_metrics(self, user_id: int) -> Dict[str, Any]:
        """Get current 24-hour metrics for user"""
        with self.lock:
            # Clean old events before returning metrics
            current_time = datetime.utcnow()
            self._clean_old_events(user_id, current_time)
            
            metrics = self.user_metrics[user_id].copy()
            
            # Calculate engagement rate
            if metrics['views'] > 0:
                metrics['engagement_rate'] = metrics['likes'] / metrics['views']
            else:
                metrics['engagement_rate'] = 0.0
                
            return metrics
```

### Part C: Viral Video Detector

```python
from collections import defaultdict
from datetime import datetime, timedelta
from typing import List, Dict, Any

def detect_viral_videos(events: List[Dict[str, Any]], 
                       window_hours: int = 2,
                       viral_threshold: float = 1.5,
                       min_views: int = 1000) -> List[int]:
    """
    Return list of video_ids that are trending
    Based on recent engagement patterns
    """
    current_time = datetime.utcnow()
    cutoff_time = current_time - timedelta(hours=window_hours)
    
    # Filter to recent events only
    recent_events = [
        event for event in events 
        if event.get('parsed_timestamp', datetime.min) >= cutoff_time
    ]
    
    # Aggregate metrics per video
    video_metrics = defaultdict(lambda: {
        'views': 0,
        'shares': 0, 
        'comments': 0,
        'viral_coefficient': 0.0
    })
    
    for event in recent_events:
        video_id = event.get('video_id')
        event_type = event.get('event_type')
        
        if not video_id or not event_type:
            continue
            
        metrics = video_metrics[video_id]
        
        if event_type == 'video_view':
            metrics['views'] += 1
        elif event_type == 'share':
            metrics['shares'] += 1
        elif event_type == 'comment':
            metrics['comments'] += 1
    
    # Calculate viral coefficient and filter
    viral_videos = []
    
    for video_id, metrics in video_metrics.items():
        if metrics['views'] < min_views:
            continue
            
        # Viral coefficient = (shares + comments) / views
        viral_coefficient = (metrics['shares'] + metrics['comments']) / metrics['views']
        metrics['viral_coefficient'] = viral_coefficient
        
        if viral_coefficient > viral_threshold:
            viral_videos.append(video_id)
    
    # Sort by viral coefficient descending
    viral_videos.sort(
        key=lambda vid: video_metrics[vid]['viral_coefficient'], 
        reverse=True
    )
    
    return viral_videos
```

### Follow-up Discussion: Scaling to 500K Events/Second

**Architecture Changes**:

1. **Horizontal Sharding**: Partition by user_id hash across multiple processes
2. **Message Queue**: Use Kafka with multiple partitions for load distribution  
3. **State Management**: Use Redis Cluster for shared metrics state
4. **Batch Processing**: Process events in micro-batches (100-1000 events)

```python
# Pseudo-code for scaled architecture
class ScaledMetricsProcessor:
    def __init__(self, shard_id: int, total_shards: int):
        self.shard_id = shard_id
        self.total_shards = total_shards
        self.redis_client = redis.Redis(host='redis-cluster')
        
    def should_process_user(self, user_id: int) -> bool:
        return hash(user_id) % self.total_shards == self.shard_id
        
    def process_event_batch(self, events: List[Dict]):
        # Only process events for users assigned to this shard
        my_events = [e for e in events if self.should_process_user(e['user_id'])]
        
        # Batch update Redis for efficiency
        pipe = self.redis_client.pipeline()
        for event in my_events:
            self.update_redis_metrics(pipe, event)
        pipe.execute()
```

**Exactly-Once Processing**:
- Use Kafka's idempotent producers and transactional consumers
- Store processed event IDs in Redis with TTL
- Implement application-level deduplication based on event_id

---

## 💰 Solution Set 3: Ads Monetization Effectiveness

### Solution 3.1: Product Sense - Ad Attribution Analysis

**Problem**: Advertisers complaining about unclear ROI. Need to measure ad effectiveness.

#### Part A: Key Attribution Metrics

1. **View-Through Conversions** - Purchases within 7 days of ad view (no click)
   - *Why*: Captures brand awareness impact
   - *Target*: 15-25% of total conversions

2. **Multi-Touch Attribution** - Credit distribution across touchpoints
   - *Why*: Users interact with multiple ads before converting
   - *Models*: First-touch, last-touch, linear, time-decay

3. **Incrementality Testing** - Conversion lift from ad exposure vs control
   - *Why*: Measures true causal impact
   - *Method*: Holdout groups, synthetic controls

#### Part B: A/B Test Design - Attribution Window Optimization

**Test**: 1-day vs 7-day vs 30-day attribution windows
- **Control**: Current 7-day window
- **Treatment A**: 1-day window (conservative)
- **Treatment B**: 30-day window (generous)
- **Metric**: Advertiser satisfaction, spend retention

### Solution 3.2: Data Modeling - Ad Attribution Schema

```sql
-- Ad events fact table
fact_ad_events (
    event_id VARCHAR(50) PRIMARY KEY,
    user_id BIGINT NOT NULL,
    ad_id BIGINT NOT NULL,
    campaign_id BIGINT NOT NULL,
    event_type VARCHAR(20), -- 'impression', 'click', 'conversion'
    event_timestamp TIMESTAMP NOT NULL,
    
    -- Attribution context
    attribution_window_hours INT,
    conversion_value_usd DECIMAL(10,2),
    product_category VARCHAR(50),
    
    date_partition DATE NOT NULL
)
PARTITION BY date_partition;

-- Multi-touch attribution weights
fact_attribution_paths (
    user_id BIGINT,
    conversion_event_id VARCHAR(50),
    conversion_timestamp TIMESTAMP,
    touchpoint_sequence_json TEXT, -- [{ad_id, timestamp, channel}...]
    
    -- Attribution model weights
    first_touch_weight DECIMAL(5,4),
    last_touch_weight DECIMAL(5,4),
    linear_weight DECIMAL(5,4),
    time_decay_weight DECIMAL(5,4),
    
    total_conversion_value DECIMAL(10,2),
    PRIMARY KEY (user_id, conversion_event_id)
);
```

### Solution 3.3: SQL Analytics - ROI Calculation

```sql
-- Campaign ROI with multi-touch attribution
WITH campaign_attribution AS (
    SELECT 
        d.campaign_id,
        d.advertiser_id,
        SUM(d.total_spend_usd) as total_spend,
        
        -- Revenue attribution by model
        SUM(a.total_conversion_value * a.last_touch_weight) as last_touch_revenue,
        SUM(a.total_conversion_value * a.linear_weight) as linear_revenue,
        SUM(a.total_conversion_value * a.time_decay_weight) as time_decay_revenue
        
    FROM dim_ad_campaigns d
    LEFT JOIN fact_attribution_paths a ON d.campaign_id = a.campaign_id
    WHERE d.campaign_start_date >= CURRENT_DATE - INTERVAL '30 days'
    GROUP BY d.campaign_id, d.advertiser_id
)
SELECT 
    campaign_id,
    total_spend,
    
    -- ROI by attribution model
    ROUND(last_touch_revenue / NULLIF(total_spend, 0), 2) as last_touch_roas,
    ROUND(linear_revenue / NULLIF(total_spend, 0), 2) as linear_roas,
    ROUND(time_decay_revenue / NULLIF(total_spend, 0), 2) as time_decay_roas,
    
    -- Campaign health indicators
    CASE 
        WHEN linear_roas >= 3.0 THEN 'excellent'
        WHEN linear_roas >= 2.0 THEN 'good'
        WHEN linear_roas >= 1.0 THEN 'break_even'
        ELSE 'poor'
    END as performance_tier
FROM campaign_attribution
ORDER BY linear_roas DESC;
```

### Solution 3.4: Python Processing - Attribution Calculator

```python
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import json

class AttributionCalculator:
    """Multi-touch attribution processor for ad campaigns"""
    
    def __init__(self, attribution_window_days: int = 7):
        self.attribution_window = timedelta(days=attribution_window_days)
        self.user_touchpoints = {}  # user_id -> [touchpoint_events]
        
    def process_ad_event(self, event: Dict) -> Optional[Dict]:
        """Process ad interaction event"""
        user_id = event['user_id']
        event_type = event['event_type']
        timestamp = datetime.fromisoformat(event['timestamp'])
        
        if user_id not in self.user_touchpoints:
            self.user_touchpoints[user_id] = []
        
        # Add touchpoint
        touchpoint = {
            'ad_id': event['ad_id'],
            'campaign_id': event['campaign_id'],
            'event_type': event_type,
            'timestamp': timestamp,
            'channel': event.get('channel', 'unknown')
        }
        
        self.user_touchpoints[user_id].append(touchpoint)
        
        # If conversion event, calculate attribution
        if event_type == 'conversion':
            return self.calculate_attribution(user_id, event)
            
        return None
    
    def calculate_attribution(self, user_id: int, conversion_event: Dict) -> Dict:
        """Calculate multi-touch attribution for conversion"""
        conversion_time = datetime.fromisoformat(conversion_event['timestamp'])
        conversion_value = conversion_event.get('conversion_value', 0)
        
        # Get touchpoints within attribution window
        relevant_touchpoints = [
            tp for tp in self.user_touchpoints[user_id]
            if conversion_time - tp['timestamp'] <= self.attribution_window
            and tp['timestamp'] <= conversion_time
        ]
        
        if not relevant_touchpoints:
            return {'error': 'No touchpoints found within attribution window'}
        
        # Calculate attribution weights
        attribution_weights = self._calculate_weights(relevant_touchpoints, conversion_time)
        
        return {
            'user_id': user_id,
            'conversion_value': conversion_value,
            'touchpoint_count': len(relevant_touchpoints),
            'attribution_weights': attribution_weights,
            'first_touch_campaign': relevant_touchpoints[0]['campaign_id'],
            'last_touch_campaign': relevant_touchpoints[-1]['campaign_id']
        }
    
    def _calculate_weights(self, touchpoints: List[Dict], conversion_time: datetime) -> Dict:
        """Calculate attribution weights using different models"""
        n = len(touchpoints)
        
        weights = {
            'first_touch': [1.0] + [0.0] * (n-1),
            'last_touch': [0.0] * (n-1) + [1.0],
            'linear': [1.0/n] * n,
            'time_decay': []
        }
        
        # Time decay model (more recent touchpoints get higher weight)
        total_decay_weight = 0
        for i, tp in enumerate(touchpoints):
            days_to_conversion = (conversion_time - tp['timestamp']).days + 1
            decay_weight = 1.0 / (days_to_conversion ** 0.5)  # Square root decay
            weights['time_decay'].append(decay_weight)
            total_decay_weight += decay_weight
        
        # Normalize time decay weights
        weights['time_decay'] = [w/total_decay_weight for w in weights['time_decay']]
        
        return weights

# Usage example
if __name__ == "__main__":
    calculator = AttributionCalculator()
    
    # Sample ad journey
    events = [
        {'user_id': 1, 'ad_id': 101, 'campaign_id': 1001, 'event_type': 'impression', 'timestamp': '2024-01-01T10:00:00'},
        {'user_id': 1, 'ad_id': 102, 'campaign_id': 1002, 'event_type': 'click', 'timestamp': '2024-01-03T14:00:00'},
        {'user_id': 1, 'ad_id': 103, 'campaign_id': 1001, 'event_type': 'conversion', 'timestamp': '2024-01-05T16:00:00', 'conversion_value': 50.0}
    ]
    
    for event in events:
        result = calculator.process_ad_event(event)
        if result:
            print(f"Attribution Result: {result}")
```

---

## 🤝 Solution Set 6: Friends Follow & Recommendation (PYMK)

### Solution 6.1: Product Sense - PYMK Success with Private Accounts

**Problem**: Defining success for PYMK when suggesting private accounts.

#### Part A: Success Metrics for Private Accounts

1. **Sustained Connection Value** - % of accepted private follow requests with meaningful interaction within 30 days
   - *Rationale*: Quality over quantity for private connections
   - *Target*: 60%+ sustained engagement rate

2. **Request Acceptance Rate by Mutual Friends** - Acceptance rate segmented by # of mutual connections
   - *Insight*: Stronger mutual signals should have higher acceptance
   - *Target*: 80%+ for 3+ mutual friends

3. **Long-Term Connection Retention** - % of private connections still active after 6 months
   - *Rationale*: Private connections should be more durable
   - *Target*: 85%+ retention vs 70% for public

#### Part B: A/B Test Design

**Test**: Require 2+ mutual friends for private account suggestions vs current 1+
- **Primary Metric**: 30-day sustained engagement rate
- **Guardrails**: Overall suggestion volume, acceptance rate

### Solution 6.2: Data Modeling - Social Graph Schema

```sql
-- User relationships (friendships + follows)
fact_user_relationships (
    relationship_id BIGINT PRIMARY KEY,
    user_id_from BIGINT NOT NULL,
    user_id_to BIGINT NOT NULL,
    relationship_type VARCHAR(10), -- 'friend', 'follow'
    status VARCHAR(15), -- 'active', 'pending', 'blocked'
    created_timestamp TIMESTAMP NOT NULL,
    
    -- Relationship strength indicators
    mutual_friends_count INT DEFAULT 0,
    interaction_score DECIMAL(5,2) DEFAULT 0,
    
    INDEX idx_user_from (user_id_from),
    INDEX idx_user_to (user_id_to)
);

-- PYMK suggestions tracking
fact_pymk_suggestions (
    suggestion_id VARCHAR(50) PRIMARY KEY,
    target_user_id BIGINT NOT NULL,
    suggested_user_id BIGINT NOT NULL,
    suggestion_timestamp TIMESTAMP NOT NULL,
    
    -- Suggestion context
    suggestion_reason VARCHAR(50), -- 'mutual_friends', 'location', 'contacts'
    mutual_friends_count INT,
    algorithm_score DECIMAL(5,4),
    
    -- Outcome tracking
    was_viewed BOOLEAN DEFAULT FALSE,
    was_requested BOOLEAN DEFAULT FALSE,
    was_accepted BOOLEAN DEFAULT FALSE,
    outcome_timestamp TIMESTAMP,
    
    date_partition DATE NOT NULL
)
PARTITION BY date_partition;

-- User privacy settings
dim_user_privacy (
    user_id BIGINT PRIMARY KEY,
    is_private_account BOOLEAN DEFAULT FALSE,
    allow_friend_suggestions BOOLEAN DEFAULT TRUE,
    pymk_frequency_preference VARCHAR(10), -- 'high', 'medium', 'low', 'off'
    last_updated TIMESTAMP NOT NULL
);
```

### Solution 6.3: SQL Analytics - PYMK Effectiveness

```sql
-- PYMK success rate analysis for private accounts
WITH pymk_outcomes AS (
    SELECT 
        s.target_user_id,
        s.suggested_user_id,
        s.mutual_friends_count,
        p_target.is_private_account as target_is_private,
        p_suggested.is_private_account as suggested_is_private,
        s.was_requested,
        s.was_accepted,
        
        -- Check for sustained engagement (30 days post-acceptance)
        CASE 
            WHEN s.was_accepted AND EXISTS (
                SELECT 1 FROM fact_user_interactions i
                WHERE (i.user_id_from = s.target_user_id AND i.user_id_to = s.suggested_user_id)
                   OR (i.user_id_from = s.suggested_user_id AND i.user_id_to = s.target_user_id)
                AND i.interaction_timestamp BETWEEN s.outcome_timestamp AND s.outcome_timestamp + INTERVAL '30 days'
                AND i.interaction_type IN ('like', 'comment', 'message')
            ) THEN TRUE ELSE FALSE
        END as has_sustained_engagement
        
    FROM fact_pymk_suggestions s
    LEFT JOIN dim_user_privacy p_target ON s.target_user_id = p_target.user_id
    LEFT JOIN dim_user_privacy p_suggested ON s.suggested_user_id = p_suggested.user_id
    WHERE s.date_partition >= CURRENT_DATE - INTERVAL '30 days'
),
private_account_metrics AS (
    SELECT 
        CASE WHEN suggested_is_private THEN 'private' ELSE 'public' END as account_type,
        mutual_friends_count,
        COUNT(*) as total_suggestions,
        COUNT(CASE WHEN was_requested THEN 1 END) as requests_sent,
        COUNT(CASE WHEN was_accepted THEN 1 END) as requests_accepted,
        COUNT(CASE WHEN has_sustained_engagement THEN 1 END) as sustained_connections
    FROM pymk_outcomes
    GROUP BY suggested_is_private, mutual_friends_count
)
SELECT 
    account_type,
    mutual_friends_count,
    total_suggestions,
    
    -- Success rate metrics
    ROUND(100.0 * requests_sent / total_suggestions, 2) as request_rate_pct,
    ROUND(100.0 * requests_accepted / NULLIF(requests_sent, 0), 2) as acceptance_rate_pct,
    ROUND(100.0 * sustained_connections / NULLIF(requests_accepted, 0), 2) as sustained_engagement_pct,
    
    -- Overall conversion funnel
    ROUND(100.0 * sustained_connections / total_suggestions, 2) as suggestion_to_connection_pct
FROM private_account_metrics
ORDER BY account_type, mutual_friends_count;
```

### Solution 6.4: Python Processing - Friend Recommendation Algorithm

```python
from typing import List, Dict, Set
from collections import defaultdict

def generate_recommendations(target_user_id: int, users_data: List[Dict], max_recommendations: int) -> List[int]:
    """
    Generate friend recommendations for a target user based on mutual friends and other attributes.
    Optimized for private account considerations.
    """
    # Find target user
    target_user = None
    for user in users_data:
        if user['user_id'] == target_user_id:
            target_user = user
            break
    
    if not target_user:
        return []

    target_friend_ids = set(target_user.get('friend_ids', []))
    target_country = target_user.get('country_code')
    
    recommendations = {}

    for candidate in users_data:
        candidate_id = candidate['user_id']
        
        # Exclusion rules
        if candidate_id == target_user_id or candidate_id in target_friend_ids:
            continue

        # Calculate scoring factors
        candidate_friend_ids = set(candidate.get('friend_ids', []))
        mutual_friends_count = len(target_friend_ids.intersection(candidate_friend_ids))
        
        score = 0
        
        # Mutual friends (strongest signal)
        score += mutual_friends_count * 5
        
        # Same country bonus
        if candidate.get('country_code') == target_country:
            score += 3

        # Activity bonus (active in last 7 days)
        if candidate.get('last_active_days_ago', float('inf')) <= 7:
            score += 2
        
        # Private account penalty (only if no mutual friends)
        if candidate.get('is_private', False) and mutual_friends_count == 0:
            score -= 10
            
        # Enhanced scoring for private accounts with mutual friends
        if candidate.get('is_private', False) and mutual_friends_count >= 2:
            score += 3  # Bonus for strong mutual connection to private user
            
        # Only include positive scores or private users with mutual friends
        if score > 0 or (candidate.get('is_private', False) and mutual_friends_count > 0):
            recommendations[candidate_id] = score

    # Sort by score descending, user_id ascending for ties
    sorted_recommendations = sorted(recommendations.items(), key=lambda x: (-x[1], x[0]))
    
    return [user_id for user_id, score in sorted_recommendations[:max_recommendations]]

# Advanced network analysis for PYMK
class SocialGraphAnalyzer:
    """Analyze social graph for friend recommendations"""
    
    def __init__(self, users_data: List[Dict]):
        self.users = {user['user_id']: user for user in users_data}
        self.friendship_graph = self._build_graph()
        
    def _build_graph(self) -> Dict[int, Set[int]]:
        """Build bidirectional friendship graph"""
        graph = defaultdict(set)
        for user_id, user in self.users.items():
            friends = user.get('friend_ids', [])
            for friend_id in friends:
                graph[user_id].add(friend_id)
                graph[friend_id].add(user_id)  # Ensure bidirectional
        return graph
    
    def calculate_mutual_friends_strength(self, user1_id: int, user2_id: int) -> float:
        """Calculate mutual friends connection strength"""
        user1_friends = self.friendship_graph.get(user1_id, set())
        user2_friends = self.friendship_graph.get(user2_id, set())
        
        mutual_friends = user1_friends.intersection(user2_friends)
        
        if not mutual_friends:
            return 0.0
        
        # Weight by mutual friends' activity and connection strength
        total_strength = 0.0
        for mutual_friend_id in mutual_friends:
            mutual_friend = self.users.get(mutual_friend_id)
            if mutual_friend:
                # More active friends provide stronger signals
                activity_bonus = max(0, 10 - mutual_friend.get('last_active_days_ago', 30)) / 10
                total_strength += 1.0 + activity_bonus
                
        return total_strength / len(mutual_friends)  # Average strength
    
    def find_friend_of_friend_candidates(self, target_user_id: int, max_distance: int = 2) -> List[Dict]:
        """Find potential friends through network traversal"""
        candidates = []
        target_friends = self.friendship_graph.get(target_user_id, set())
        
        # Look at friends of friends
        for friend_id in target_friends:
            friend_friends = self.friendship_graph.get(friend_id, set())
            
            for candidate_id in friend_friends:
                if candidate_id != target_user_id and candidate_id not in target_friends:
                    strength = self.calculate_mutual_friends_strength(target_user_id, candidate_id)
                    candidate_user = self.users.get(candidate_id)
                    
                    if candidate_user:
                        candidates.append({
                            'user_id': candidate_id,
                            'connection_strength': strength,
                            'mutual_friend_ids': list(target_friends.intersection(
                                self.friendship_graph.get(candidate_id, set())
                            ))
                        })
        
        # Sort by connection strength
        candidates.sort(key=lambda x: x['connection_strength'], reverse=True)
        return candidates

# Test the enhanced algorithm
if __name__ == "__main__":
    test_users = [
        {'user_id': 1, 'country_code': 'US', 'is_private': False, 'friend_ids': [2, 3], 'last_active_days_ago': 0},
        {'user_id': 2, 'country_code': 'US', 'is_private': False, 'friend_ids': [1, 4], 'last_active_days_ago': 5},
        {'user_id': 3, 'country_code': 'CA', 'is_private': True,  'friend_ids': [1, 5], 'last_active_days_ago': 10},
        {'user_id': 4, 'country_code': 'US', 'is_private': False, 'friend_ids': [2], 'last_active_days_ago': 2},
        {'user_id': 5, 'country_code': 'CA', 'is_private': True,  'friend_ids': [3, 6, 7], 'last_active_days_ago': 3},
    ]
    
    # Test basic recommendations
    recommendations = generate_recommendations(target_user_id=1, users_data=test_users, max_recommendations=3)
    print(f"Recommendations for User 1: {recommendations}")
    
    # Test graph analysis
    analyzer = SocialGraphAnalyzer(test_users)
    candidates = analyzer.find_friend_of_friend_candidates(target_user_id=1)
    print(f"Network-based candidates: {candidates}")
```

---

## Meta Interview Success Tips

### Technical Depth Signals
- **Scale-aware thinking**: Always mention billions of records
- **Trade-off discussions**: Memory vs latency, consistency vs availability
- **Operational concerns**: Monitoring, alerting, failure scenarios
- **Performance optimization**: Indexing, partitioning, caching strategies

### Collaboration Signals  
- **Ask clarifying questions**: "Should we optimize for read or write performance?"
- **Explain assumptions**: "I'm assuming we need real-time updates within 1 second"
- **Consider stakeholders**: PM needs, engineering constraints, user experience

### Ownership Signals
- **End-to-end thinking**: Data pipeline monitoring, alerting, recovery
- **Production readiness**: Error handling, logging, performance metrics
- **Long-term maintenance**: Schema evolution, operational runbooks

Good luck with your Meta interview! 🚀 