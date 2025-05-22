"""
Solution to Question: Find the top N movies by rating for each category
"""

def get_top_n_movies_per_category(movie_data, n):
    """
    Given a list of movie dictionaries, finds the top N movies by rating for each category.
    
    Args:
        movie_data: A list of dictionaries, where each dict represents a movie
                   and has at least 'title', 'category', and 'rating' keys.
        n (int): The number of top movies to return per category.
        
    Returns:
        A dictionary where keys are category names (str) and values are lists
        of tuples, each tuple being (movie_title, rating), sorted in
        descending order of rating. Each list contains at most N movies.
    """
    # Handle invalid input
    if not movie_data or n <= 0:
        return {}
    
    # Dictionary to store movies by category
    categories = {}
    
    # Process each movie
    for movie in movie_data:
        # Skip movies without required fields
        if not all(key in movie for key in ['title', 'category', 'rating']):
            continue
        
        title = movie['title']
        category = movie['category']
        rating = movie['rating']
        
        # Try to convert rating to float if it's a string
        if isinstance(rating, str):
            try:
                rating = float(rating)
            except ValueError:
                # Skip this movie if rating can't be converted
                continue
        
        # Add movie to its category
        if category not in categories:
            categories[category] = []
        
        categories[category].append((title, rating))
    
    # Sort movies by rating and get top N for each category
    result = {}
    for category, movies in categories.items():
        # Sort movies by rating in descending order
        sorted_movies = sorted(movies, key=lambda x: x[1], reverse=True)
        # Keep only the top N movies
        result[category] = sorted_movies[:n]
    
    return result

# Test cases
def test_get_top_n_movies_per_category():
    # Test case 1: Get top 1 movie per category
    movie_data = [
        {'title': 'Movie A', 'category': 'Action', 'rating': 8.5},
        {'title': 'Movie B', 'category': 'Comedy', 'rating': 7.0},
        {'title': 'Movie C', 'category': 'Action', 'rating': 9.0},
        {'title': 'Movie G', 'category': 'Action', 'rating': 8.8},
        {'title': 'Movie H', 'category': 'Comedy', 'rating': 9.5}
    ]
    result1 = get_top_n_movies_per_category(movie_data, 1)
    
    assert 'Action' in result1, "Action category should be included"
    assert 'Comedy' in result1, "Comedy category should be included"
    assert len(result1['Action']) == 1, "Should return exactly 1 Action movie"
    assert len(result1['Comedy']) == 1, "Should return exactly 1 Comedy movie"
    assert result1['Action'][0][0] == 'Movie C', f"Top Action movie should be 'Movie C', got {result1['Action'][0][0]}"
    assert result1['Action'][0][1] == 9.0, f"Top Action movie rating should be 9.0, got {result1['Action'][0][1]}"
    assert result1['Comedy'][0][0] == 'Movie H', f"Top Comedy movie should be 'Movie H', got {result1['Comedy'][0][0]}"
    
    # Test case 2: Get top 2 movies per category
    result2 = get_top_n_movies_per_category(movie_data, 2)
    
    assert len(result2['Action']) == 2, "Should return exactly 2 Action movies"
    assert len(result2['Comedy']) == 2, "Should return exactly 2 Comedy movies"
    assert [movie[0] for movie in result2['Action']] == ['Movie C', 'Movie G'], "Action movies should be in correct order"
    assert [movie[0] for movie in result2['Comedy']] == ['Movie H', 'Movie B'], "Comedy movies should be in correct order"
    
    # Test case 3: Handle invalid input
    result3 = get_top_n_movies_per_category([], 1)
    assert result3 == {}, "Empty input should return empty dictionary"
    
    result4 = get_top_n_movies_per_category(movie_data, 0)
    assert result4 == {}, "n=0 should return empty dictionary"
    
    # Test case 4: Handle invalid movie data
    invalid_movie_data = [
        {'title': 'Movie I', 'rating': 8.0},  # Missing category
        {'category': 'Drama', 'rating': 7.5}, # Missing title
        {'title': 'Movie J', 'category': 'Drama'} # Missing rating
    ]
    result5 = get_top_n_movies_per_category(invalid_movie_data, 1)
    assert 'Drama' not in result5, "Invalid movies should be skipped"
    
    print("All test cases passed!")

if __name__ == "__main__":
    test_get_top_n_movies_per_category() 