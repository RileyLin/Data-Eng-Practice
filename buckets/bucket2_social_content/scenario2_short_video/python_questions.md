# Scenario 2: Short Video (TikTok/Reels) - Python Questions

## Question 1: Video Feed View Validation

**Problem**: Process video feed logs to determine valid video views per session. A video is considered a valid view if it was visible for at least 3 seconds OR reached at least 70% completion.

**Key Requirements**:
- Track start time, end time, and maximum completion percentage for each video
- Handle multiple start/end events for the same video
- Calculate valid views based on duration and completion criteria
- Support session-based analysis

### Solution:
```python
def process_video_log(log, session_buffer):
    """
    Process a single video feed log event, updating session_buffer with view information.
    
    Args:
        log (dict): A video log event with keys:
                    'session_id', 'video_id', 'timestamp', 'event_type', 'completion_pct'
        session_buffer (dict): Data structure tracking view metrics by session/video
        
    Returns:
        None (updates session_buffer in-place)
    """
    if not log:
        return
    
    session_id = log.get('session_id')
    video_id = log.get('video_id')
    timestamp = log.get('timestamp')
    event_type = log.get('event_type')
    completion_pct = log.get('completion_pct', 0)
    
    # Initialize session if needed
    if session_id not in session_buffer:
        session_buffer[session_id] = {}
    
    current_session = session_buffer[session_id]
    
    # Initialize video if needed
    if video_id not in current_session:
        current_session[video_id] = {
            'video_id': video_id,
            'start_time': None,
            'end_time': None,
            'max_completion_pct': 0
        }
    
    current_video = current_session[video_id]
    
    # Update based on event type
    if event_type == 'start':
        if current_video['start_time'] is None:
            current_video['start_time'] = timestamp
        else:
            current_video['start_time'] = min(timestamp, current_video['start_time'])
    
    elif event_type == 'end':
        if current_video['end_time'] is None:
            current_video['end_time'] = timestamp
        else:
            current_video['end_time'] = max(timestamp, current_video['end_time'])
    
    # Always update max completion percentage
    current_video['max_completion_pct'] = max(
        current_video['max_completion_pct'], 
        completion_pct
    )

def calculate_session_valid_views(session_id: str, session_buffer: dict) -> int:
    """
    Calculate the number of valid video views for a given session.
    
    Valid view criteria:
    - Video was visible for at least 3 seconds, OR
    - Video reached at least 70% completion
    
    Args:
        session_id: The ID of the session to analyze
        session_buffer: The dictionary containing all processed session data
        
    Returns:
        The number of videos that meet the valid view criteria
    """
    if session_id not in session_buffer:
        return 0
    
    valid_count = 0
    session = session_buffer[session_id]
    
    for video_data in session.values():
        start_time = video_data['start_time']
        end_time = video_data['end_time']
        max_completion = video_data['max_completion_pct']
        
        # Check if we have valid start and end times
        if start_time is not None and end_time is not None and end_time >= start_time:
            duration = end_time - start_time
            
            # Valid if duration >= 3 seconds OR completion >= 70%
            if duration >= 3 or max_completion >= 70:
                valid_count += 1
    
    return valid_count

# Test the functions
def test_video_view_validation():
    session_buffer = {}
    
    # Test case 1: Valid view (long duration)
    process_video_log({
        'session_id': 's1', 'video_id': 'v1',
        'timestamp': 100, 'event_type': 'start', 'completion_pct': 10
    }, session_buffer)
    
    process_video_log({
        'session_id': 's1', 'video_id': 'v1',
        'timestamp': 104, 'event_type': 'end', 'completion_pct': 45
    }, session_buffer)
    
    # Test case 2: Valid view (high completion, short duration)
    process_video_log({
        'session_id': 's1', 'video_id': 'v2',
        'timestamp': 110, 'event_type': 'start', 'completion_pct': 0
    }, session_buffer)
    
    process_video_log({
        'session_id': 's1', 'video_id': 'v2',
        'timestamp': 111, 'event_type': 'end', 'completion_pct': 85
    }, session_buffer)
    
    # Test case 3: Invalid view (short duration, low completion)
    process_video_log({
        'session_id': 's1', 'video_id': 'v3',
        'timestamp': 120, 'event_type': 'start', 'completion_pct': 0
    }, session_buffer)
    
    process_video_log({
        'session_id': 's1', 'video_id': 'v3',
        'timestamp': 121, 'event_type': 'end', 'completion_pct': 30
    }, session_buffer)
    
    valid_views = calculate_session_valid_views('s1', session_buffer)
    assert valid_views == 2, f"Expected 2 valid views, got {valid_views}"
    print("Video view validation test passed!")

if __name__ == "__main__":
    test_video_view_validation()
```

---

## Question 2: Content Recommendation Engine

**Problem**: Implement a content recommendation system that suggests videos based on user preferences, trending content, and social signals.

**Features**:
- Score videos based on multiple factors
- Handle user preference learning
- Support trending and social boost factors
- Implement diversity requirements

### Solution:
```python
import random
from typing import Dict, List, Tuple, Set
from collections import defaultdict
import heapq

class ContentRecommendationEngine:
    """
    A recommendation engine for short video content based on multiple factors.
    """
    
    def __init__(self):
        self.user_preferences = defaultdict(lambda: defaultdict(float))  # user -> category -> score
        self.video_metadata = {}  # video_id -> metadata
        self.user_interactions = defaultdict(list)  # user_id -> [interaction_history]
        self.trending_boost = defaultdict(float)  # video_id -> trending_score
        self.social_connections = defaultdict(set)  # user_id -> set of connected users
        
    def add_user_interaction(self, user_id: str, video_id: str, 
                           interaction_type: str, completion_pct: float):
        """
        Record a user interaction and update preferences.
        
        Args:
            user_id: User identifier
            video_id: Video identifier
            interaction_type: 'view', 'like', 'share', 'comment'
            completion_pct: Percentage of video watched (0-100)
        """
        interaction = {
            'video_id': video_id,
            'type': interaction_type,
            'completion_pct': completion_pct,
            'timestamp': len(self.user_interactions[user_id])  # Simple timestamp
        }
        
        self.user_interactions[user_id].append(interaction)
        
        # Update user preferences based on interaction
        if video_id in self.video_metadata:
            video_category = self.video_metadata[video_id]['category']
            
            # Calculate preference score based on interaction type and completion
            preference_delta = self._calculate_preference_delta(
                interaction_type, completion_pct
            )
            
            self.user_preferences[user_id][video_category] += preference_delta
    
    def add_video_metadata(self, video_id: str, category: str, tags: List[str], 
                          creator_id: str, upload_time: int):
        """Add video metadata for recommendation scoring."""
        self.video_metadata[video_id] = {
            'category': category,
            'tags': tags,
            'creator_id': creator_id,
            'upload_time': upload_time
        }
    
    def update_trending_scores(self, trending_videos: Dict[str, float]):
        """Update trending boost scores for videos."""
        self.trending_boost.update(trending_videos)
    
    def add_social_connection(self, user_id: str, connected_user_id: str):
        """Add a social connection between users."""
        self.social_connections[user_id].add(connected_user_id)
        self.social_connections[connected_user_id].add(user_id)
    
    def _calculate_preference_delta(self, interaction_type: str, completion_pct: float) -> float:
        """Calculate how much to adjust user preference based on interaction."""
        base_scores = {
            'view': 1.0,
            'like': 3.0,
            'comment': 5.0,
            'share': 8.0
        }
        
        base_score = base_scores.get(interaction_type, 0.0)
        completion_bonus = (completion_pct / 100.0) * 2.0  # Up to 2x bonus for completion
        
        return base_score * (1.0 + completion_bonus)
    
    def _calculate_video_score(self, user_id: str, video_id: str) -> float:
        """Calculate overall recommendation score for a video."""
        if video_id not in self.video_metadata:
            return 0.0
        
        video = self.video_metadata[video_id]
        score = 0.0
        
        # 1. User preference score
        category = video['category']
        preference_score = self.user_preferences[user_id].get(category, 0.0)
        score += preference_score * 0.4  # 40% weight
        
        # 2. Trending boost
        trending_score = self.trending_boost.get(video_id, 0.0)
        score += trending_score * 0.3  # 30% weight
        
        # 3. Social signal (friends' interactions)
        social_score = self._calculate_social_score(user_id, video_id)
        score += social_score * 0.2  # 20% weight
        
        # 4. Freshness score (newer content gets slight boost)
        current_time = max([v['upload_time'] for v in self.video_metadata.values()]) if self.video_metadata else 0
        freshness_score = max(0, 10 - (current_time - video['upload_time']))
        score += freshness_score * 0.1  # 10% weight
        
        return score
    
    def _calculate_social_score(self, user_id: str, video_id: str) -> float:
        """Calculate social boost score based on friends' interactions."""
        connected_users = self.social_connections.get(user_id, set())
        social_score = 0.0
        
        for connected_user in connected_users:
            for interaction in self.user_interactions[connected_user]:
                if interaction['video_id'] == video_id:
                    # Friends' interactions boost the score
                    if interaction['type'] == 'like':
                        social_score += 2.0
                    elif interaction['type'] == 'share':
                        social_score += 5.0
                    elif interaction['type'] == 'comment':
                        social_score += 3.0
        
        return min(social_score, 20.0)  # Cap social score at 20
    
    def get_recommendations(self, user_id: str, num_recommendations: int = 10,
                          exclude_seen: bool = True, diversity_factor: float = 0.3) -> List[str]:
        """
        Get video recommendations for a user.
        
        Args:
            user_id: User to recommend for
            num_recommendations: Number of videos to recommend
            exclude_seen: Whether to exclude videos user has already seen
            diversity_factor: How much to prioritize category diversity (0-1)
            
        Returns:
            List of video IDs ordered by recommendation score
        """
        # Get videos user has already seen
        seen_videos = set()
        if exclude_seen:
            seen_videos = {
                interaction['video_id'] 
                for interaction in self.user_interactions[user_id]
            }
        
        # Calculate scores for all eligible videos
        candidate_videos = []
        for video_id in self.video_metadata:
            if video_id not in seen_videos:
                score = self._calculate_video_score(user_id, video_id)
                candidate_videos.append((score, video_id))
        
        # Sort by score (descending)
        candidate_videos.sort(reverse=True)
        
        # Apply diversity if requested
        if diversity_factor > 0:
            return self._apply_diversity(
                candidate_videos, num_recommendations, diversity_factor
            )
        else:
            return [video_id for _, video_id in candidate_videos[:num_recommendations]]
    
    def _apply_diversity(self, scored_videos: List[Tuple[float, str]], 
                        num_recommendations: int, diversity_factor: float) -> List[str]:
        """Apply diversity constraints to recommendations."""
        recommendations = []
        category_counts = defaultdict(int)
        
        # Calculate max videos per category for diversity
        total_categories = len(set(
            self.video_metadata[vid]['category'] 
            for _, vid in scored_videos
        ))
        max_per_category = max(1, int(num_recommendations * diversity_factor / total_categories))
        
        for score, video_id in scored_videos:
            if len(recommendations) >= num_recommendations:
                break
                
            video_category = self.video_metadata[video_id]['category']
            
            # Add if we haven't exceeded category limit or if diversity factor is low
            if (category_counts[video_category] < max_per_category or 
                random.random() > diversity_factor):
                recommendations.append(video_id)
                category_counts[video_category] += 1
        
        return recommendations
    
    def get_user_insights(self, user_id: str) -> Dict:
        """Get insights about user preferences and behavior."""
        interactions = self.user_interactions[user_id]
        preferences = dict(self.user_preferences[user_id])
        
        # Calculate engagement metrics
        total_interactions = len(interactions)
        avg_completion = sum(i['completion_pct'] for i in interactions) / max(total_interactions, 1)
        
        interaction_types = defaultdict(int)
        for interaction in interactions:
            interaction_types[interaction['type']] += 1
        
        return {
            'total_interactions': total_interactions,
            'avg_completion_pct': avg_completion,
            'interaction_breakdown': dict(interaction_types),
            'top_categories': sorted(preferences.items(), key=lambda x: x[1], reverse=True)[:5],
            'social_connections': len(self.social_connections[user_id])
        }

# Test the recommendation engine
def test_recommendation_engine():
    engine = ContentRecommendationEngine()
    
    # Add some video metadata
    videos = [
        ('v1', 'comedy', ['funny', 'viral'], 'creator1', 100),
        ('v2', 'dance', ['trending', 'music'], 'creator2', 101),
        ('v3', 'comedy', ['funny', 'cats'], 'creator3', 102),
        ('v4', 'education', ['science', 'facts'], 'creator4', 103),
        ('v5', 'dance', ['tutorial', 'beginner'], 'creator5', 104),
    ]
    
    for video_id, category, tags, creator, upload_time in videos:
        engine.add_video_metadata(video_id, category, tags, creator, upload_time)
    
    # Add user interactions
    engine.add_user_interaction('user1', 'v1', 'like', 85.0)
    engine.add_user_interaction('user1', 'v3', 'share', 90.0)
    engine.add_user_interaction('user1', 'v2', 'view', 20.0)
    
    # Add trending scores
    engine.update_trending_scores({'v2': 15.0, 'v4': 8.0})
    
    # Add social connections
    engine.add_social_connection('user1', 'user2')
    engine.add_user_interaction('user2', 'v4', 'like', 95.0)
    
    # Get recommendations
    recommendations = engine.get_recommendations('user1', num_recommendations=3)
    print(f"Recommendations for user1: {recommendations}")
    
    # Get user insights
    insights = engine.get_user_insights('user1')
    print(f"User insights: {insights}")
    
    print("Recommendation engine test completed!")

if __name__ == "__main__":
    test_recommendation_engine()
```

---

## Question 3: Viral Content Detection

**Problem**: Implement a system to detect viral content in real-time by analyzing engagement patterns and velocity.

**Requirements**:
- Track engagement velocity (rate of engagement growth)
- Identify viral patterns vs normal content lifecycle
- Support multiple engagement types with different weights
- Calculate viral coefficient and spread metrics

### Solution:
```python
import time
from typing import Dict, List, Tuple
from collections import deque, defaultdict
import statistics

class ViralContentDetector:
    """
    Detect viral content based on engagement velocity and patterns.
    """
    
    def __init__(self, time_window_minutes: int = 60):
        self.time_window = time_window_minutes * 60  # Convert to seconds
        self.content_engagements = defaultdict(deque)  # content_id -> [(timestamp, engagement_type, weight)]
        self.engagement_weights = {
            'view': 1,
            'like': 3,
            'comment': 5,
            'share': 10,
            'save': 7
        }
        self.viral_thresholds = {
            'velocity_threshold': 100,  # Engagements per hour
            'acceleration_threshold': 2.0,  # 2x acceleration required
            'sustained_duration': 1800  # 30 minutes of sustained growth
        }
        
    def add_engagement(self, content_id: str, engagement_type: str, 
                      timestamp: float = None):
        """
        Add an engagement event for content.
        
        Args:
            content_id: Unique content identifier
            engagement_type: Type of engagement ('view', 'like', etc.)
            timestamp: Unix timestamp (defaults to current time)
        """
        if timestamp is None:
            timestamp = time.time()
            
        weight = self.engagement_weights.get(engagement_type, 1)
        
        # Add engagement with timestamp
        self.content_engagements[content_id].append((timestamp, engagement_type, weight))
        
        # Clean old data outside time window
        self._clean_old_data(content_id, timestamp)
    
    def _clean_old_data(self, content_id: str, current_timestamp: float):
        """Remove engagement data outside the time window."""
        engagements = self.content_engagements[content_id]
        cutoff_time = current_timestamp - self.time_window
        
        while engagements and engagements[0][0] < cutoff_time:
            engagements.popleft()
    
    def calculate_engagement_velocity(self, content_id: str, 
                                    window_minutes: int = 10) -> float:
        """
        Calculate engagement velocity (weighted engagements per hour).
        
        Args:
            content_id: Content to analyze
            window_minutes: Time window for velocity calculation
            
        Returns:
            Weighted engagements per hour
        """
        if content_id not in self.content_engagements:
            return 0.0
        
        current_time = time.time()
        window_seconds = window_minutes * 60
        cutoff_time = current_time - window_seconds
        
        # Count weighted engagements in window
        weighted_count = 0
        for timestamp, _, weight in self.content_engagements[content_id]:
            if timestamp >= cutoff_time:
                weighted_count += weight
        
        # Convert to per-hour rate
        hours = window_seconds / 3600
        return weighted_count / hours if hours > 0 else 0.0
    
    def calculate_engagement_acceleration(self, content_id: str) -> float:
        """
        Calculate engagement acceleration (velocity change over time).
        
        Returns:
            Ratio of recent velocity to earlier velocity
        """
        # Compare last 10 minutes to previous 10 minutes
        recent_velocity = self.calculate_engagement_velocity(content_id, 10)
        
        # Calculate velocity for 10-20 minutes ago
        current_time = time.time()
        start_time = current_time - 20 * 60  # 20 minutes ago
        end_time = current_time - 10 * 60    # 10 minutes ago
        
        weighted_count = 0
        for timestamp, _, weight in self.content_engagements[content_id]:
            if start_time <= timestamp < end_time:
                weighted_count += weight
        
        previous_velocity = weighted_count * 6  # Convert to per-hour
        
        if previous_velocity == 0:
            return float('inf') if recent_velocity > 0 else 0.0
        
        return recent_velocity / previous_velocity
    
    def detect_viral_content(self, min_age_minutes: int = 30) -> List[Dict]:
        """
        Detect content that shows viral characteristics.
        
        Args:
            min_age_minutes: Minimum content age to consider for viral detection
            
        Returns:
            List of content with viral metrics
        """
        viral_content = []
        current_time = time.time()
        min_age_seconds = min_age_minutes * 60
        
        for content_id, engagements in self.content_engagements.items():
            if not engagements:
                continue
            
            # Check if content is old enough
            first_engagement_time = engagements[0][0]
            content_age = current_time - first_engagement_time
            
            if content_age < min_age_seconds:
                continue
            
            # Calculate viral metrics
            velocity = self.calculate_engagement_velocity(content_id, 60)
            acceleration = self.calculate_engagement_acceleration(content_id)
            
            # Check viral criteria
            is_viral = (
                velocity >= self.viral_thresholds['velocity_threshold'] and
                acceleration >= self.viral_thresholds['acceleration_threshold']
            )
            
            if is_viral:
                viral_content.append({
                    'content_id': content_id,
                    'velocity': velocity,
                    'acceleration': acceleration,
                    'total_engagements': len(engagements),
                    'content_age_minutes': content_age / 60,
                    'viral_score': velocity * acceleration
                })
        
        # Sort by viral score
        viral_content.sort(key=lambda x: x['viral_score'], reverse=True)
        return viral_content
    
    def get_engagement_distribution(self, content_id: str) -> Dict[str, int]:
        """Get breakdown of engagement types for content."""
        if content_id not in self.content_engagements:
            return {}
        
        distribution = defaultdict(int)
        for _, engagement_type, _ in self.content_engagements[content_id]:
            distribution[engagement_type] += 1
        
        return dict(distribution)
    
    def predict_viral_potential(self, content_id: str) -> Dict:
        """
        Predict viral potential based on early engagement patterns.
        
        Returns:
            Prediction metrics and probability
        """
        if content_id not in self.content_engagements:
            return {'viral_probability': 0.0, 'confidence': 'low'}
        
        engagements = self.content_engagements[content_id]
        if len(engagements) < 10:  # Need minimum data
            return {'viral_probability': 0.0, 'confidence': 'insufficient_data'}
        
        # Analyze early patterns (first 30 minutes)
        current_time = time.time()
        first_engagement = engagements[0][0]
        early_window = first_engagement + 30 * 60  # 30 minutes
        
        early_engagements = [
            (ts, et, w) for ts, et, w in engagements 
            if ts <= early_window
        ]
        
        if len(early_engagements) < 5:
            return {'viral_probability': 0.0, 'confidence': 'low'}
        
        # Calculate early metrics
        early_velocity = len(early_engagements) * 2  # Per hour rate
        engagement_diversity = len(set(et for _, et, _ in early_engagements))
        high_value_engagements = sum(1 for _, et, _ in early_engagements if et in ['share', 'save'])
        
        # Simple viral probability calculation
        viral_probability = min(1.0, (
            (early_velocity / 100) * 0.4 +
            (engagement_diversity / 5) * 0.3 +
            (high_value_engagements / len(early_engagements)) * 0.3
        ))
        
        confidence = 'high' if len(early_engagements) > 50 else 'medium'
        
        return {
            'viral_probability': viral_probability,
            'confidence': confidence,
            'early_velocity': early_velocity,
            'engagement_diversity': engagement_diversity,
            'high_value_ratio': high_value_engagements / len(early_engagements)
        }

# Test the viral detection system
def test_viral_detection():
    detector = ViralContentDetector()
    
    # Simulate normal content
    base_time = time.time() - 3600  # 1 hour ago
    
    # Normal content with steady engagement
    for i in range(50):
        detector.add_engagement('normal_content', 'view', base_time + i * 60)
        if i % 5 == 0:
            detector.add_engagement('normal_content', 'like', base_time + i * 60)
    
    # Viral content with accelerating engagement
    viral_start = base_time + 1800  # 30 minutes ago
    for i in range(200):
        # Exponential growth pattern
        timestamp = viral_start + i * 10 + (i ** 1.5)
        detector.add_engagement('viral_content', 'view', timestamp)
        
        if i % 3 == 0:
            detector.add_engagement('viral_content', 'like', timestamp)
        if i % 10 == 0:
            detector.add_engagement('viral_content', 'share', timestamp)
    
    # Check velocities
    normal_velocity = detector.calculate_engagement_velocity('normal_content')
    viral_velocity = detector.calculate_engagement_velocity('viral_content')
    
    print(f"Normal content velocity: {normal_velocity:.2f} engagements/hour")
    print(f"Viral content velocity: {viral_velocity:.2f} engagements/hour")
    
    # Detect viral content
    viral_content = detector.detect_viral_content()
    print(f"Detected viral content: {viral_content}")
    
    # Predict viral potential
    prediction = detector.predict_viral_potential('viral_content')
    print(f"Viral prediction: {prediction}")
    
    print("Viral detection test completed!")

if __name__ == "__main__":
    test_viral_detection()
```

## Key Concepts Tested

1. **Event Stream Processing**: Real-time processing of user interaction logs
2. **Time Series Analysis**: Calculating velocities and trends over time windows
3. **Recommendation Systems**: Multi-factor scoring and ranking algorithms
4. **Pattern Recognition**: Identifying viral content characteristics
5. **Data Structure Optimization**: Efficient storage and retrieval for real-time systems
6. **Statistical Analysis**: Velocity, acceleration, and trend calculations 

## Python Question 2.4.1: Fixed-Size Buffer for Event Stream Processing

Implement two Python functions for processing a stream of events (e.g., from a short video platform like TikTok or Reels) using a fixed-size buffer:

1.  `process_fixed_buffer_stream(event_item, buffer, buffer_size, totals_engagement, totals_view_seconds, test_users)`:
    *   Takes an `event_item` (dictionary) and processes it through a fixed-size `buffer`.
    *   When the `buffer` is full (reaches `buffer_size`), processes the oldest item from the buffer.
    *   Tracks engagement counts (`totals_engagement`) and total view durations in seconds (`totals_view_seconds`), excluding events from `test_users`.
    *   Adds the new `event_item` to the buffer.

2.  `flush_fixed_buffer(buffer, totals_engagement, totals_view_seconds, test_users)`:
    *   Processes all remaining items in the `buffer`.
    *   Updates `totals_engagement` and `totals_view_seconds` accordingly, excluding `test_users`.

This system is useful for real-time analytics where events are processed in chunks, for example, to calculate rolling engagement metrics for short videos.

**DATA STRUCTURE EXAMPLES:**

Input: `event_item` (dict)
- Structure: `{'user_id': str, 'event_type': str, 'post_id': str|list, 'view_duration_ms': int (optional)}`
- `event_type` values: 'like', 'comment', 'share', 'view'
- `view_duration_ms`: only present for 'view' events (in milliseconds)

Examples:
- Engagement event: `{'user_id': 'user123', 'event_type': 'like', 'post_id': ['p1']}`
- View event: `{'user_id': 'user456', 'event_type': 'view', 'post_id': 'p2', 'view_duration_ms': 5000}`

Input: `buffer` (list)
- Structure: `[event_item1, event_item2, ...]` (FIFO queue)

Input: `buffer_size` (int)
- Example: `3`

Input: `totals_engagement` (list with single int, e.g., `[0]`)
- Counts 'like', 'comment', 'share' events.

Input: `totals_view_seconds` (list with single float, e.g., `[0.0]`)
- Accumulates view duration in seconds.

Input: `test_users` (set)
- Example: `{'test_user_reel', 'internal_user_123'}`

**BUFFER PROCESSING FLOW EXAMPLE:**

Initial state:
`buffer = []`, `buffer_size = 3`, `totals_engagement = [0]`, `totals_view_seconds = [0.0]`

1.  Add event1 (`like`): `buffer = [event1]`. Totals unchanged.
2.  Add event2 (`view`, 10000ms): `buffer = [event1, event2]`. Totals unchanged.
3.  Add event3 (`comment`): `buffer = [event1, event2, event3]`. Totals unchanged.
4.  Add event4 (`share`): (Buffer is full, oldest event1 is processed)
    *   Process event1 (`like`): `totals_engagement = [1]`.
    *   `buffer = [event2, event3, event4]`.

**Flush buffer (at the end):**
- Process event2 (`view`, 10000ms): `totals_view_seconds = [10.0]` (assuming event2 is not from a test user).
- Process event3 (`comment`): `totals_engagement = [2]` (assuming event3 is not from a test user).
- Process event4 (`share`): `totals_engagement = [3]` (assuming event4 is not from a test user).
- `buffer = []`.
Final totals: `totals_engagement = [3]`, `totals_view_seconds = [10.0]`.

**Function Signatures:**
```python
def process_fixed_buffer_stream(event_item, buffer, buffer_size, totals_engagement, totals_view_seconds, test_users):
    # ... implementation ...

def flush_fixed_buffer(buffer, totals_engagement, totals_view_seconds, test_users):
    # ... implementation ...
``` 