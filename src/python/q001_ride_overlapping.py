"""
Question 1.4.1 (Overlapping User Rides):
A user wants to book multiple rides for themselves. Given a list of
requested rides, where each ride is a tuple `(start_time, end_time)`
with integer times, write a Python function
`can_user_complete_rides(requested_rides)` that returns `True` if the user
can theoretically complete all their requested rides (i.e., none of their
own rides overlap), and `False` otherwise.

DATA STRUCTURE EXAMPLES:

Input: requested_rides (List[Tuple[int, int]])
- Each tuple represents (start_time, end_time) for a single ride
- Times are integers (could represent minutes, hours, etc.)
- end_time > start_time for valid rides

Example 1 - Non-overlapping rides:
requested_rides = [(0, 30), (30, 60), (70, 90)]
Visualization:
Time:  0    30   60   70   90
       |----| |----| |----| 
       Ride1  Ride2  Ride3
Expected Output: True

Example 2 - Overlapping rides:
requested_rides = [(0, 60), (30, 90)]
Visualization:
Time:  0    30   60   90
       |---------|
            |---------|
           Ride1  Ride2 (overlap from 30-60)
Expected Output: False

Example 3 - Single ride:
requested_rides = [(10, 20)]
Expected Output: True

Example 4 - Empty list:
requested_rides = []
Expected Output: True

Example 5 - Edge case (rides touching but not overlapping):
requested_rides = [(0, 30), (30, 60)]
Visualization:
Time:  0    30   60
       |----||----| 
       Ride1 Ride2 (touching at time 30, but not overlapping)
Expected Output: True

Follow-up consideration: How would this problem change if we were considering 
a single carpool vehicle with a limited passenger capacity (e.g., 6 passengers), 
and the input was a list of ride segments for *different* users wanting to share 
that vehicle?
"""

def can_user_complete_rides(requested_rides):
    """
    Checks if a list of ride requests (start_time, end_time) for a single user overlap.
    
    Args:
        requested_rides: A list of tuples, where each tuple is (start_time, end_time).
                         Times are integers. Assumes end_time > start_time.
    
    Returns:
        True if no rides overlap, False otherwise.
    """
    
    if not requested_rides:
        return True 
    
    if len(requested_rides)<1:
        return False
    
    sorted_rides = requested_rides

    sorted_rides.sort(key = lambda x:x[1])

    previous_end_time = 0

    for ride in sorted_rides:

        if ride[0]<previous_end_time:
            return False
        
        previous_end_time = ride[1]

    return True





# Test cases
def test_can_user_complete_rides():
    assert can_user_complete_rides([(0, 30), (30, 60), (70, 90)]) == True
    assert can_user_complete_rides([(0, 60), (30, 90)]) == False
    assert can_user_complete_rides([(10, 20)]) == True
    assert can_user_complete_rides([]) == True
    print("All test cases passed!")

if __name__ == "__main__":
    test_can_user_complete_rides() 