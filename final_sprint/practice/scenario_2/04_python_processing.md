# Problem 4: Python Data Processing - Real-time Reels Analytics
**Time Limit: 8 minutes**

## Scenario
Build a streaming data processor that ingests Reels engagement events and produces real-time analytics for the recommendation system. The system must handle 50K events/second with low latency.

## Input Data Format
```python
# Sample streaming events (JSON)
{
    "event_id": "evt_123456789",
    "event_type": "video_view", 
    "user_id": 987654321,
    "video_id": 567890123,
    "creator_id": 123456789,
    "timestamp": "2025-01-15T14:30:45.123Z",
    "session_id": "sess_abcdef123",
    "metadata": {
        "view_duration_ms": 15000,
        "video_position": 0.75,
        "device_type": "mobile"
    }
}
```

## Your Task

### Part A: Event Parser (2 minutes)
**Create a function to:**
1. Parse and validate incoming JSON events
2. Handle missing/invalid fields gracefully
3. Extract key metrics for processing

```python
def parse_event(event_json: str) -> dict:
    """
    Parse and validate Reels engagement event
    Return None for invalid events
    """
    # Your implementation here
    pass
```

### Part B: Rolling Metrics Calculator (3 minutes)
**Build a class to track 24-hour rolling metrics per user:**
- Total videos watched
- Total engagement time (minutes)
- Engagement rate (likes/views ratio)

```python
class UserMetricsTracker:
    def __init__(self):
        # Your initialization here
        pass
        
    def update_user_metrics(self, user_id: int, event: dict):
        """Update rolling 24-hour metrics for user"""
        # Your implementation here
        pass
        
    def get_user_metrics(self, user_id: int) -> dict:
        """Get current 24-hour metrics for user"""
        # Your implementation here
        pass
```

### Part C: Viral Video Detector (3 minutes)
**Write a function to identify trending videos:**
- Viral coefficient = (shares + comments) / views
- Flag videos with coefficient > 1.5 and 1000+ views
- Calculate metrics over last 2 hours

```python
def detect_viral_videos(events: list) -> list:
    """
    Return list of video_ids that are trending
    Based on recent engagement patterns
    """
    # Your implementation here
    pass
```

## Follow-up Questions
Be prepared to discuss:
- How would you scale this to handle 500K events/second?
- What would you do if the system falls behind during traffic spikes?
- How would you ensure exactly-once processing?
- What monitoring would you add for production deployment?

## Technical Requirements
- **Memory Efficient**: Handle 10M+ active users with limited RAM
- **Fault Tolerant**: Gracefully handle malformed data and system errors
- **Low Latency**: Process events within 100ms for real-time recommendations
- **Scalable**: Design for horizontal scaling across multiple machines

## Success Criteria
- **Clean, efficient code** with proper error handling
- **Memory-conscious design** for streaming workloads
- **Practical implementation** considering real-world constraints
- **Scalability considerations** for Meta-scale traffic

## Bonus Challenge
If you finish early: How would you implement exactly-once processing semantics to ensure no duplicate event processing? 