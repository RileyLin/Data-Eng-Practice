#!/usr/bin/env python3
"""
Meta Data Engineer Interview - Scenario 1: DAU/MAU Analytics
Problem 4: Python Data Processing - User Engagement Pipeline

Time Limit: 8 minutes

Scenario: Build a user engagement pipeline that calculates DAU/MAU metrics
and identifies user churn patterns in real-time. Must handle billions of
user activity events and support multiple time window calculations.

Your Task:
1. Process user activity events and calculate rolling DAU/MAU
2. Identify users at risk of churning based on engagement patterns
3. Generate cohort retention reports for different user segments
4. Handle data quality issues and late-arriving events

Requirements:
- Process 100K+ users simultaneously
- Calculate multiple time windows (1, 7, 30 days)
- Memory efficient for large user base
- Real-time churn risk scoring

Follow-up: How would you scale this across multiple data centers?
"""

from datetime import datetime, timedelta
from typing import Dict, List, Set, Optional
from collections import defaultdict, deque
from dataclasses import dataclass
from enum import Enum
import threading


class EventType(Enum):
    SESSION_START = "session_start"
    POST_VIEWED = "post_viewed"
    POST_LIKED = "post_liked"
    POST_SHARED = "post_shared"
    COMMENT_POSTED = "comment_posted"
    SESSION_END = "session_end"


@dataclass
class UserEvent:
    user_id: int
    event_type: EventType
    timestamp: datetime
    session_id: str
    metadata: Dict = None


# Sample activity event
SAMPLE_EVENT = UserEvent(
    user_id=123456789,
    event_type=EventType.POST_VIEWED,
    timestamp=datetime.now(),
    session_id="sess_abc123",
    metadata={"post_id": 987654, "time_spent_seconds": 15}
)


class DAUMAUCalculator:
    """
    Calculate DAU/MAU metrics with rolling time windows
    
    TODO: Implement your solution here
    Requirements:
    - Track active users for multiple time windows (1, 7, 30 days)
    - Calculate DAU/MAU ratio efficiently
    - Handle user activity events in real-time
    - Memory efficient for billions of users
    """
    
    def __init__(self):
        # YOUR CODE HERE
        pass
        
    def add_user_activity(self, event: UserEvent):
        """
        Record user activity event
        
        TODO: Implement your solution here
        """
        # YOUR CODE HERE
        pass
        
    def get_dau_mau_ratio(self, date: datetime) -> float:
        """
        Get DAU/MAU ratio for specific date
        
        TODO: Implement your solution here
        Should return ratio between 0.0 and 1.0
        """
        # YOUR CODE HERE
        pass
        
    def get_active_users_count(self, date: datetime, days_back: int) -> int:
        """
        Get count of active users in last N days from given date
        
        TODO: Implement your solution here
        """
        # YOUR CODE HERE
        pass


class ChurnRiskAnalyzer:
    """
    Identify users at risk of churning based on engagement patterns
    
    TODO: Implement your solution here
    Requirements:
    - Track user engagement patterns over time
    - Calculate churn risk score (0-100)
    - Identify users with declining activity
    - Consider recency, frequency, and engagement depth
    """
    
    def __init__(self, window_days: int = 30):
        # YOUR CODE HERE
        pass
        
    def update_user_activity(self, event: UserEvent):
        """
        Update user activity patterns
        
        TODO: Implement your solution here
        """
        # YOUR CODE HERE
        pass
        
    def get_churn_risk_score(self, user_id: int) -> float:
        """
        Calculate churn risk score for user (0-100)
        Higher score = higher churn risk
        
        TODO: Implement your solution here
        Consider:
        - Days since last activity
        - Change in activity frequency
        - Engagement depth (likes, shares vs just views)
        - Session duration trends
        """
        # YOUR CODE HERE
        pass
        
    def get_high_risk_users(self, threshold: float = 75.0) -> List[int]:
        """
        Get list of users with churn risk above threshold
        
        TODO: Implement your solution here
        """
        # YOUR CODE HERE
        pass


def calculate_cohort_retention(events: List[UserEvent], 
                             cohort_start_date: datetime,
                             cohort_definition: str = "registration") -> Dict[int, float]:
    """
    Calculate retention rates for user cohort over time
    
    TODO: Implement your solution here
    Requirements:
    - Define cohort (users who registered/first active on specific date)
    - Calculate retention on Day 1, 7, 14, 30
    - Return retention percentages by day
    - Handle large cohort sizes efficiently
    
    Args:
        events: List of user activity events
        cohort_start_date: Date to define cohort
        cohort_definition: How to define cohort membership
        
    Returns:
        Dict mapping days since cohort start to retention rate
        Example: {1: 0.85, 7: 0.45, 14: 0.32, 30: 0.18}
    """
    # YOUR CODE HERE
    pass


def test_dau_mau_calculator():
    """Test the DAU/MAU calculator"""
    print("Testing DAU/MAU Calculator...")
    
    calculator = DAUMAUCalculator()
    
    # Create test events
    test_date = datetime(2025, 1, 15)
    test_events = [
        UserEvent(123, EventType.SESSION_START, test_date, "sess1"),
        UserEvent(124, EventType.SESSION_START, test_date, "sess2"),
        UserEvent(125, EventType.SESSION_START, test_date - timedelta(days=15), "sess3"),
        UserEvent(126, EventType.SESSION_START, test_date - timedelta(days=25), "sess4"),
    ]
    
    # Add events
    for event in test_events:
        calculator.add_user_activity(event)
    
    # Test DAU/MAU calculation
    ratio = calculator.get_dau_mau_ratio(test_date)
    print(f"DAU/MAU ratio: {ratio}")
    
    # Test active user counts
    dau = calculator.get_active_users_count(test_date, 1)
    mau = calculator.get_active_users_count(test_date, 30)
    print(f"DAU: {dau}, MAU: {mau}")


def test_churn_analyzer():
    """Test the churn risk analyzer"""
    print("\nTesting Churn Risk Analyzer...")
    
    analyzer = ChurnRiskAnalyzer()
    
    # Create test user activity pattern
    base_date = datetime.now()
    
    # User with declining activity (high churn risk)
    declining_events = [
        UserEvent(200, EventType.SESSION_START, base_date - timedelta(days=25), "sess1"),
        UserEvent(200, EventType.SESSION_START, base_date - timedelta(days=20), "sess2"),
        UserEvent(200, EventType.SESSION_START, base_date - timedelta(days=18), "sess3"),
        # No recent activity = churn risk
    ]
    
    # User with consistent activity (low churn risk)  
    active_events = [
        UserEvent(201, EventType.SESSION_START, base_date - timedelta(days=1), "sess1"),
        UserEvent(201, EventType.POST_LIKED, base_date - timedelta(days=1), "sess1"),
        UserEvent(201, EventType.SESSION_START, base_date - timedelta(days=3), "sess2"),
        UserEvent(201, EventType.POST_SHARED, base_date - timedelta(days=3), "sess2"),
    ]
    
    # Process events
    for event in declining_events + active_events:
        analyzer.update_user_activity(event)
    
    # Test churn scores
    declining_score = analyzer.get_churn_risk_score(200)
    active_score = analyzer.get_churn_risk_score(201)
    
    print(f"Declining user churn score: {declining_score}")
    print(f"Active user churn score: {active_score}")
    
    # Test high risk users
    high_risk = analyzer.get_high_risk_users(50.0)
    print(f"High risk users: {high_risk}")


def test_cohort_retention():
    """Test cohort retention calculation"""
    print("\nTesting Cohort Retention...")
    
    cohort_date = datetime(2025, 1, 1)
    
    # Create cohort events
    test_events = [
        # User 100: registered Jan 1, active on day 1, 7, but not 30
        UserEvent(100, EventType.SESSION_START, cohort_date, "sess1"),
        UserEvent(100, EventType.SESSION_START, cohort_date + timedelta(days=1), "sess2"),
        UserEvent(100, EventType.SESSION_START, cohort_date + timedelta(days=7), "sess3"),
        
        # User 101: registered Jan 1, only active on registration day
        UserEvent(101, EventType.SESSION_START, cohort_date, "sess1"),
        
        # User 102: registered Jan 1, very active throughout
        UserEvent(102, EventType.SESSION_START, cohort_date, "sess1"),
        UserEvent(102, EventType.SESSION_START, cohort_date + timedelta(days=1), "sess2"),
        UserEvent(102, EventType.SESSION_START, cohort_date + timedelta(days=7), "sess3"),
        UserEvent(102, EventType.SESSION_START, cohort_date + timedelta(days=30), "sess4"),
    ]
    
    # Calculate retention
    retention = calculate_cohort_retention(test_events, cohort_date)
    print(f"Cohort retention rates: {retention}")


if __name__ == "__main__":
    print("Meta DAU/MAU Analytics - Python Processing Challenge")
    print("=" * 60)
    
    # Run tests to verify your implementation
    test_dau_mau_calculator()
    test_churn_analyzer()
    test_cohort_retention()
    
    print("\n" + "=" * 60)
    print("Complete your implementation and run again to test!")
    print("Focus on:")
    print("1. Efficient time window calculations")
    print("2. Memory management for billions of users")
    print("3. Real-time processing capabilities")
    print("4. Accurate churn risk modeling") 