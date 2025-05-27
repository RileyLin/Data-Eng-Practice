"""
Scenario 3: Streaming Platform (Netflix/Hulu)
Question 3.4.3: Average Rating per Movie

Description:
Given a list of movie rating instances (each with title and rating),
calculate the average rating for each unique movie title.
Implement the function `calculate_average_movie_ratings(movie_data)`
that returns a dictionary mapping each movie title to its average rating.

Example:
movie_data = [
    {'title': 'Movie A', 'rating': 4.5},
    {'title': 'Movie B', 'rating': 3.0},
    {'title': 'Movie A', 'rating': 3.5},
    {'title': 'Movie C', 'rating': 5.0},
    {'title': 'Movie B', 'rating': 4.0},
]
Expected Output: {'Movie A': 4.0, 'Movie B': 3.5, 'Movie C': 5.0}

movie_data_empty = []
Expected Output: {}

movie_data_single = [{'title': 'Solo Flick', 'rating': 2.5}]
Expected Output: {'Solo Flick': 2.5}

Solution to Average Movie Ratings

DATA STRUCTURE EXAMPLES:

Input: movie_data (List[Dict])
- Structure: [{'title': str, 'rating': float|str}, ...]
- Each rating instance should have 'title' and 'rating' keys
- 'rating' can be float or string (will be converted to float)
- Multiple instances can have the same title (different ratings)

Example rating instances:
- Valid instance: {'title': 'Movie Alpha', 'rating': 8.0}
- String rating: {'title': 'Movie Beta', 'rating': '7.5'}
- Missing rating: {'title': 'Movie Gamma'} # Will be skipped
- Missing title: {'rating': 9.0} # Will be skipped
- Invalid rating: {'title': 'Movie Delta', 'rating': 'invalid'} # Will be skipped

Output: Dict[str, float]
- Structure: {movie_title: average_rating}
- movie_title: string representing the movie title
- average_rating: float representing the average rating for that movie

Example Input:
movie_ratings_list = [
    {'title': 'Movie Alpha', 'rating': 8.0},
    {'title': 'Movie Beta', 'rating': 7.0},
    {'title': 'Movie Alpha', 'rating': 9.0},
    {'title': 'Movie Alpha', 'rating': 8.5},
    {'title': 'Movie Beta', 'rating': 7.5},
]

Processing breakdown:
Movie Alpha ratings: [8.0, 9.0, 8.5] → Average: (8.0 + 9.0 + 8.5) / 3 = 8.5
Movie Beta ratings: [7.0, 7.5] → Average: (7.0 + 7.5) / 2 = 7.25

Expected Output:
{
    'Movie Alpha': 8.5,  # (8.0 + 9.0 + 8.5) / 3 = 8.5
    'Movie Beta': 7.25   # (7.0 + 7.5) / 2 = 7.25
}

Edge Cases:
- Empty input: [] → {}
- Single rating per movie: [{'title': 'Movie A', 'rating': 5.0}] → {'Movie A': 5.0}
- All instances missing required fields: [{'other_field': 'value'}] → {}
- Duplicate exact instances: Same title and rating appear multiple times
- Mixed valid/invalid instances: Only valid instances are processed

Real-world scenario:
This function could be used to aggregate movie ratings from multiple sources or users,
where each rating instance represents one person's rating of a movie.
"""

from collections import defaultdict

def calculate_average_movie_ratings(movie_data: list[dict]) -> dict[str, float]:
    """
    Calculates the average rating for each unique movie title.

    Args:
        movie_data: A list of dictionaries, where each dictionary represents
                    a movie rating instance with 'title' (str) and 'rating' (float).

    Returns:
        A dictionary mapping each movie title (str) to its average rating (float).
    """
    if not movie_data:
        return {}

    ratings_sum = defaultdict(float)
    ratings_count = defaultdict(int)

    for entry in movie_data:
        title = entry.get('title')
        rating = entry.get('rating')

        if title is not None and isinstance(rating, (int, float)):
            ratings_sum[title] += rating
            ratings_count[title] += 1

    average_ratings = {}
    for title, total_rating in ratings_sum.items():
        count = ratings_count[title]
        if count > 0:
            average_ratings[title] = total_rating / count
        else:
            # This case should ideally not be reached if input validation is robust
            # or if titles are guaranteed to have at least one rating.
            # Depending on requirements, could return 0.0 or raise an error.
            average_ratings[title] = 0.0

    return average_ratings


# Example Usage
if __name__ == "__main__":
    # Example 1
    movie_data1 = [
        {'title': 'Movie A', 'rating': 4.5},
        {'title': 'Movie B', 'rating': 3.0},
        {'title': 'Movie A', 'rating': 3.5},
        {'title': 'Movie C', 'rating': 5.0},
        {'title': 'Movie B', 'rating': 4.0},
    ]
    expected_output1 = {'Movie A': 4.0, 'Movie B': 3.5, 'Movie C': 5.0}
    print(f"Movie Data 1: {movie_data1}")
    result1 = calculate_average_movie_ratings(movie_data1)
    print(f"Calculated Average Ratings: {result1}")
    print(f"Expected Output: {expected_output1}")
    assert result1 == expected_output1, f"Test Case 1 Failed: Expected {expected_output1}, got {result1}"
    print("Test Case 1 Passed\n")

    # Example 2: Empty list
    movie_data_empty = []
    expected_output_empty = {}
    print(f"Movie Data Empty: {movie_data_empty}")
    result_empty = calculate_average_movie_ratings(movie_data_empty)
    print(f"Calculated Average Ratings: {result_empty}")
    print(f"Expected Output: {expected_output_empty}")
    assert result_empty == expected_output_empty, f"Test Case Empty Failed: Expected {expected_output_empty}, got {result_empty}"
    print("Test Case Empty Passed\n")

    # Example 3: Single movie rating
    movie_data_single = [{'title': 'Solo Flick', 'rating': 2.5}]
    expected_output_single = {'Solo Flick': 2.5}
    print(f"Movie Data Single: {movie_data_single}")
    result_single = calculate_average_movie_ratings(movie_data_single)
    print(f"Calculated Average Ratings: {result_single}")
    print(f"Expected Output: {expected_output_single}")
    assert result_single == expected_output_single, f"Test Case Single Failed: Expected {expected_output_single}, got {result_single}"
    print("Test Case Single Passed\n")

    # Example 4: Movie with non-numeric rating (should be handled gracefully or raise error depending on spec)
    # For this implementation, we assume valid inputs as per typical problem constraints,
    # but robust code would add type checking or error handling.
    # Let's test with a mix including a potentially problematic entry that should be skipped by current logic
    movie_data_mixed = [
        {'title': 'Valid Movie', 'rating': 5.0},
        {'title': 'Another Valid', 'rating': 3.0},
        {'title': 'Valid Movie', 'rating': 4.0},
        {'title': 'Problem Movie', 'rating': 'bad_rating'}, # This should be skipped
        {'no_title_field': True, 'rating': 2.0} # This should be skipped
    ]
    expected_output_mixed = {'Valid Movie': 4.5, 'Another Valid': 3.0}
    print(f"Movie Data Mixed: {movie_data_mixed}")
    result_mixed = calculate_average_movie_ratings(movie_data_mixed)
    print(f"Calculated Average Ratings: {result_mixed}")
    print(f"Expected Output: {expected_output_mixed}")
    assert result_mixed == expected_output_mixed, f"Test Case Mixed Failed: Expected {expected_output_mixed}, got {result_mixed}"
    print("Test Case Mixed Passed\n")

    print("All q007 tests passed!") 