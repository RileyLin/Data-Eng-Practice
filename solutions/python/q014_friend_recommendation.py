"""
Solution to Question 14: Friend Recommendation Algorithm (PYMK - People You May Know)

Implement a simplified Python function to generate friend recommendations based on mutual friends 
and other user attributes. This function will be a core part of the PYMK (People You May Know) system.

This solution demonstrates:
1. Proper exclusion logic for recommendations
2. Multi-factor scoring system combining mutual friends, location, activity, and privacy
3. Efficient set operations for finding mutual connections
4. Robust tie-breaking and sorting
5. Edge case handling for invalid inputs and empty results
"""

def get_user_by_id(user_id, users_data):
    """Helper to find a user dict by user_id."""
    for user in users_data:
        if user['user_id'] == user_id:
            return user
    return None


def generate_recommendations(target_user_id: int, users_data: list[dict], max_recommendations: int) -> list[int]:
    """
    Generate friend recommendations for a target user based on mutual friends and other attributes.
    
    Args:
        target_user_id: The ID of the user for whom to generate recommendations
        users_data: List of user dictionaries containing user_id, country_code, is_private, friend_ids, last_active_days_ago
        max_recommendations: Maximum number of recommendations to return
    
    Returns:
        List of user_ids for recommended friends, sorted by recommendation score (descending)
    """
    # Step 1: Find the target user
    target_user = get_user_by_id(target_user_id, users_data)
    if not target_user:
        return []

    # Step 2: Get target user's friend list and attributes
    target_friend_ids = set(target_user.get('friend_ids', []))
    target_country = target_user.get('country_code')
    
    # Step 3: Initialize recommendations dictionary to store {user_id: score}
    recommendations = {}

    # Step 4: Iterate through all users as potential candidates
    for candidate_user in users_data:
        candidate_id = candidate_user['user_id']

        # Exclusion Rule 1: Skip if candidate is the target user
        if candidate_id == target_user_id:
            continue
            
        # Exclusion Rule 2: Skip if candidate is already a friend
        if candidate_id in target_friend_ids:
            continue

        # Initialize score for this candidate
        score = 0
        
        # Scoring Factor 1: Mutual Friends (+5 points each)
        candidate_friend_ids = set(candidate_user.get('friend_ids', []))
        mutual_friends_count = len(target_friend_ids.intersection(candidate_friend_ids))
        score += mutual_friends_count * 5

        # Scoring Factor 2: Same Country (+3 points)
        if candidate_user.get('country_code') == target_country:
            score += 3

        # Scoring Factor 3: Activity Bonus (+2 points if active in last 7 days)
        if candidate_user.get('last_active_days_ago', float('inf')) <= 7:
            score += 2
        
        # Scoring Factor 4: Private Account Penalty (-10 points if private with no mutuals)
        if candidate_user.get('is_private', False) and mutual_friends_count == 0:
            score -= 10
            
        # Only consider candidates with positive scores or private users with mutual friends
        if score > 0 or (candidate_user.get('is_private', False) and mutual_friends_count > 0):
            recommendations[candidate_id] = score

    # Step 5: Sort recommendations by score (desc) and user_id (asc) for ties
    sorted_recommendations = sorted(recommendations.items(), key=lambda item: (-item[1], item[0]))
    
    # Step 6: Return top N user_ids
    return [user_id for user_id, score in sorted_recommendations[:max_recommendations]]


# Test cases
def test_generate_recommendations():
    # Test data
    test_users = [
        {'user_id': 1, 'country_code': 'US', 'is_private': False, 'friend_ids': [2, 3], 'last_active_days_ago': 0},
        {'user_id': 2, 'country_code': 'US', 'is_private': False, 'friend_ids': [1, 4], 'last_active_days_ago': 5},
        {'user_id': 3, 'country_code': 'CA', 'is_private': True,  'friend_ids': [1, 5], 'last_active_days_ago': 10},
        {'user_id': 4, 'country_code': 'US', 'is_private': False, 'friend_ids': [2], 'last_active_days_ago': 2},
        {'user_id': 5, 'country_code': 'CA', 'is_private': True,  'friend_ids': [3, 6, 7], 'last_active_days_ago': 3},
        {'user_id': 6, 'country_code': 'US', 'is_private': False, 'friend_ids': [5, 7], 'last_active_days_ago': 15},
        {'user_id': 7, 'country_code': 'GB', 'is_private': False, 'friend_ids': [5, 6], 'last_active_days_ago': 1},
        {'user_id': 8, 'country_code': 'US', 'is_private': True,  'friend_ids': [], 'last_active_days_ago': 30},
        {'user_id': 9, 'country_code': 'US', 'is_private': False, 'friend_ids': [], 'last_active_days_ago': 1},
        {'user_id': 10, 'country_code': 'CA', 'is_private': True, 'friend_ids': [2], 'last_active_days_ago': 2}
    ]
    
    # Test case 1: Basic recommendations for User 1
    # User 4: 1 mutual (2), same country (US), active → Score: 5 + 3 + 2 = 10
    # User 5: 1 mutual (3), different country (CA), active → Score: 5 + 0 + 2 = 7  
    # User 10: 1 mutual (2), different country (CA), active → Score: 5 + 0 + 2 = 7
    # Expected order: [4, 5, 10] (score DESC, user_id ASC for ties)
    result1 = generate_recommendations(target_user_id=1, users_data=test_users, max_recommendations=3)
    expected1 = [4, 5, 10]
    print(f"Test 1 - User 1 recommendations: {result1} (expected: {expected1})")
    assert result1 == expected1, f"Test 1 failed: expected {expected1}, got {result1}"
    
    # Test case 2: User with no friends (User 9)
    # Users 1, 2, 4 all score 5 (same country + active), sorted by user_id ASC: [1, 2, 4]
    result2 = generate_recommendations(target_user_id=9, users_data=test_users, max_recommendations=3)
    expected2 = [1, 2, 4]
    print(f"Test 2 - User 9 recommendations: {result2} (expected: {expected2})")
    assert result2 == expected2, f"Test 2 failed: expected {expected2}, got {result2}"
    
    # Test case 3: Limit recommendations
    result3 = generate_recommendations(target_user_id=1, users_data=test_users, max_recommendations=1)
    expected3 = [4]
    print(f"Test 3 - User 1 top 1: {result3} (expected: {expected3})")
    assert result3 == expected3, f"Test 3 failed: expected {expected3}, got {result3}"
    
    # Test case 4: Invalid user
    result4 = generate_recommendations(target_user_id=99, users_data=test_users, max_recommendations=3)
    expected4 = []
    print(f"Test 4 - Invalid user: {result4} (expected: {expected4})")
    assert result4 == expected4, f"Test 4 failed: expected {expected4}, got {result4}"
    
    # Test case 5: No possible recommendations (single user)
    single_user_data = [{'user_id': 1, 'country_code': 'US', 'is_private': False, 'friend_ids': [], 'last_active_days_ago': 0}]
    result5 = generate_recommendations(target_user_id=1, users_data=single_user_data, max_recommendations=3)
    expected5 = []
    print(f"Test 5 - No candidates: {result5} (expected: {expected5})")
    assert result5 == expected5, f"Test 5 failed: expected {expected5}, got {result5}"
    
    # Test case 6: Private user penalty test
    # User 8 should have negative score for User 9 and not be recommended
    if 8 not in generate_recommendations(target_user_id=9, users_data=test_users, max_recommendations=10):
        print("Test 6 - Private penalty: User 8 correctly excluded from User 9's recommendations")
    else:
        print("Test 6 - Private penalty: FAILED - User 8 should be excluded")
        assert False, "User 8 should be excluded due to private penalty"
    
    print("All test cases passed!")

if __name__ == "__main__":
    test_generate_recommendations()
    
    # Example Usage:
    print("\nExample Usage:")
    test_users = [
        {'user_id': 1, 'country_code': 'US', 'is_private': False, 'friend_ids': [2, 3], 'last_active_days_ago': 0},
        {'user_id': 2, 'country_code': 'US', 'is_private': False, 'friend_ids': [1, 4], 'last_active_days_ago': 5},
        {'user_id': 3, 'country_code': 'CA', 'is_private': True,  'friend_ids': [1, 5], 'last_active_days_ago': 10},
        {'user_id': 4, 'country_code': 'US', 'is_private': False, 'friend_ids': [2], 'last_active_days_ago': 2},
        {'user_id': 5, 'country_code': 'CA', 'is_private': True,  'friend_ids': [3, 6, 7], 'last_active_days_ago': 3},
        {'user_id': 9, 'country_code': 'US', 'is_private': False, 'friend_ids': [], 'last_active_days_ago': 1},
    ]
    
    recommendations = generate_recommendations(target_user_id=1, users_data=test_users, max_recommendations=3)
    print(f"Recommendations for User 1: {recommendations}")
    
    recommendations_user9 = generate_recommendations(target_user_id=9, users_data=test_users, max_recommendations=3)
    print(f"Recommendations for User 9: {recommendations_user9}") 