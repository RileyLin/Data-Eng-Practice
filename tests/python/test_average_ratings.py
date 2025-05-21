"""
Test file for the average rating per category challenge in q005_average_rating_category.py
"""

import unittest
import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

from python.q005_average_rating_category import calculate_average_ratings

class TestAverageRatings(unittest.TestCase):
    
    def test_normal_case(self):
        """Test case with multiple categories and movies."""
        movie_data = [
            {'title': 'Movie A', 'category': 'Action', 'rating': 8.5},
            {'title': 'Movie B', 'category': 'Comedy', 'rating': 7.0},
            {'title': 'Movie C', 'category': 'Action', 'rating': 9.0},
            {'title': 'Movie D', 'category': 'Drama', 'rating': 8.0},
            {'title': 'Movie E', 'category': 'Comedy', 'rating': 6.5}
        ]
        result = calculate_average_ratings(movie_data)
        self.assertAlmostEqual(result['Action'], 8.75, places=2)
        self.assertAlmostEqual(result['Comedy'], 6.75, places=2)
        self.assertAlmostEqual(result['Drama'], 8.0, places=2)
    
    def test_string_ratings(self):
        """Test case with string ratings that need conversion."""
        movie_data = [
            {'title': 'Movie F', 'category': 'Action', 'rating': '7.5'}, 
            {'title': 'Movie G', 'category': 'Comedy', 'rating': '9.0'}
        ]
        result = calculate_average_ratings(movie_data)
        self.assertAlmostEqual(result['Action'], 7.5, places=2)
        self.assertAlmostEqual(result['Comedy'], 9.0, places=2)
    
    def test_missing_values(self):
        """Test case with missing category or rating."""
        movie_data = [
            {'title': 'Movie H', 'category': 'Horror'}, # Missing rating
            {'title': 'Movie I', 'rating': 6.5}, # Missing category
            {'title': 'Movie J', 'category': 'Horror', 'rating': 7.0}
        ]
        result = calculate_average_ratings(movie_data)
        self.assertEqual(len(result), 1) # Only Horror category should be included
        self.assertAlmostEqual(result['Horror'], 7.0, places=2)
    
    def test_empty_input(self):
        """Test case with empty input."""
        result = calculate_average_ratings([])
        self.assertEqual(result, {})
    
    def test_invalid_ratings(self):
        """Test case with invalid ratings that can't be converted to float."""
        movie_data = [
            {'title': 'Movie K', 'category': 'Action', 'rating': 'excellent'},
            {'title': 'Movie L', 'category': 'Action', 'rating': 8.0}
        ]
        result = calculate_average_ratings(movie_data)
        self.assertAlmostEqual(result['Action'], 8.0, places=2)

if __name__ == '__main__':
    unittest.main() 