# Scenario 6: News Feed (Facebook/LinkedIn) - Python Questions

## Question 1: Newsfeed View Validation

**Problem**: Process a stream of newsfeed interaction events to determine valid views for each post in each session. A view is considered valid if the user spent at least 3 seconds on the post OR interacted with it (e.g., like, comment, share).

**Key Requirements**:
-   Correctly attribute `view_time` to posts within a session.
-   Handle multiple interaction types.
-   Aggregate total valid views per post across all sessions.

### Solution (Adapted from `src/python/q008_newsfeed_view_validation.py`):

```python
from collections import defaultdict

def process_feed_event(event, session_data, post_view_details):
    """
    Processes a single newsfeed event to update session data and post view details.

    Args:
        event (dict): A dictionary representing a newsfeed event.
                      Expected keys: 'session_id', 'user_id', 'timestamp', 'event_type',
                                     'post_id', 'view_time_seconds' (optional).
        session_data (defaultdict): A dictionary to store active session information.
                                    Key: session_id, Value: dict of post_id -> {view_duration, interacted}
        post_view_details (defaultdict): A dictionary to store aggregated post view info.
                                         Key: post_id, Value: {total_view_time, interactions, valid_views_count}
    """
    session_id = event.get('session_id')
    post_id = event.get('post_id')
    event_type = event.get('event_type')
    view_time = event.get('view_time_seconds', 0)

    if not session_id or not post_id:
        return # Invalid event

    # Initialize post in session if not present
    if post_id not in session_data[session_id]:
        session_data[session_id][post_id] = {'view_duration': 0, 'interacted': False, 'counted_valid': False}

    current_post_in_session = session_data[session_id][post_id]

    if event_type == 'view':
        current_post_in_session['view_duration'] += view_time
        post_view_details[post_id]['total_view_time'] = post_view_details[post_id].get('total_view_time', 0) + view_time
    elif event_type in ['like', 'comment', 'share', 'click']:
        current_post_in_session['interacted'] = True
        post_view_details[post_id]['interactions'] = post_view_details[post_id].get('interactions', 0) + 1
    
    # Check for valid view conditions if not already counted for this session
    if not current_post_in_session['counted_valid']:
        if current_post_in_session['view_duration'] >= 3 or current_post_in_session['interacted']:
            post_view_details[post_id]['valid_views_count'] = post_view_details[post_id].get('valid_views_count', 0) + 1
            current_post_in_session['counted_valid'] = True

    if event_type == 'session_end':
        # Clean up session data if necessary, or simply mark posts as no longer active in this session
        # For this example, we'll just clear the specific session data as posts are processed per event
        if session_id in session_data:
            del session_data[session_id]

def get_valid_post_views(post_view_details):
    """
    Returns a summary of valid views per post.
    """
    return {post_id: data.get('valid_views_count', 0) for post_id, data in post_view_details.items()}

# Test Cases
def test_newsfeed_validation():
    session_data = defaultdict(dict)
    post_view_details = defaultdict(lambda: {'total_view_time': 0, 'interactions': 0, 'valid_views_count': 0})

    events = [
        {'session_id': 's1', 'user_id': 'u1', 'timestamp': 100, 'event_type': 'view', 'post_id': 'p1', 'view_time_seconds': 2},
        {'session_id': 's1', 'user_id': 'u1', 'timestamp': 102, 'event_type': 'view', 'post_id': 'p1', 'view_time_seconds': 2}, # p1 valid (total 4s)
        {'session_id': 's1', 'user_id': 'u1', 'timestamp': 105, 'event_type': 'view', 'post_id': 'p2', 'view_time_seconds': 1},
        {'session_id': 's1', 'user_id': 'u1', 'timestamp': 106, 'event_type': 'like', 'post_id': 'p2'}, # p2 valid (liked)
        {'session_id': 's1', 'user_id': 'u1', 'timestamp': 110, 'event_type': 'view', 'post_id': 'p3', 'view_time_seconds': 2}, # p3 not valid yet
        {'session_id': 's2', 'user_id': 'u2', 'timestamp': 200, 'event_type': 'view', 'post_id': 'p1', 'view_time_seconds': 5}, # p1 valid again in new session
        {'session_id': 's2', 'user_id': 'u2', 'timestamp': 205, 'event_type': 'session_end'},
        {'session_id': 's1', 'user_id': 'u1', 'timestamp': 120, 'event_type': 'session_end'},
    ]

    for event in events:
        process_feed_event(event, session_data, post_view_details)

    valid_views = get_valid_post_views(post_view_details)
    print("Valid Post Views:", valid_views)
    assert valid_views.get('p1', 0) == 2, f"Error for p1: Expected 2, got {valid_views.get('p1',0)}"
    assert valid_views.get('p2', 0) == 1, f"Error for p2: Expected 1, got {valid_views.get('p2',0)}"
    assert valid_views.get('p3', 0) == 0, f"Error for p3: Expected 0, got {valid_views.get('p3',0)}"
    print("Newsfeed validation test passed!")

if __name__ == "__main__":
    test_newsfeed_validation()

```

---

## Question 2: Simplified Feed Ranking Algorithm

**Problem**: Implement a basic news feed ranking algorithm that scores posts based on recency, interaction counts (likes, comments, shares with different weights), and user's affinity for the content source.

**Key Requirements**:
-   Input: A list of candidate posts and user profile information.
-   Output: A ranked list of post IDs.
-   Scoring: Customizable weights for recency, likes, comments, shares, and source affinity.

### Solution:

```python
import time
from collections import defaultdict

def rank_feed_posts(user_profile, candidate_posts, weights):
    """
    Ranks candidate posts for a user's news feed.

    Args:
        user_profile (dict): Contains user's affinities, e.g., {'source_affinities': {'source1': 0.8, 'source2': 0.3}}.
        candidate_posts (list): List of post dictionaries. Each post should have:
                                'post_id', 'source_id', 'timestamp', 'likes', 'comments', 'shares'.
        weights (dict): Weights for scoring components, e.g., 
                        {'recency': 0.2, 'likes': 0.3, 'comments': 0.3, 'shares': 0.1, 'affinity': 0.1}

    Returns:
        list: Ranked list of post_ids.
    """
    scored_posts = []
    current_timestamp = time.time()
    source_affinities = user_profile.get('source_affinities', {})

    for post in candidate_posts:
        score = 0

        # Recency score (higher for newer posts, max age 7 days)
        age_seconds = current_timestamp - post.get('timestamp', current_timestamp)
        recency_score = max(0, 1 - (age_seconds / (7 * 24 * 3600))) # Normalized 0-1
        score += recency_score * weights.get('recency', 0)

        # Engagement scores
        score += post.get('likes', 0) * weights.get('likes', 0)
        score += post.get('comments', 0) * weights.get('comments', 0) * 1.5 # Comments weighted higher
        score += post.get('shares', 0) * weights.get('shares', 0) * 2.0 # Shares weighted highest

        # Source affinity score
        affinity = source_affinities.get(post.get('source_id'), 0.1) # Default affinity if not specified
        score += affinity * weights.get('affinity', 0)
        
        # Bonus for posts from highly affined sources
        if affinity > 0.7:
            score *= 1.1 # 10% bonus

        scored_posts.append({'post_id': post['post_id'], 'score': score})

    # Sort posts by score in descending order
    ranked_posts = sorted(scored_posts, key=lambda x: x['score'], reverse=True)
    return [p['post_id'] for p in ranked_posts]

# Test Cases
def test_feed_ranking():
    user_profile = {
        'user_id': 'u1',
        'source_affinities': {'s1': 0.9, 's2': 0.4, 's3': 0.1}
    }
    candidate_posts = [
        {'post_id': 'p1', 'source_id': 's1', 'timestamp': time.time() - 3600, 'likes': 10, 'comments': 2, 'shares': 1},
        {'post_id': 'p2', 'source_id': 's2', 'timestamp': time.time() - 7200, 'likes': 50, 'comments': 10, 'shares': 5},
        {'post_id': 'p3', 'source_id': 's3', 'timestamp': time.time() - 300, 'likes': 2, 'comments': 0, 'shares': 0},
        {'post_id': 'p4', 'source_id': 's1', 'timestamp': time.time() - 86400*3, 'likes': 100, 'comments': 20, 'shares': 10}, # Older but high engagement
        {'post_id': 'p5', 'source_id': 's4', 'timestamp': time.time() - 600, 'likes': 5, 'comments': 1, 'shares': 0} # Unknown source
    ]
    weights = {'recency': 0.2, 'likes': 0.1, 'comments': 0.3, 'shares': 0.3, 'affinity': 0.1}

    ranked_feed = rank_feed_posts(user_profile, candidate_posts, weights)
    print("Ranked Feed:", ranked_feed)
    
    # Expected: p2 likely high due to engagement, p1 benefits from affinity and recency, p3 recent but low engagement/affinity
    # The exact order depends on the interplay of weights. This test is more for execution check.
    assert len(ranked_feed) == len(candidate_posts)
    print("Feed ranking test executed.")

if __name__ == "__main__":
    test_newsfeed_validation()
    test_feed_ranking()
```

---

## Question 3: Feed Content Diversity Algorithm

**Problem**: Implement an algorithm to ensure diversity in a user's news feed. After an initial ranking, re-order or select posts to prevent too many consecutive posts from the same source or of the same content type.

**Key Requirements**:
-   Input: A ranked list of post objects (containing `post_id`, `source_id`, `content_type`).
-   Output: A diversified list of post IDs.
-   Constraints: e.g., no more than 2 consecutive posts from the same source, no more than 3 consecutive posts of the same content type.

### Solution:

```python
from collections import deque

def diversify_feed(ranked_posts, max_consecutive_source=2, max_consecutive_type=3):
    """
    Diversifies a ranked feed to avoid too many consecutive similar posts.

    Args:
        ranked_posts (list): List of post dictionaries, already ranked by relevance.
                             Each post: {'post_id', 'source_id', 'content_type', ...}
        max_consecutive_source (int): Max allowed consecutive posts from the same source.
        max_consecutive_type (int): Max allowed consecutive posts of the same content type.

    Returns:
        list: Diversified list of post_ids.
    """
    diversified_feed_ids = []
    source_history = deque()
    type_history = deque()
    
    temp_hold = [] # To hold posts that are temporarily skipped for diversity

    available_posts = deque(ranked_posts)

    while available_posts or temp_hold:
        candidate_post = None
        found_suitable_post = False

        # Try to pick from available_posts first
        for _ in range(len(available_posts)):
            post = available_posts.popleft()
            
            # Check source diversity
            source_count = sum(1 for s_id in source_history if s_id == post['source_id'])
            if source_count >= max_consecutive_source:
                temp_hold.append(post)
                continue
            
            # Check content type diversity
            type_count = sum(1 for c_type in type_history if c_type == post['content_type'])
            if type_count >= max_consecutive_type:
                temp_hold.append(post)
                continue
            
            candidate_post = post
            found_suitable_post = True
            break # Found a suitable post
        
        # If no suitable post from available_posts, try from temp_hold (less ideal but ensures progress)
        if not found_suitable_post and temp_hold:
            # Simple strategy: pick the first one from temp_hold, relaxing constraints slightly if needed
            # A more sophisticated approach might re-score or prioritize based on original rank
            candidate_post = temp_hold.pop(0) 
            # We accept this post even if it slightly violates, to prevent infinite loops if all remaining posts are similar.
            # In a production system, you might have more graceful fallback or re-ranking.
        
        if candidate_post:
            diversified_feed_ids.append(candidate_post['post_id'])
            
            # Update source history
            source_history.append(candidate_post['source_id'])
            if len(source_history) > max_consecutive_source:
                source_history.popleft()
            
            # Update type history
            type_history.append(candidate_post['content_type'])
            if len(type_history) > max_consecutive_type:
                type_history.popleft()
            
            # Add remaining temp_hold items back to available_posts to be reconsidered
            # This ensures posts that were skipped earlier get another chance soon
            while temp_hold:
                 # Insert at the beginning to prioritize originally higher-ranked items
                available_posts.appendleft(temp_hold.pop())
        elif not available_posts and not temp_hold: # No more posts to process
            break

    return diversified_feed_ids

# Test Cases
def test_feed_diversification():
    ranked_posts_sample = [
        {'post_id': 'p1', 'source_id': 's1', 'content_type': 'video'},
        {'post_id': 'p2', 'source_id': 's1', 'content_type': 'photo'},
        {'post_id': 'p3', 'source_id': 's1', 'content_type': 'text'},  # s1 limit might be hit
        {'post_id': 'p4', 'source_id': 's2', 'content_type': 'video'},
        {'post_id': 'p5', 'source_id': 's3', 'content_type': 'video'}, # video limit might be hit
        {'post_id': 'p6', 'source_id': 's2', 'content_type': 'video'},
        {'post_id': 'p7', 'source_id': 's1', 'content_type': 'photo'},
        {'post_id': 'p8', 'source_id': 's4', 'content_type': 'text'},
        {'post_id': 'p9', 'source_id': 's4', 'content_type': 'text'},
        {'post_id': 'p10', 'source_id': 's4', 'content_type': 'text'}, # s4 and text limit
    ]

    diversified_feed = diversify_feed(ranked_posts_sample, max_consecutive_source=2, max_consecutive_type=2)
    print("Original Ranked IDs:", [p['post_id'] for p in ranked_posts_sample])
    print("Diversified Feed IDs:", diversified_feed)

    # Verification (visual inspection or more rigorous checks)
    # Check s1: p1, p2, (p3 held), p4, p5, p6, p7 (s1 again, ok), ...
    # Check video: p1, p4, (p5 held), p6 (video again, ok if source changed), ...
    # This test is primarily for execution and basic logic flow
    unique_output_posts = len(set(diversified_feed))
    assert len(diversified_feed) >= len(ranked_posts_sample) - 3 # Allow for some posts to be dropped in simple model if no choice
    assert unique_output_posts == len(diversified_feed), "Duplicates in diversified feed"

    print("Feed diversification test executed.")

if __name__ == "__main__":
    test_newsfeed_validation()
    test_feed_ranking()
    test_feed_diversification()

```

## Key Concepts Tested
1.  **Event Stream Processing**: Handling sequences of user interaction data.
2.  **Sessionization**: Grouping events by user sessions to define context for views.
3.  **Ranking Algorithms**: Applying weighted scoring based on multiple features (recency, engagement, affinity).
4.  **Personalization**: Tailoring content ranking to individual user preferences.
5.  **Diversity Algorithms**: Re-ranking or filtering to improve user experience by avoiding monotony.
6.  **Data Structures**: Using dictionaries and deques for efficient tracking and manipulation of post states and history.
7.  **Time-based Calculations**: Handling timestamps for recency scoring. 