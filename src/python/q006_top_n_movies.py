"""
Question: Given a list of movies and their categories, find the top N movies by rating for each category.

Implement the function `get_top_n_movies_per_category(movie_data, n)` that takes:
1. A list of movie dictionaries (with 'title', 'category', and 'rating' keys)
2. An integer n specifying how many top movies to return per category

The function should return a dictionary where:
- Keys are category names
- Values are lists of (movie_title, rating) tuples, sorted by rating in descending order
- Each list contains at most the top N movies from that category

The function should handle edge cases:
- Skip movies without title, category, or rating
- Convert string ratings to float (ignore if conversion fails)
- Return an empty dictionary if input is invalid or empty
- Return at most n movies per category

Example Input:
movie_data = [
    {'title': 'Movie A', 'category': 'Action', 'rating': 8.5},
    {'title': 'Movie B', 'category': 'Comedy', 'rating': 7.0},
    {'title': 'Movie C', 'category': 'Action', 'rating': 9.0},
    {'title': 'Movie G', 'category': 'Action', 'rating': 8.8},
    {'title': 'Movie H', 'category': 'Comedy', 'rating': 9.5}
]
n = 1

Expected Output:
{
    'Action': [('Movie C', 9.0)],
    'Comedy': [('Movie H', 9.5)]
}

Example Input (same data, n=2):
Expected Output:
{
    'Action': [('Movie C', 9.0), ('Movie G', 8.8)],
    'Comedy': [('Movie H', 9.5), ('Movie B', 7.0)]
}
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
    if not movie_data or n<1:
        return {}
    
    categories = {}
    
    for movie in movie_data:

        if 'title' not in movie or 'category' not in movie or 'rating' not in movie: 
            continue



        title = movie['title']
        category = movie['category']
        rating = movie['rating']

        if isinstance(rating, str):
            try:
                rating = float(rating)
            except:
                continue

        if category not in categories:
            categories[category] = [(title,rating)]
        else: 
            categories[category].append((title,rating))
        
    
    result = {}

    for category,movie in categories.items():
        
        sorted_category = sorted(movie, key=lambda x:x[1], reverse=True)

        result[category]=sorted_category[:n]
    
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