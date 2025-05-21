"""
Test file for the ride overlapping challenge in q001_ride_overlapping.py
"""

import unittest
import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

from python.q001_ride_overlapping import can_user_complete_rides

class TestRideOverlapping(unittest.TestCase):
    
    def test_non_overlapping_rides(self):
        """Test case for non-overlapping rides."""
        requested_rides = [(0, 30), (30, 60), (70, 90)]
        self.assertTrue(can_user_complete_rides(requested_rides), 
                        "Expected True for non-overlapping rides")
    
    def test_overlapping_rides(self):
        """Test case for overlapping rides."""
        requested_rides = [(0, 60), (30, 90)]
        self.assertFalse(can_user_complete_rides(requested_rides), 
                         "Expected False for overlapping rides")
    
    def test_single_ride(self):
        """Test case for a single ride."""
        requested_rides = [(10, 20)]
        self.assertTrue(can_user_complete_rides(requested_rides), 
                        "Expected True for a single ride")
    
    def test_empty_list(self):
        """Test case for an empty list of rides."""
        requested_rides = []
        self.assertTrue(can_user_complete_rides(requested_rides), 
                        "Expected True for an empty list of rides")
    
    def test_exact_boundaries(self):
        """Test case for rides with exact boundaries (end time of one = start time of next)."""
        requested_rides = [(0, 10), (10, 20), (20, 30)]
        self.assertTrue(can_user_complete_rides(requested_rides), 
                        "Expected True for rides with exact boundaries")
    
    def test_multiple_overlaps(self):
        """Test case for multiple overlapping rides."""
        requested_rides = [(0, 30), (10, 40), (20, 50)]
        self.assertFalse(can_user_complete_rides(requested_rides),
                         "Expected False for multiple overlapping rides")
    
    def test_nested_rides(self):
        """Test case for nested rides (one ride completely inside another)."""
        requested_rides = [(0, 100), (25, 75)]
        self.assertFalse(can_user_complete_rides(requested_rides),
                         "Expected False for nested rides")
    
    def test_unsorted_rides(self):
        """Test case for unsorted list of rides."""
        requested_rides = [(70, 90), (0, 30), (30, 60)]
        self.assertTrue(can_user_complete_rides(requested_rides),
                        "Expected True for unsorted, non-overlapping rides")

if __name__ == '__main__':
    unittest.main() 