"""
Question: Given a list of movies and categories, calculate the average rating per category.

Implement the function `calculate_average_ratings(movie_data)` that takes a list of movie dictionaries
and returns a dictionary mapping each category to its average rating.

Each movie dictionary in the input list should have 'category' and 'rating' keys.
The function should handle edge cases:
- Skip movies without a category or rating
- Convert string ratings to float (ignore if conversion fails)
- Return an empty dictionary if the input is empty

Example Input:
movie_data = [
    {'title': 'Movie A', 'category': 'Action', 'rating': 8.5},
    {'title': 'Movie B', 'category': 'Comedy', 'rating': 7.0},
    {'title': 'Movie C', 'category': 'Action', 'rating': 9.0},
    {'title': 'Movie D', 'category': 'Drama', 'rating': 8.0},
    {'title': 'Movie E', 'category': 'Comedy', 'rating': 6.5},
    {'title': 'Movie F', 'category': 'Action', 'rating': '7.5'}, # Rating as string
    {'title': 'Movie G', 'category': 'Action'}, # Missing rating
    {'title': 'Movie H', 'rating': 5.0} # Missing category
]

Expected Output:
{
    'Action': 8.333..., # (8.5 + 9.0 + 7.5) / 3 = 8.333...
    'Comedy': 6.75,     # (7.0 + 6.5) / 2 = 6.75
    'Drama': 8.0        # 8.0 / 1 = 8.0
}
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

    category_sum={}
    category_count={}

    for movie in movie_data:

        if 'category' not in movie or 'rating' not in movie:
            continue
        
        category = movie['category']
        rating = movie['rating']
        if isinstance(rating,str):
            try:
                rating = float(rating)
            except:
                continue
        
        if category not in category_sum:
            category_sum[category] = rating
            category_count[category]=1
        else:
            category_sum[category]+=rating
            category_count[category]+=1
    
    result = {}

    for category in category_sum:

        result[category]= category_sum[category]/category_count[category]
    
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