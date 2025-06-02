# Scenario 5: DAU/MAU Analysis - Python Questions

## Python Question 5.4.1: Session-Based Engagement Event Processing

Implement the Python function `process_event(event, buffer, totals, test_users)` that:

1.  Processes a single engagement event (like, comment, view).
2.  Buffers events by `session_id` in a `buffer` dictionary.
3.  Updates aggregate counts in `totals` for non-internal sessions when a `session_end` event is received.
4.  Does not count events from internal `test_users` in the aggregate counts.

This function is a foundational piece for tracking user engagement which can then be used to calculate metrics like DAU (Daily Active Users) or MAU (Monthly Active Users) by aggregating these processed totals over respective periods.

**DATA STRUCTURE EXAMPLES:**

Input: `event` (dict)
- Keys: 'session_id', 'user_id', 'event_type'
- Example: `{'session_id': 's1', 'user_id': 'user1', 'event_type': 'like'}`

Input: `buffer` (dict)
- Structure: `{session_id: {'events': [event1, event2, ...], 'users': {user1, user2, ...}}}` (or similar structure to hold user events per session)
- Example: `{'s1': {'events': [{'session_id': 's1', 'user_id': 'user1', 'event_type': 'like'}], 'users': {'user1'}}}`

Input: `totals` (dict)
- Structure: `{event_type: count}`
- Example: `{'likes': 5, 'comments': 3, 'views': 10}`

Input: `test_users` (set)
- Structure: `{user_id1, user_id2, ...}`
- Example: `{'user_test_A', 'user_test_B', 'internal_user_123'}`

**Example Scenario 1 - Regular user session:**
Events:
```python
[
    {'session_id': 's1', 'user_id': 'user1', 'event_type': 'like'},
    {'session_id': 's1', 'user_id': 'user1', 'event_type': 'view'},
    {'session_id': 's1', 'user_id': 'user1', 'event_type': 'session_end'}
]
```
Result: `totals` updated with +1 like, +1 view.

**Example Scenario 2 - Test user session (ignored):**
Events:
```python
[
    {'session_id': 's2', 'user_id': 'user_test_A', 'event_type': 'like'},
    {'session_id': 's2', 'user_id': 'user_test_A', 'event_type': 'session_end'}
]
```
Result: `totals` unchanged (test user session ignored).

**Example Scenario 3 - Mixed session (session contains a test user, so entire session might be ignored or handled based on specific rules, e.g., only count non-test user events):**
Events:
```python
[
    {'session_id': 's3', 'user_id': 'user2', 'event_type': 'comment'},
    {'session_id': 's3', 'user_id': 'user_test_B', 'event_type': 'like'},
    {'session_id': 's3', 'user_id': 'user2', 'event_type': 'session_end'}
]
```
Result: Behavior depends on implementation details regarding mixed sessions. The provided `q003_session_engagement.py` aims to count non-test user events even in mixed sessions.

**Buffer Evolution Example:**
- Initial: `buffer = {}`
- After event 1: `buffer = {'s1': {'users': {'user1': ['like']}}}` (actual structure may vary based on implementation)
- After event 2: `buffer = {'s1': {'users': {'user1': ['like', 'view']}}}`
- After `session_end`: `buffer = {}` (session processed and removed)

**Function Signature:**
```python
def process_event(event, buffer, totals, test_users):
    # ... implementation ...
```

## Question 1: User Engagement Processing

**Problem**: Implement a function to process user engagement events and calculate DAU/MAU metrics while filtering out test users and maintaining session integrity.

**Key Requirements**:
- Process events by session and exclude test user sessions entirely
- Track engagement events (likes, comments, views) 
- Calculate accurate user activity for DAU/MAU computation
- Handle mixed sessions (regular + test users) appropriately

### Solution:
```python
def process_event(event, buffer, totals, test_users):
    """
    Process a single engagement event, buffer it by session_id, and update 
    aggregate counts for non-internal sessions upon session_end.
    
    Args:
        event (dict): Event with 'session_id', 'user_id', 'event_type'
        buffer (dict): Session buffer storing events by session_id 
        totals (dict): Running counts of engagement types
        test_users (set): Set of internal test user IDs to exclude
        
    Returns:
        None (updates buffer and totals in-place)
    """
    session_id = event['session_id']
    user_id = event['user_id']
    event_type = event['event_type']

    # Initialize session in buffer if not already present
    if session_id not in buffer:
        buffer[session_id] = {'events': [], 'users': set()}

    buffer[session_id]['events'].append(event)
    buffer[session_id]['users'].add(user_id)
    
    if event_type == 'session_end':
        # Check if session contains any test users
        is_test_session = any(user in test_users for user in buffer[session_id]['users'])
        
        if not is_test_session:
            # Process all events in this session
            for e in buffer[session_id]['events']:
                e_event_type = e['event_type']
                if e_event_type in totals:
                    totals[e_event_type] += 1
        
        # Remove session from buffer after processing
        del buffer[session_id]
```

---

## Question 2: DAU/MAU Calculator

**Problem**: Create a class to efficiently calculate DAU/MAU ratios and engagement metrics from user activity data.

**Features**:
- Track daily and monthly active users
- Calculate stickiness ratios over time periods
- Support user segmentation analysis
- Handle different definitions of "active"

### Solution:
```python
from datetime import datetime, timedelta
from collections import defaultdict, deque
from typing import Dict, List, Set, Tuple

class DAUMAUCalculator:
    """
    Efficient calculator for DAU/MAU metrics and user engagement analysis.
    """
    
    def __init__(self, activity_threshold: int = 1):
        """
        Initialize the calculator.
        
        Args:
            activity_threshold: Minimum actions required to be considered "active"
        """
        self.activity_threshold = activity_threshold
        self.daily_active_users = defaultdict(set)  # date -> set of active users
        self.user_activity = defaultdict(lambda: defaultdict(int))  # user -> date -> action_count
        self.monthly_windows = defaultdict(deque)  # date -> deque of 30 days of active users
        
    def add_user_activity(self, user_id: str, date: str, action_count: int):
        """
        Add user activity for a specific date.
        
        Args:
            user_id: User identifier
            date: Date string (YYYY-MM-DD)
            action_count: Number of actions performed
        """
        self.user_activity[user_id][date] = action_count
        
        # Check if user meets activity threshold
        if action_count >= self.activity_threshold:
            self.daily_active_users[date].add(user_id)
    
    def calculate_dau(self, date: str) -> int:
        """Calculate Daily Active Users for a specific date."""
        return len(self.daily_active_users[date])
    
    def calculate_mau(self, date: str) -> int:
        """Calculate Monthly Active Users for a specific date (30-day window)."""
        target_date = datetime.strptime(date, '%Y-%m-%d')
        monthly_users = set()
        
        for i in range(30):
            check_date = target_date - timedelta(days=i)
            check_date_str = check_date.strftime('%Y-%m-%d')
            monthly_users.update(self.daily_active_users[check_date_str])
        
        return len(monthly_users)
    
    def calculate_dau_mau_ratio(self, date: str) -> float:
        """Calculate DAU/MAU ratio for a specific date."""
        dau = self.calculate_dau(date)
        mau = self.calculate_mau(date)
        
        return dau / mau if mau > 0 else 0.0
    
    def get_engagement_distribution(self, date: str) -> Dict[str, int]:
        """
        Get distribution of user engagement levels for a given month.
        
        Returns:
            Dict with engagement tiers and user counts
        """
        target_date = datetime.strptime(date, '%Y-%m-%d')
        user_active_days = defaultdict(int)
        
        # Count active days for each user in 30-day window
        for i in range(30):
            check_date = target_date - timedelta(days=i)
            check_date_str = check_date.strftime('%Y-%m-%d')
            
            for user in self.daily_active_users[check_date_str]:
                user_active_days[user] += 1
        
        # Categorize users by engagement tier
        distribution = {'casual': 0, 'regular': 0, 'core': 0, 'power': 0}
        
        for user, active_days in user_active_days.items():
            if active_days >= 20:
                distribution['power'] += 1
            elif active_days >= 16:
                distribution['core'] += 1
            elif active_days >= 6:
                distribution['regular'] += 1
            else:
                distribution['casual'] += 1
        
        return distribution
    
    def analyze_cohort_stickiness(self, cohort_users: Set[str], 
                                 start_date: str, days: int = 30) -> List[float]:
        """
        Analyze DAU/MAU progression for a specific user cohort.
        
        Args:
            cohort_users: Set of users in the cohort
            start_date: Starting date for analysis
            days: Number of days to analyze
            
        Returns:
            List of DAU/MAU ratios for each day
        """
        start_dt = datetime.strptime(start_date, '%Y-%m-%d')
        ratios = []
        
        for day in range(days):
            current_date = start_dt + timedelta(days=day)
            current_date_str = current_date.strftime('%Y-%m-%d')
            
            # Calculate DAU for cohort
            cohort_dau = len(cohort_users.intersection(
                self.daily_active_users[current_date_str]
            ))
            
            # Calculate MAU for cohort (30-day window)
            cohort_mau_users = set()
            for i in range(min(30, day + 1)):
                check_date = current_date - timedelta(days=i)
                check_date_str = check_date.strftime('%Y-%m-%d')
                cohort_mau_users.update(
                    cohort_users.intersection(self.daily_active_users[check_date_str])
                )
            
            cohort_mau = len(cohort_mau_users)
            ratio = cohort_dau / cohort_mau if cohort_mau > 0 else 0.0
            ratios.append(ratio)
        
        return ratios

# Example usage and test cases
def test_dau_mau_calculator():
    """Test the DAU/MAU calculator with sample data."""
    calculator = DAUMAUCalculator(activity_threshold=1)
    
    # Add sample user activity
    test_data = [
        ('user1', '2023-01-01', 5),
        ('user1', '2023-01-02', 3),
        ('user1', '2023-01-03', 7),
        ('user2', '2023-01-01', 2),
        ('user2', '2023-01-03', 1),
        ('user3', '2023-01-01', 1),
        ('user3', '2023-01-02', 4),
        ('user3', '2023-01-03', 2),
    ]
    
    for user_id, date, action_count in test_data:
        calculator.add_user_activity(user_id, date, action_count)
    
    # Test DAU calculation
    dau_jan_1 = calculator.calculate_dau('2023-01-01')
    print(f"DAU for 2023-01-01: {dau_jan_1}")  # Should be 3
    
    # Test MAU calculation
    mau_jan_3 = calculator.calculate_mau('2023-01-03')
    print(f"MAU for 2023-01-03: {mau_jan_3}")  # Should be 3
    
    # Test DAU/MAU ratio
    ratio = calculator.calculate_dau_mau_ratio('2023-01-03')
    print(f"DAU/MAU ratio for 2023-01-03: {ratio:.3f}")
    
    # Test engagement distribution
    distribution = calculator.get_engagement_distribution('2023-01-03')
    print(f"Engagement distribution: {distribution}")

if __name__ == "__main__":
    test_dau_mau_calculator()
```

---

## Question 3: User Segmentation & Churn Prediction

**Problem**: Implement a system to segment users based on engagement patterns and predict churn risk using activity trends.

**Requirements**:
- Classify users into engagement tiers
- Identify users at risk of churning  
- Calculate engagement trend indicators
- Support real-time updates

### Solution:
```python
import numpy as np
from typing import Dict, List, Optional
from enum import Enum
from dataclasses import dataclass

class EngagementTier(Enum):
    CASUAL = "casual"
    REGULAR = "regular" 
    CORE = "core"
    POWER = "power"
    AT_RISK = "at_risk"

@dataclass
class UserEngagementProfile:
    user_id: str
    current_tier: EngagementTier
    active_days_last_30: int
    avg_daily_sessions: float
    avg_session_duration: float
    days_since_last_active: int
    trend_direction: str  # "increasing", "stable", "declining"
    churn_risk_score: float

class UserEngagementAnalyzer:
    """
    Analyze user engagement patterns and predict churn risk.
    """
    
    def __init__(self):
        self.user_profiles = {}
        self.tier_thresholds = {
            'power': 20,    # 20+ active days
            'core': 16,     # 16-19 active days
            'regular': 6,   # 6-15 active days
            'casual': 1     # 1-5 active days
        }
    
    def update_user_profile(self, user_id: str, activity_data: Dict) -> UserEngagementProfile:
        """
        Update user engagement profile based on recent activity.
        
        Args:
            user_id: User identifier
            activity_data: Dict with activity metrics
            
        Returns:
            Updated UserEngagementProfile
        """
        active_days = activity_data.get('active_days_last_30', 0)
        avg_sessions = activity_data.get('avg_daily_sessions', 0)
        avg_duration = activity_data.get('avg_session_duration', 0)
        days_since_active = activity_data.get('days_since_last_active', 0)
        
        # Determine engagement tier
        tier = self._classify_engagement_tier(active_days, days_since_active)
        
        # Calculate trend direction
        trend = self._calculate_trend(user_id, activity_data)
        
        # Calculate churn risk score
        churn_risk = self._calculate_churn_risk(
            active_days, avg_sessions, days_since_active, trend
        )
        
        profile = UserEngagementProfile(
            user_id=user_id,
            current_tier=tier,
            active_days_last_30=active_days,
            avg_daily_sessions=avg_sessions,
            avg_session_duration=avg_duration,
            days_since_last_active=days_since_active,
            trend_direction=trend,
            churn_risk_score=churn_risk
        )
        
        self.user_profiles[user_id] = profile
        return profile
    
    def _classify_engagement_tier(self, active_days: int, 
                                 days_since_active: int) -> EngagementTier:
        """Classify user into engagement tier."""
        if days_since_active > 7:
            return EngagementTier.AT_RISK
        elif active_days >= self.tier_thresholds['power']:
            return EngagementTier.POWER
        elif active_days >= self.tier_thresholds['core']:
            return EngagementTier.CORE
        elif active_days >= self.tier_thresholds['regular']:
            return EngagementTier.REGULAR
        else:
            return EngagementTier.CASUAL
    
    def _calculate_trend(self, user_id: str, activity_data: Dict) -> str:
        """Calculate engagement trend direction."""
        current_week = activity_data.get('active_days_current_week', 0)
        previous_week = activity_data.get('active_days_previous_week', 0)
        
        if current_week > previous_week * 1.2:
            return "increasing"
        elif current_week < previous_week * 0.8:
            return "declining"
        else:
            return "stable"
    
    def _calculate_churn_risk(self, active_days: int, avg_sessions: float,
                            days_since_active: int, trend: str) -> float:
        """Calculate churn risk score (0-1, higher = more risk)."""
        risk_score = 0.0
        
        # Activity recency factor
        if days_since_active > 7:
            risk_score += 0.4
        elif days_since_active > 3:
            risk_score += 0.2
        
        # Activity frequency factor
        if active_days < 3:
            risk_score += 0.3
        elif active_days < 6:
            risk_score += 0.1
        
        # Session engagement factor
        if avg_sessions < 0.5:
            risk_score += 0.2
        elif avg_sessions < 1.0:
            risk_score += 0.1
        
        # Trend factor
        if trend == "declining":
            risk_score += 0.2
        elif trend == "increasing":
            risk_score -= 0.1
        
        return min(1.0, max(0.0, risk_score))
    
    def get_at_risk_users(self, threshold: float = 0.6) -> List[UserEngagementProfile]:
        """Get users with high churn risk."""
        return [
            profile for profile in self.user_profiles.values()
            if profile.churn_risk_score >= threshold
        ]
    
    def get_tier_distribution(self) -> Dict[str, int]:
        """Get count of users in each engagement tier."""
        distribution = defaultdict(int)
        for profile in self.user_profiles.values():
            distribution[profile.current_tier.value] += 1
        return dict(distribution)
    
    def analyze_cohort_progression(self, cohort_users: List[str]) -> Dict:
        """Analyze how a cohort progresses through engagement tiers."""
        cohort_profiles = [
            self.user_profiles[user] for user in cohort_users
            if user in self.user_profiles
        ]
        
        tier_counts = defaultdict(int)
        total_risk_score = 0
        
        for profile in cohort_profiles:
            tier_counts[profile.current_tier.value] += 1
            total_risk_score += profile.churn_risk_score
        
        return {
            'tier_distribution': dict(tier_counts),
            'avg_churn_risk': total_risk_score / len(cohort_profiles) if cohort_profiles else 0,
            'total_users': len(cohort_profiles)
        }

# Test the analyzer
def test_engagement_analyzer():
    analyzer = UserEngagementAnalyzer()
    
    # Test data for different user types
    test_users = [
        ('power_user', {
            'active_days_last_30': 25,
            'avg_daily_sessions': 3.5,
            'avg_session_duration': 15.0,
            'days_since_last_active': 0,
            'active_days_current_week': 7,
            'active_days_previous_week': 6
        }),
        ('at_risk_user', {
            'active_days_last_30': 2,
            'avg_daily_sessions': 0.2,
            'avg_session_duration': 2.0,
            'days_since_last_active': 10,
            'active_days_current_week': 0,
            'active_days_previous_week': 1
        }),
        ('regular_user', {
            'active_days_last_30': 12,
            'avg_daily_sessions': 1.8,
            'avg_session_duration': 8.0,
            'days_since_last_active': 1,
            'active_days_current_week': 3,
            'active_days_previous_week': 3
        })
    ]
    
    for user_id, activity_data in test_users:
        profile = analyzer.update_user_profile(user_id, activity_data)
        print(f"{user_id}: {profile.current_tier.value}, Risk: {profile.churn_risk_score:.2f}")
    
    # Test analytics functions
    at_risk = analyzer.get_at_risk_users()
    print(f"At-risk users: {len(at_risk)}")
    
    distribution = analyzer.get_tier_distribution()
    print(f"Tier distribution: {distribution}")

if __name__ == "__main__":
    test_engagement_analyzer()
```

## Key Concepts Tested

1. **Data Stream Processing**: Real-time event processing and session management
2. **Time Series Analysis**: DAU/MAU calculations over rolling windows
3. **User Segmentation**: Dynamic classification based on behavior patterns
4. **Predictive Analytics**: Churn risk scoring using multiple factors
5. **Performance Optimization**: Efficient data structures for large-scale analytics
6. **Statistical Analysis**: Trend detection and engagement distribution analysis 