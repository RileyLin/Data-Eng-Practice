"""
Solution to Average Rating by Category

DATA STRUCTURE EXAMPLES:

Input: movie_data (List[Dict])
- Structure: [{'title': str, 'category': str, 'rating': float|str}, ...]
- Each movie dictionary should have 'category' and 'rating' keys
- 'rating' can be float or string (will be converted to float)
- Other keys like 'title' are optional and ignored

Example movie dictionaries:
- Complete movie: {'title': 'Movie A', 'category': 'Action', 'rating': 8.5}
- String rating: {'title': 'Movie B', 'category': 'Comedy', 'rating': '7.0'}
- Missing rating: {'title': 'Movie C', 'category': 'Action'} # Will be skipped
- Missing category: {'title': 'Movie D', 'rating': 5.0} # Will be skipped
- Invalid rating: {'title': 'Movie E', 'category': 'Drama', 'rating': 'invalid'} # Will be skipped

Output: Dict[str, float]
- Structure: {category_name: average_rating}
- category_name: string representing the movie category
- average_rating: float representing the average rating for that category

Example Input:
movie_data = [
    {'title': 'Movie A', 'category': 'Action', 'rating': 8.5},
    {'title': 'Movie B', 'category': 'Comedy', 'rating': 7.0},
    {'title': 'Movie C', 'category': 'Action', 'rating': 9.0},
    {'title': 'Movie D', 'category': 'Drama', 'rating': 8.0},
    {'title': 'Movie E', 'category': 'Comedy', 'rating': 6.5},
    {'title': 'Movie F', 'category': 'Action', 'rating': '7.5'}, # Rating as string
    {'title': 'Movie G', 'category': 'Action'}, # Missing rating - SKIPPED
    {'title': 'Movie H', 'rating': 5.0} # Missing category - SKIPPED
]

Processing breakdown:
Action movies: [8.5, 9.0, 7.5] → Average: (8.5 + 9.0 + 7.5) / 3 = 8.333...
Comedy movies: [7.0, 6.5] → Average: (7.0 + 6.5) / 2 = 6.75
Drama movies: [8.0] → Average: 8.0 / 1 = 8.0

Expected Output:
{
    'Action': 8.333..., # (8.5 + 9.0 + 7.5) / 3 = 8.333...
    'Comedy': 6.75,     # (7.0 + 6.5) / 2 = 6.75
    'Drama': 8.0        # 8.0 / 1 = 8.0
}

Edge Cases:
- Empty input: [] → {}
- All movies missing required fields: [{'title': 'Movie'}] → {}
- Single category: [{'category': 'Action', 'rating': 5.0}] → {'Action': 5.0}
- Duplicate categories: Multiple movies with same category are averaged together
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
    
    category_totals = {}
    category_counts = {}
    
    for movie in movie_data:
        # Skip movies without required fields
        if 'category' not in movie or 'rating' not in movie:
            continue
            
        category = movie['category']
        rating = movie['rating']
        
        # Convert string ratings to float, skip if conversion fails
        if isinstance(rating, str):
            try:
                rating = float(rating)
            except ValueError:
                continue
        
        # Accumulate totals and counts
        if category not in category_totals:
            category_totals[category] = rating
            category_counts[category] = 1
        else:
            category_totals[category] += rating
            category_counts[category] += 1
    
    # Calculate averages
    result = {}
    for category in category_totals:
        result[category] = category_totals[category] / category_counts[category]
    
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
    assert abs(result1['Action'] - 8.75) < 0.001
    assert abs(result1['Comedy'] - 6.75) < 0.001
    assert abs(result1['Drama'] - 8.0) < 0.001
    
    # Test case 2: Handle string ratings and missing values
    movie_data2 = [
        {'title': 'Movie F', 'category': 'Action', 'rating': '7.5'},
        {'title': 'Movie G', 'category': 'Action'},
        {'title': 'Movie H', 'rating': 5.0}
    ]
    result2 = calculate_average_ratings(movie_data2)
    assert 'Action' in result2
    assert abs(result2['Action'] - 7.5) < 0.001
    
    # Test case 3: Empty input
    result3 = calculate_average_ratings([])
    assert result3 == {}
    
    print("All test cases passed!")

if __name__ == "__main__":
    test_calculate_average_ratings() 