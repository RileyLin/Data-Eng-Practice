"""
Question: Given a list of movie rating instances (each with title and rating),
calculate the average rating for each unique movie title.

Implement the function `calculate_average_movie_ratings(movie_data)` that takes a list of movie
rating instances (dictionaries) and returns a dictionary mapping each movie title to its average rating.

Each rating instance in the input list should have 'title' and 'rating' keys.
The function should handle edge cases:
- Skip instances without a title or rating
- Convert string ratings to float (ignore if conversion fails)
- Return an empty dictionary if the input is empty

Example Input:
movie_ratings_list = [
    {'title': 'Movie Alpha', 'rating': 8.0},
    {'title': 'Movie Beta', 'rating': 7.0},
    {'title': 'Movie Alpha', 'rating': 9.0},
    {'title': 'Movie Alpha', 'rating': 8.5},
    {'title': 'Movie Beta', 'rating': 7.5},
]

Expected Output:
{
    'Movie Alpha': 8.5,  # (8.0 + 9.0 + 8.5) / 3 = 8.5
    'Movie Beta': 7.25   # (7.0 + 7.5) / 2 = 7.25
}
"""

def calculate_average_movie_ratings(movie_data):
    """
    Calculates the average rating per movie title from a list of rating instances.
    
    Args:
        movie_data: A list of dictionaries, where each dict represents a rating instance
                   and should have 'title' and 'rating' keys.
                   
    Returns:
        A dictionary mapping movie title (str) to its average rating (float).
    """
    # TODO: Implement your solution here
    return {}

# Test cases
def test_calculate_average_movie_ratings():
    # Test case 1: Normal case with multiple ratings per movie
    movie_data1 = [
        {'title': 'Movie Alpha', 'rating': 8.0},
        {'title': 'Movie Beta', 'rating': 7.0},
        {'title': 'Movie Alpha', 'rating': 9.0},
        {'title': 'Movie Alpha', 'rating': 8.5},
        {'title': 'Movie Beta', 'rating': 7.5},
    ]
    result1 = calculate_average_movie_ratings(movie_data1)
    assert abs(result1['Movie Alpha'] - 8.5) < 0.001, f"Expected Movie Alpha avg ~8.5, got {result1['Movie Alpha']}"
    assert abs(result1['Movie Beta'] - 7.25) < 0.001, f"Expected Movie Beta avg ~7.25, got {result1['Movie Beta']}"
    
    # Test case 2: Handle string ratings and missing values
    movie_data2 = [
        {'title': 'Movie Gamma', 'rating': '6.5'}, # Rating as string
        {'title': 'Movie Gamma', 'rating': 7.5},
        {'title': 'Movie Delta'},                   # Missing rating
        {'rating': 9.0}                             # Missing title
    ]
    result2 = calculate_average_movie_ratings(movie_data2)
    assert 'Movie Gamma' in result2, "Movie Gamma should be included"
    assert abs(result2['Movie Gamma'] - 7.0) < 0.001, f"Expected Movie Gamma avg ~7.0, got {result2['Movie Gamma']}"
    assert 'Movie Delta' not in result2, "Movie Delta should be skipped due to missing rating"
    
    # Test case 3: Empty input
    result3 = calculate_average_movie_ratings([])
    assert result3 == {}, "Empty input should return empty dictionary"
    
    print("All test cases passed!")

if __name__ == "__main__":
    test_calculate_average_movie_ratings() 