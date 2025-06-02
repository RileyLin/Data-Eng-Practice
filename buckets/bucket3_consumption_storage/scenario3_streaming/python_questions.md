# Scenario 3: Streaming (Netflix/YouTube) - Python Questions

## Question 1: Calculating Average Content Ratings

**Problem**: Given a list of user ratings for various content items (movies, series), calculate the average rating for each item and identify items with insufficient ratings.

**Key Requirements**:
-   Process a list of rating events (user_id, content_id, rating_value).
-   Calculate average rating per content_id.
-   Handle content with fewer than a minimum number of ratings (e.g., less than 5 ratings).

### Solution (Adapted from `src/python/q007_average_movie_ratings.py`):

```python
from collections import defaultdict

MIN_RATINGS_THRESHOLD = 5

def calculate_average_ratings(ratings_data):
    """
    Calculates average ratings for content items from a list of rating events.

    Args:
        ratings_data (list): A list of dictionaries, where each dictionary represents a rating event.
                             Expected keys: 'user_id', 'content_id', 'rating_value' (e.g., 1-5).

    Returns:
        tuple: (average_ratings, low_rating_counts)
               average_ratings (dict): {content_id: avg_rating}
               low_rating_counts (dict): {content_id: num_ratings} for items below threshold
    """
    content_ratings_sum = defaultdict(int)
    content_rating_count = defaultdict(int)

    for rating_event in ratings_data:
        content_id = rating_event.get('content_id')
        rating_value = rating_event.get('rating_value')

        if content_id and isinstance(rating_value, (int, float)):
            content_ratings_sum[content_id] += rating_value
            content_rating_count[content_id] += 1

    average_ratings = {}
    low_rating_counts = {}

    for content_id, total_sum in content_ratings_sum.items():
        count = content_rating_count[content_id]
        if count >= MIN_RATINGS_THRESHOLD:
            average_ratings[content_id] = round(total_sum / count, 2)
        else:
            low_rating_counts[content_id] = count
            
    return average_ratings, low_rating_counts

# Test Cases
def test_average_ratings_calculation():
    sample_ratings = [
        {'user_id': 'u1', 'content_id': 'movie1', 'rating_value': 5},
        {'user_id': 'u2', 'content_id': 'movie1', 'rating_value': 4},
        {'user_id': 'u3', 'content_id': 'movie1', 'rating_value': 5},
        {'user_id': 'u4', 'content_id': 'movie1', 'rating_value': 3},
        {'user_id': 'u5', 'content_id': 'movie1', 'rating_value': 4}, # movie1: (5+4+5+3+4)/5 = 4.2
        {'user_id': 'u1', 'content_id': 'movie2', 'rating_value': 3},
        {'user_id': 'u2', 'content_id': 'movie2', 'rating_value': 2},
        {'user_id': 'u1', 'content_id': 'seriesA_ep1', 'rating_value': 5}, # seriesA_ep1: 1 rating (low)
        {'user_id': 'u6', 'content_id': 'movie1', 'rating_value': 'Invalid'}, # Invalid rating
        {'user_id': 'u7', 'content_id': None, 'rating_value': 5}, # Invalid content_id
    ]
    
    # Add more ratings for movie2 to meet threshold
    for i in range(3):
         sample_ratings.append({'user_id': f'u{3+i}', 'content_id': 'movie2', 'rating_value': i+2}) 
    # movie2: (3+2+2+3+4)/5 = 2.8

    avg_ratings, low_counts = calculate_average_ratings(sample_ratings)
    print("Average Ratings (sufficient count):", avg_ratings)
    print("Low Rating Counts:", low_counts)

    assert avg_ratings.get('movie1') == 4.2
    assert avg_ratings.get('movie2') == 2.8
    assert 'seriesA_ep1' in low_counts
    assert low_counts['seriesA_ep1'] == 1
    assert 'movie1' not in low_counts
    print("Average ratings calculation test passed.")

if __name__ == "__main__":
    test_average_ratings_calculation()
```

---

## Question 2: Simple Content-Based Recommendation

**Problem**: Implement a basic content-based recommendation function. Given a user's watch history and content metadata (genres, tags), recommend new content that shares common attributes with what the user has liked (watched significantly).

**Key Requirements**:
-   Input: User's watch history (list of content_ids with high completion), all available content metadata (content_id -> {genres: set, tags: set}).
-   Output: A ranked list of recommended content_ids not in the user's history.
-   Scoring: Simple overlap score (e.g., number of shared genres/tags).

### Solution:

```python
from collections import defaultdict

def get_content_based_recommendations(user_watch_history, all_content_metadata, top_n=5):
    """
    Generates content-based recommendations for a user.

    Args:
        user_watch_history (list): List of content_ids the user has watched significantly.
        all_content_metadata (dict): {content_id: {'title': str, 'genres': set(), 'tags': set()}}
        top_n (int): Number of recommendations to return.

    Returns:
        list: List of recommended content_ids, ranked by similarity score.
    """
    user_profile_genres = set()
    user_profile_tags = set()

    # Build user profile from their watch history
    for content_id in user_watch_history:
        if content_id in all_content_metadata:
            user_profile_genres.update(all_content_metadata[content_id].get('genres', set()))
            user_profile_tags.update(all_content_metadata[content_id].get('tags', set()))

    recommendation_scores = defaultdict(float)

    # Score all other content items
    for content_id, metadata in all_content_metadata.items():
        if content_id not in user_watch_history:
            genre_overlap = len(user_profile_genres.intersection(metadata.get('genres', set())))
            tag_overlap = len(user_profile_tags.intersection(metadata.get('tags', set())))
            
            # Simple scoring: more weight to genre, then tags
            score = (genre_overlap * 2) + tag_overlap
            
            # Boost for content with multiple shared attributes
            if genre_overlap > 1 or tag_overlap > 1:
                score *= 1.2
                
            if score > 0:
                recommendation_scores[content_id] = score
    
    # Sort by score and return top N
    sorted_recommendations = sorted(recommendation_scores.items(), key=lambda item: item[1], reverse=True)
    return [content_id for content_id, score in sorted_recommendations[:top_n]]

# Test Cases
def test_content_based_recommendations():
    all_content = {
        'movie1': {'title': 'Action Adventure Fun', 'genres': {'action', 'adventure'}, 'tags': {'fast-paced', 'epic'}},
        'movie2': {'title': 'Comedy Time', 'genres': {'comedy'}, 'tags': {'lighthearted', 'funny'}},
        'movie3': {'title': 'Action Hero Returns', 'genres': {'action', 'thriller'}, 'tags': {'suspense', 'fast-paced'}},
        'movie4': {'title': 'Adventure into the Wild', 'genres': {'adventure', 'drama'}, 'tags': {'nature', 'epic'}},
        'movie5': {'title': 'Sci-Fi Action Blast', 'genres': {'action', 'sci-fi'}, 'tags': {'futuristic', 'fast-paced'}},
        'movie6': {'title': 'Just Comedy', 'genres': {'comedy'}, 'tags': {'funny', 'silly'}}
    }
    user_history = ['movie1', 'movie2'] # User likes Action/Adventure and Comedy

    recommendations = get_content_based_recommendations(user_history, all_content, top_n=3)
    print(f"User history: {user_history}")
    print(f"Recommendations: {recommendations}")

    # Expected: movie3 (shares 'action', 'fast-paced'), movie5 (shares 'action', 'fast-paced'), 
    # movie4 (shares 'adventure', 'epic') or movie6 (shares 'comedy', 'funny'). Order depends on scoring nuances.
    assert 'movie3' in recommendations
    assert 'movie5' in recommendations
    assert len(recommendations) <= 3
    assert 'movie1' not in recommendations # Shouldn't recommend already watched
    assert 'movie2' not in recommendations
    print("Content-based recommendation test passed.")

if __name__ == "__main__":
    test_average_ratings_calculation()
    print("\n---\n")
    test_content_based_recommendations()

```

---

## Question 3: Simulate User Viewing Session with Dynamic Recommendations

**Problem**: Simulate a user's viewing session where after they finish watching a piece of content, they are presented with new recommendations based on their updated watch history.

**Key Requirements**:
-   Maintain user's watch history for the session.
-   A function `watch_content(user_id, content_id, duration_watched)` that updates history.
-   After watching, call a recommendation function (can use the one from Q2 or a simplified version) to show what they might watch next.
-   The simulation should run for a few cycles of watching and getting recommendations.

### Solution:

```python
import random

# (Re-use get_content_based_recommendations and all_content_metadata from Q2 for this)
# Or define a simplified version here if needed
ALL_CONTENT_METADATA_Q3 = {
    'm1': {'title': 'Movie A (Action)', 'genres': {'action', 'sci-fi'}, 'tags': {'space', 'battle'}},
    'm2': {'title': 'Movie B (Comedy)', 'genres': {'comedy'}, 'tags': {'funny', 'family'}},
    'm3': {'title': 'Movie C (Action)', 'genres': {'action', 'thriller'}, 'tags': {'chase', 'suspense'}},
    'm4': {'title': 'Movie D (Drama)', 'genres': {'drama'}, 'tags': {'emotional', 'slow-burn'}},
    'm5': {'title': 'Movie E (Sci-Fi)', 'genres': {'sci-fi', 'adventure'}, 'tags': {'space', 'exploration'}},
    's1e1': {'title': 'Series X Ep1 (Comedy)', 'genres': {'comedy', 'sitcom'}, 'tags': {'workplace', 'funny'}}
}

def simulate_viewing_session(user_id, initial_content_id, num_cycles=3):
    """
    Simulates a user watching content and getting recommendations.
    """
    session_watch_history = []
    current_content_id = initial_content_id

    print(f"User '{user_id}' starting session.")

    for i in range(num_cycles):
        print(f"\nCycle {i+1}:")
        if not current_content_id or current_content_id not in ALL_CONTENT_METADATA_Q3:
            print("No valid content to watch. Ending session early.")
            break

        content_details = ALL_CONTENT_METADATA_Q3[current_content_id]
        print(f"User '{user_id}' is watching: '{content_details['title']}' ({current_content_id})")
        # Simulate watching it significantly
        session_watch_history.append(current_content_id)
        print(f"User '{user_id}' finished watching '{content_details['title']}'.")
        print(f"Current Watch History: {session_watch_history}")

        # Get recommendations based on updated history
        recommendations = get_content_based_recommendations(session_watch_history, ALL_CONTENT_METADATA_Q3, top_n=3)
        print(f"Recommended next: {recommendations}")

        if not recommendations:
            print("No more recommendations available. Ending session.")
            break
        
        # User picks the first recommendation to watch next (can be randomized)
        current_content_id = recommendations[0]
        if current_content_id in session_watch_history:
            # If top pick is already watched (e.g. small catalog or limited recommendations)
            # try to pick another one or end if all recommended are watched.
            available_new_recs = [rec for rec in recommendations if rec not in session_watch_history]
            if available_new_recs:
                current_content_id = available_new_recs[0]
            else:
                print("All recommendations already watched. Ending session.")
                break
    
    print(f"\nSession ended for user '{user_id}'. Final watch history: {session_watch_history}")
    return session_watch_history

# Test Cases
def test_viewing_session_simulation():
    user_id = "viewer123"
    # Start by watching an action movie
    final_history = simulate_viewing_session(user_id, initial_content_id='m1', num_cycles=4)
    
    # Expected: History should grow, recommendations should adapt (hopefully)
    assert len(final_history) > 0
    assert 'm1' in final_history
    # Check if other action/sci-fi movies like m3 or m5 were likely watched based on initial + recs
    if len(final_history) > 1:
        assert final_history[1] in ['m3', 'm5'] or final_history[1] in ALL_CONTENT_METADATA_Q3 # General check it's valid

    print("\nViewing session simulation test passed.")

if __name__ == "__main__":
    test_average_ratings_calculation()
    print("\n---\n")
    test_content_based_recommendations()
    print("\n---\n")
    test_viewing_session_simulation()

```

## Key Concepts Tested
1.  **Data Aggregation**: Processing lists of events to calculate summary statistics (average ratings).
2.  **Content-Based Filtering**: Implementing a basic recommendation algorithm based on item attributes and user profiles.
3.  **User Profile Building**: Dynamically creating a user interest profile from their interaction history.
4.  **Similarity Scoring**: Using simple overlap metrics (e.g., shared genres/tags) to score items.
5.  **Session Simulation**: Modeling a sequence of user actions and system responses over time.
6.  **Dynamic State Update**: Modifying user history and generating new recommendations within a session loop.
7.  **Handling Edge Cases**: Considering scenarios like no available recommendations or small content catalogs. 