# Meta Data Engineer Interview - Final Sprint Solutions
## Reels Session Analytics Scenario

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