"""
Solution to Question: Calculate the average rating per category
"""

def calculate_average_ratings(movie_data):
    """
    Calculates the average rating per category from a list of movie dictionaries.
    
    Args:
        movie_data: A list of dictionaries, where each dict represents a movie
                   and should have 'category' and 'rating' keys.
                  
    Returns:
        A dictionary mapping category (str) to average rating (float).
    """
    if not movie_data:
        return {}
        
    # Initialize dictionaries to track sum and count for each category
    category_sum = {}
    category_count = {}
    
    for movie in movie_data:
        # Skip movies without both category and rating
        if 'category' not in movie or 'rating' not in movie:
            continue
            
        category = movie['category']
        rating = movie['rating']
        
        # Try to convert rating to float if it's a string
        if isinstance(rating, str):
            try:
                rating = float(rating)
            except ValueError:
                # Skip this movie if rating can't be converted
                continue
        
        # Initialize category if not seen before
        if category not in category_sum:
            category_sum[category] = 0
            category_count[category] = 0
        
        # Add to running sum and count
        category_sum[category] += rating
        category_count[category] += 1
    
    # Calculate average for each category
    result = {}
    for category in category_sum:
        if category_count[category] > 0:  # Avoid division by zero
            result[category] = category_sum[category] / category_count[category]
    
    return result

# Test cases
def test_calculate_average_ratings():
    # Test case 1: Normal case with multiple categories and movies
    movie_data1 = [
        {'title': 'Movie A', 'category': 'Action', 'rating': 8.5},
        {'title': 'Movie B', 'category': 'Comedy', 'rating': 7.0},
        {'title': 'Movie C', 'category': 'Action', 'rating': 9.0},
        {'title': 'Movie D', 'category': 'Drama', 'rating': 8.0},
        {'title': 'Movie E', 'category': 'Comedy', 'rating': 6.5}
    ]
    result1 = calculate_average_ratings(movie_data1)
    assert abs(result1['Action'] - 8.75) < 0.001, f"Expected Action avg ~8.75, got {result1['Action']}"
    assert abs(result1['Comedy'] - 6.75) < 0.001, f"Expected Comedy avg ~6.75, got {result1['Comedy']}"
    assert abs(result1['Drama'] - 8.0) < 0.001, f"Expected Drama avg ~8.0, got {result1['Drama']}"
    
    # Test case 2: Handle string ratings and missing values
    movie_data2 = [
        {'title': 'Movie F', 'category': 'Action', 'rating': '7.5'}, # Rating as string
        {'title': 'Movie G', 'category': 'Action'}, # Missing rating
        {'title': 'Movie H', 'rating': 5.0} # Missing category
    ]
    result2 = calculate_average_ratings(movie_data2)
    assert 'Action' in result2, "Action category should be included"
    assert abs(result2['Action'] - 7.5) < 0.001, f"Expected Action avg ~7.5, got {result2['Action']}"
    
    # Test case 3: Empty input
    result3 = calculate_average_ratings([])
    assert result3 == {}, "Empty input should return empty dictionary"
    
    print("All test cases passed!")

if __name__ == "__main__":
    test_calculate_average_ratings() 