"""
Problem 4: Python Processing - Friend Recommendation Algorithm
Time Limit: 8 minutes

Scenario:
Implement a simplified Python function to generate friend recommendations based on mutual friends 
and other user attributes. This function will be a core part of the PYMK (People You May Know) system.

Requirements:
- Input: 
    - target_user_id: The ID of the user for whom to generate recommendations.
    - users_data: A list of dictionaries, where each dictionary represents a user and contains:
        - user_id (int)
        - country_code (str, e.g., "US", "IN")
        - is_private (bool)
        - friend_ids (list of int, current friends of this user)
        - last_active_days_ago (int, 0 for active today, 1 for yesterday, etc.)
    - max_recommendations (int): Maximum number of recommendations to return.
- Output: 
    - A list of user_ids for the recommended friends, sorted by a recommendation score (descending).
- Recommendation Logic:
    1. Exclude:
        - The target_user_id itself.
        - Existing friends of target_user_id.
        - Users who are already being followed by target_user_id (for simplicity here, use friend_ids to cover both friends and unidirectional follows for now).
    2. Scoring (Example - feel free to enhance):
        - Mutual Friends: +5 points for each mutual friend.
        - Same Country: +3 points if the candidate user is from the same country as the target_user_id.
        - Activity Bonus: +2 points if the candidate user was active in the last 7 days (last_active_days_ago <= 7).
        - Penalty for Private & No Mutuals: -10 points if a candidate is private AND has 0 mutual friends (to deprioritize suggesting private users with no clear connection).
    3. Selection: Return the top max_recommendations users based on their scores.

Your Task:
Part A: Implement the generate_recommendations function (6 minutes)
Write the Python function according to the specifications. Pay attention to clarity and efficiency.

Part B: Testing Considerations (2 minutes)
Briefly describe 2-3 test cases you would create to ensure your generate_recommendations function works correctly. Consider edge cases.

Follow-up Questions:
Be prepared to discuss:
- Scalability: How would this approach perform with millions of users? What are the bottlenecks?
- Alternative Data Structures: Could you use graphs or other data structures to optimize finding mutual friends or candidates?
- More Complex Scoring: How would you incorporate other signals like shared interests, group memberships, or location proximity?
- Cold Start Problem: How would you generate recommendations for new users with no friends or activity?
- Diversity and Serendipity: How can you ensure recommendations are not just an echo chamber and help users discover new connections?
- Real-time Updates: If friend relationships change frequently, how would you keep recommendations fresh?

Success Criteria:
- Correctly implemented logic for exclusions, scoring, and selection.
- Clear and readable Python code with good variable names.
- Thoughtful test cases that cover primary logic and edge conditions.
- Ability to discuss scalability and potential improvements.

Meta Context:
- PYMK is a computationally intensive feature at Meta scale.
- The core logic often involves graph traversal and feature engineering.
- A/B testing different recommendation algorithms is common practice.
"""


def get_user_by_id(user_id, users_data):
    """Helper to find a user dict by user_id."""
    # TODO: Implement this helper function
    pass


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
    # TODO: Implement the recommendation algorithm
    
    # Step 1: Find the target user
    # TODO: Use get_user_by_id helper function
    
    # Step 2: Get target user's friend list
    # TODO: Extract friend_ids from target user, handle missing field
    
    # Step 3: Initialize recommendations dictionary to store {user_id: score}
    # TODO: Create empty dictionary for recommendations
    
    # Step 4: Iterate through all users as potential candidates
    # TODO: Loop through users_data
    
        # TODO: Implement exclusion rules
        # - Skip if candidate is the target user
        # - Skip if candidate is already a friend
        
        # TODO: Implement scoring system
        # - Calculate mutual friends (+5 each)
        # - Add same country bonus (+3)
        # - Add activity bonus (+2 if active in last 7 days)
        # - Apply private account penalty (-10 if private AND no mutuals)
        
        # TODO: Only add candidates with positive scores or private users with mutual friends
    
    # Step 5: Sort recommendations by score (desc) and user_id (asc) for ties
    # TODO: Use sorted() with custom key function
    
    # Step 6: Return top N user_ids
    # TODO: Extract user_ids and slice to max_recommendations
    
    return []  # Replace with your implementation


# Test Framework (You don't need to write this part in the interview, but be ready to discuss)

TEST_USERS_DATA = [
    {'user_id': 1, 'country_code': 'US', 'is_private': False, 'friend_ids': [2, 3], 'last_active_days_ago': 0},
    {'user_id': 2, 'country_code': 'US', 'is_private': False, 'friend_ids': [1, 4], 'last_active_days_ago': 5},
    {'user_id': 3, 'country_code': 'CA', 'is_private': True,  'friend_ids': [1, 5], 'last_active_days_ago': 10},
    {'user_id': 4, 'country_code': 'US', 'is_private': False, 'friend_ids': [2], 'last_active_days_ago': 2},
    {'user_id': 5, 'country_code': 'CA', 'is_private': True,  'friend_ids': [3, 6, 7], 'last_active_days_ago': 3},
    {'user_id': 6, 'country_code': 'US', 'is_private': False, 'friend_ids': [5, 7], 'last_active_days_ago': 15},
    {'user_id': 7, 'country_code': 'GB', 'is_private': False, 'friend_ids': [5, 6], 'last_active_days_ago': 1},
    {'user_id': 8, 'country_code': 'US', 'is_private': True,  'friend_ids': [], 'last_active_days_ago': 30},  # Private, no friends
    {'user_id': 9, 'country_code': 'US', 'is_private': False, 'friend_ids': [], 'last_active_days_ago': 1},   # Public, no friends, active US
    {'user_id': 10, 'country_code': 'CA', 'is_private': True, 'friend_ids': [2], 'last_active_days_ago': 2}   # Private, 1 mutual with user 1 (via user 2), active CA
]


def run_tests():
    """Run test cases for the generate_recommendations function."""
    print("Running tests for generate_recommendations...")
    
    # TODO: Implement your test cases here
    # Consider these test scenarios:
    
    # Test Case 1: Basic recommendations for User 1
    # Expected: User 4 (score 10), User 5 (score 7), User 10 (score 7)
    # Order: [4, 5, 10] (score DESC, user_id ASC for ties)
    
    # Test Case 2: User with no friends (User 9)
    # Expected: Users with same country + active bonus
    
    # Test Case 3: Max recommendations limits output
    # Test with max_recommendations=1
    
    # Test Case 4: Target user not found
    # Test with invalid user_id
    
    # Test Case 5: No possible recommendations
    # Test with single user dataset
    
    # Test Case 6: Private user penalty
    # Verify that private users with no mutuals are penalized
    
    print("TODO: Implement test cases")


if __name__ == '__main__':
    run_tests()
    
    # Example Usage (uncomment when you implement the function):
    # print("\nExample Usage:")
    # recommendations = generate_recommendations(target_user_id=1, users_data=TEST_USERS_DATA, max_recommendations=3)
    # print(f"Recommendations for User 1: {recommendations}")
    
    # recommendations_user9 = generate_recommendations(target_user_id=9, users_data=TEST_USERS_DATA, max_recommendations=3)
    # print(f"Recommendations for User 9: {recommendations_user9}") 