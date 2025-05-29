#!/usr/bin/env python3
"""
Meta Data Engineer Interview - Scenario 2: Reels Analytics
Problem 4: Python Data Processing - Real-time Reels Analytics

Time Limit: 8 minutes

Scenario: Build a streaming data processor that ingests Reels engagement events 
and produces real-time analytics for the recommendation system. 
Must handle 50K events/second with low latency.

Your Task:
1. Parse incoming event streams (JSON)
2. Calculate rolling 24-hour engagement metrics per user
3. Identify trending videos (viral coefficient > 1.5)
4. Handle data quality issues (missing fields, duplicates)

Requirements:
- Process 50K events/second
- Memory efficient 
- Fault tolerant

Follow-up: How would you scale this to handle 10x traffic during peak hours?
"""

import json
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
from collections import defaultdict, deque
import threading


# Sample streaming event format
SAMPLE_EVENT = {
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


def parse_event(event_json: str) -> Optional[Dict[str, Any]]:
    """
    Parse and validate Reels engagement event
    Return None for invalid events
    
    TODO: Implement your solution here
    Requirements:
    - Parse JSON safely
    - Validate required fields: event_id, event_type, user_id, video_id, timestamp
    - Handle missing/invalid fields gracefully
    - Extract metadata safely
    """
    # YOUR CODE HERE
    pass


class UserMetricsTracker:
    """
    Track 24-hour rolling metrics per user
    
    TODO: Implement your solution here
    Requirements:
    - Total videos watched
    - Total engagement time (minutes)
    - Engagement rate (likes/views ratio)
    - Memory efficient for 10M+ users
    - Thread-safe
    """
    
    def __init__(self, window_hours: int = 24):
        # YOUR CODE HERE
        pass
        
    def update_user_metrics(self, user_id: int, event: Dict[str, Any]):
        """
        Update rolling 24-hour metrics for user
        
        TODO: Implement your solution here
        """
        # YOUR CODE HERE
        pass
        
    def get_user_metrics(self, user_id: int) -> Dict[str, Any]:
        """
        Get current 24-hour metrics for user
        
        TODO: Implement your solution here
        Should return: {
            'videos_watched': int,
            'total_engagement_time_minutes': float,
            'engagement_rate': float  # likes/views ratio
        }
        """
        # YOUR CODE HERE
        pass


def detect_viral_videos(events: List[Dict[str, Any]], 
                       window_hours: int = 2,
                       viral_threshold: float = 1.5,
                       min_views: int = 1000) -> List[int]:
    """
    Return list of video_ids that are trending
    Based on recent engagement patterns
    
    TODO: Implement your solution here
    Requirements:
    - Viral coefficient = (shares + comments) / views
    - Flag videos with coefficient > 1.5 and 1000+ views
    - Calculate metrics over last 2 hours
    - Sort by viral coefficient descending
    """
    # YOUR CODE HERE
    pass


def test_event_parser():
    """Test the event parser with sample data"""
    print("Testing Event Parser...")
    
    # Test valid event
    valid_event_json = json.dumps(SAMPLE_EVENT)
    result = parse_event(valid_event_json)
    print(f"Valid event result: {result}")
    
    # Test invalid JSON
    invalid_json = "not json"
    result = parse_event(invalid_json)
    print(f"Invalid JSON result: {result}")
    
    # Test missing fields
    incomplete_event = {"event_id": "test", "user_id": 123}
    incomplete_json = json.dumps(incomplete_event)
    result = parse_event(incomplete_json)
    print(f"Incomplete event result: {result}")


def test_user_metrics():
    """Test the user metrics tracker"""
    print("\nTesting User Metrics Tracker...")
    
    tracker = UserMetricsTracker()
    
    # Create test events
    test_events = [
        {
            "event_type": "video_view",
            "user_id": 123,
            "video_id": 456,
            "timestamp": datetime.now().isoformat(),
            "metadata": {"view_duration_ms": 30000}
        },
        {
            "event_type": "like",
            "user_id": 123,
            "video_id": 456,
            "timestamp": datetime.now().isoformat()
        }
    ]
    
    # Update metrics
    for event in test_events:
        tracker.update_user_metrics(123, event)
    
    # Get metrics
    metrics = tracker.get_user_metrics(123)
    print(f"User metrics: {metrics}")


def test_viral_detection():
    """Test the viral video detector"""
    print("\nTesting Viral Video Detection...")
    
    # Create test events for viral detection
    test_events = [
        {
            "video_id": 1001,
            "event_type": "video_view",
            "parsed_timestamp": datetime.now()
        },
        {
            "video_id": 1001,
            "event_type": "share",
            "parsed_timestamp": datetime.now()
        },
        {
            "video_id": 1001,
            "event_type": "comment", 
            "parsed_timestamp": datetime.now()
        }
    ] * 500  # Simulate 1500 events (500 each type)
    
    viral_videos = detect_viral_videos(test_events)
    print(f"Viral videos detected: {viral_videos}")


if __name__ == "__main__":
    print("Meta Reels Analytics - Python Processing Challenge")
    print("=" * 60)
    
    # Run tests to verify your implementation
    test_event_parser()
    test_user_metrics()
    test_viral_detection()
    
    print("\n" + "=" * 60)
    print("Complete your implementation and run again to test!")
    print("Focus on:")
    print("1. Error handling and data validation")
    print("2. Memory efficiency for large scale")
    print("3. Thread safety for concurrent processing")
    print("4. Performance optimization") 