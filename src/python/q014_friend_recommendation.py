"""
Question 14: Friend Recommendation Algorithm (Simplified - Friends of Friends)

This version implements a friend recommendation algorithm primarily based on 
the "friends of friends" concept. It counts how many mutual friends connect 
the target user to a potential recommendation (a friend of a friend).

If no such friends-of-friends are found, it falls back to recommending any
users who are not already friends with the target user.

The primary sorting criterion is the count of these mutual connections,
then by user ID for tie-breaking.
"""

def build_graph(users_data: list[dict]) -> dict[int, set[int]]:
    """
    Transforms the list of user dictionaries into an adjacency list representation (graph).
    Each user_id maps to a set of their friend_ids for efficient lookups.
    
    Args:
        users_data: List of user dictionaries. Each dict must have 'user_id' 
                    and 'friend_ids' (list of ints).
        Example: [
            {'user_id': 1, 'friend_ids': [2, 3]},
            {'user_id': 2, 'friend_ids': [1]}
        ]
    
    Returns:
        A dictionary where keys are user_ids and values are sets of their friend_ids.
        Example: {1: {2, 3}, 2: {1}}
    """
    graph = {} # Initialize an empty dictionary to store the graph
    for user_dict in users_data: # Iterate through each user's data dictionary
        user_id = user_dict.get('user_id') # Get the user's ID
        # Get the list of friend IDs, defaulting to an empty list if 'friend_ids' is missing
        friend_ids = user_dict.get('friend_ids', []) 
        if user_id is not None: # Ensure user_id is present
            # Store the friends as a set for efficient operations (e.g., checking membership)
            graph[user_id] = set(friend_ids) 
    return graph # Return the constructed graph

def recommend_friends(user_id: int, k: int, graph: dict[int, set[int]]) -> list[int]:
    """
    Recommends friends for a given user based on friends-of-friends.

    Args:
        user_id: The ID of the user for whom to generate recommendations. (e.g., 1)
        k: The maximum number of recommendations to return. (e.g., 3)
        graph: A dictionary representing the social network.
               Example: {1: {2, 3}, 2: {1, 4}, 3: {1, 5}, 4: {2}, 5: {3}}

    Returns:
        A list of recommended user_ids, sorted by the number of mutual 
        connections (descending) and then by user_id (ascending).
        Example output for user_id=1, k=2 with above graph: [4, 5]
    """
    # Check if the target user_id exists in the graph. If not, no recommendations can be made.
    # Example: if user_id = 99 and 99 is not in graph keys, return [].
    if user_id not in graph:
        return []

    # Get the set of direct friends for the target user.
    # Defaults to an empty set if user_id is in graph but has no listed friends (e.g., graph[user_id] was an empty set).
    # Example: if user_id=1, graph[1]={2,3}, then direct_friends = {2, 3}.
    direct_friends = graph.get(user_id, set())
    
    # Initialize a dictionary to store potential candidates and their mutual connection counts.
    # Key: candidate_user_id, Value: count of paths through direct friends.
    # Example: {4: 1, 5: 2} means user 4 is a FoF via 1 path, user 5 via 2 paths.
    mutual_count = {}  

    # Iterate over each direct friend of the target user.
    # Example: For user_id=1, first iteration friend=2, second iteration friend=3.
    for friend in direct_friends:
        # For each direct friend, iterate over *their* friends (these are friends-of-friends, FoFs).
        # graph.get(friend, set()) handles cases where a friend_id might be in a friend list 
        # but not have their own entry as a key in the graph (a dangling edge).
        # Example: If friend=2, graph.get(2, set()) might be {1, 4}. So, fof will be 1, then 4.
        for fof in graph.get(friend, set()): 
            # Exclude the target user themselves from recommendations.
            # Example: If fof=1 (target_user_id), skip.
            if fof == user_id:
                continue
            # Exclude users who are already direct friends of the target user.
            # Example: If user_id=1, direct_friends={2,3}. If fof=2, skip.
            if fof in direct_friends:
                continue
            
            # If `fof` is a valid candidate (not self, not a direct friend), increment their mutual connection count.
            # .get(fof, 0) retrieves current count or 0 if fof not yet in mutual_count.
            # Example: If fof=4 and was not seen, mutual_count becomes {4: 1}.
            #          If fof=4 was seen via another path, its count increments e.g. from 1 to 2.
            mutual_count[fof] = mutual_count.get(fof, 0) + 1

    # Fallback logic: If no friends-of-friends were found (mutual_count is empty)
    # AND the user requested at least one recommendation (k > 0).
    if not mutual_count and k > 0:
        # Iterate through all users in the graph as potential fallback candidates.
        for person in graph: 
            # Must not be the target user themselves.
            if person == user_id:
                continue
            # Must not be an existing direct friend.
            if person not in direct_friends:
                # Add this person to mutual_count with a count of 0.
                # setdefault is used here to ensure that if, hypothetically, `person` was already added
                # (which shouldn't happen if mutual_count is truly empty), it wouldn't overwrite a non-zero count.
                # Example: If graph has user 6, and 6 is not user_id and not in direct_friends, 
                #          mutual_count.setdefault(6,0) makes mutual_count {..., 6:0, ...}.
                mutual_count.setdefault(person, 0) 

    # Sort the candidates.
    # mutual_count.items() gives a list of (user_id, count) tuples. e.g., [(4,1), (5,1)]
    sorted_candidates = sorted(
        mutual_count.items(),
        # Sort key: a tuple. Python sorts by the first element, then second for ties.
        # -item[1]: Sorts by count (item[1]) in descending order (due to negative sign).
        # item[0]: Sorts by user_id (item[0]) in ascending order for tie-breaking if counts are equal.
        # Example: [(4,2), (5,1), (7,2)] -> sort by (-count) -> [(4,2), (7,2), (5,1)]
        #          then for (4,2) and (7,2) which have same count, sort by user_id -> (4,2) before (7,2) -> [(4,2), (7,2), (5,1)]
        key=lambda item: (-item[1], item[0]) 
    )

    # Extract just the user_ids from the sorted list of (user_id, count) tuples.
    # And slice the list to get at most `k` recommendations.
    # Example: if sorted_candidates=[(4,2), (7,2), (5,1)] and k=2, result is [4, 7].
    return [uid for uid, _count in sorted_candidates[:k]]


# Test cases
def test_recommend_friends():
    test_users_data = [
        {'user_id': 1, 'country_code': 'US', 'is_private': False, 'friend_ids': [2, 3], 'last_active_days_ago': 0},
        {'user_id': 2, 'country_code': 'US', 'is_private': False, 'friend_ids': [1, 4], 'last_active_days_ago': 5},
        {'user_id': 3, 'country_code': 'CA', 'is_private': True,  'friend_ids': [1, 5], 'last_active_days_ago': 10},
        {'user_id': 4, 'country_code': 'US', 'is_private': False, 'friend_ids': [2], 'last_active_days_ago': 2},
        {'user_id': 5, 'country_code': 'CA', 'is_private': True,  'friend_ids': [3, 6, 7], 'last_active_days_ago': 3},
        {'user_id': 6, 'country_code': 'US', 'is_private': False, 'friend_ids': [5, 7], 'last_active_days_ago': 15},
        {'user_id': 7, 'country_code': 'GB', 'is_private': False, 'friend_ids': [5, 6], 'last_active_days_ago': 1},
        {'user_id': 8, 'country_code': 'US', 'is_private': True,  'friend_ids': [], 'last_active_days_ago': 30}, # No friends
        {'user_id': 9, 'country_code': 'US', 'is_private': False, 'friend_ids': [10], 'last_active_days_ago': 1}, # Friend 10 (user 10 data below)
        {'user_id': 10, 'country_code': 'CA', 'is_private': True, 'friend_ids': [2], 'last_active_days_ago': 2} # User 10, friend of 2
    ]
    
    graph = build_graph(test_users_data)

    # Test case 1: Basic recommendations for User 1
    # User 1 friends: {2, 3}
    # FoFs via friend 2 (friends {1,4}): Candidate 4 (count becomes 1 in mutual_count[4])
    # FoFs via friend 3 (friends {1,5}): Candidate 5 (count becomes 1 in mutual_count[5])
    # mutual_count = {4:1, 5:1}
    # Sorted by (-count, id): [(4,1), (5,1)] -> [4, 5]
    result1 = recommend_friends(user_id=1, k=3, graph=graph)
    expected1 = [4, 5] 
    print(f"Test 1 - User 1 recommendations: {result1} (expected: {expected1})")
    assert result1 == expected1, f"Test 1 Failed: Expected {expected1}, got {result1}"

    # Test case 2: User with no FoF recommendations, but has direct friends (User 4)
    # User 4 friends: {2}
    # FoFs via friend 2 (friends {1,4}): Candidate 1 is friend of 2, BUT 1 is user_id (target) if we were recommending for 2, not a FoF for 4 in this pass.
    # Friend 2 of user 4: friends {1,4}. fof=1 is not 4, fof=1 is not in direct_friends({2}) for user 4. So {1:1} ?
    # Let's trace: user_id=4, direct_friends={2}. friend=2. graph.get(2)={1,4}.
    # fof=1: 1!=4 (target). 1 not in {2} (direct_friends). mutual_count[1]=1.
    # fof=4: 4==4 (target). skip.
    # So mutual_count = {1:1}.
    # Fallback is NOT triggered.
    result2 = recommend_friends(user_id=4, k=3, graph=graph)
    expected2 = [1] # User 1 is FoF for User 4 via User 2.
    print(f"Test 2 - User 4 recommendations: {result2} (expected: {expected2})")
    assert result2 == expected2, f"Test 2 Failed: Expected {expected2}, got {result2}"

    # Test case 3: Limit recommendations (k=1 for User 1)
    # From result1 logic, mutual_count = {4:1, 5:1}. Sorted [4,5]. Sliced to k=1 -> [4]
    result3 = recommend_friends(user_id=1, k=1, graph=graph)
    expected3 = [4] 
    print(f"Test 3 - User 1 top 1: {result3} (expected: {expected3})")
    assert result3 == expected3, f"Test 3 Failed: Expected {expected3}, got {result3}"

    # Test case 4: Invalid user_id (not in graph)
    result4 = recommend_friends(user_id=99, k=3, graph=graph)
    expected4 = []
    print(f"Test 4 - Invalid user: {result4} (expected: {expected4})")
    assert result4 == expected4, f"Test 4 Failed: Expected {expected4}, got {result4}"

    # Test case 5: User with no friends (User 8)
    # User 8 direct_friends = {}. Loop for FoFs doesn't run. mutual_count = {}.
    # Fallback IS triggered.
    # Non-friends of 8: all other users [1,2,3,4,5,6,7,9,10]. All get count 0.
    # Sorted by (-0, id) -> [1,2,3,4,5,6,7,9,10]. Sliced to k=3 -> [1,2,3]
    result5 = recommend_friends(user_id=8, k=3, graph=graph)
    expected5 = [1, 2, 3]
    print(f"Test 5 - User 8 (no friends, fallback): {result5} (expected: {expected5})")
    assert result5 == expected5, f"Test 5 Failed: Expected {expected5}, got {result5}"

    # Test case 6: Tie-breaking (multiple FoFs with same count)
    tie_graph = {
        1: {2, 3},      # Target user 1
        2: {1, 4, 5},   # Friend 2 of 1. FoFs via 2 are 4, 5.
        3: {1, 6, 7},   # Friend 3 of 1. FoFs via 3 are 6, 7.
        4: {2}, 5: {2}, 6: {3}, 7: {3} # Other users to complete graph
    }
    # For user_id=1, k=3, graph=tie_graph:
    # Direct friends of 1: {2,3}
    # Via friend 2 (friends {1,4,5}): fof=4 (valid), fof=5 (valid). mutual_count = {4:1, 5:1}
    # Via friend 3 (friends {1,6,7}): fof=6 (valid), fof=7 (valid). mutual_count = {4:1, 5:1, 6:1, 7:1}
    # All have count 1. Sorted by (-1, id): [4,5,6,7]. Sliced to k=3 -> [4,5,6]
    result6 = recommend_friends(user_id=1, k=3, graph=tie_graph)
    expected6 = [4, 5, 6]
    print(f"Test 6 - Tie-breaking (all count 1): {result6} (expected: {expected6})")
    assert result6 == expected6, f"Test 6 Failed: Expected {expected6}, got {result6}"

    # Test case 7: k=0, should return empty list
    result7 = recommend_friends(user_id=1, k=0, graph=graph)
    expected7 = []
    print(f"Test 7 - k=0: {result7} (expected: {expected7})")
    assert result7 == expected7, f"Test 7 Failed: Expected {expected7}, got {result7}"

    # Test case 8: User whose friends might not be fully represented in graph keys (dangling edge handled by graph.get(friend, set()))
    # User 9 friends: {10}. graph[9]={10}.
    # Friend is 10. graph.get(10) = {2} (from user 10 data)
    # FoF is 2. (2 is not 9, 2 is not in direct_friends of 9 which is {10}).
    # mutual_count = {2:1}.
    result8 = recommend_friends(user_id=9, k=3, graph=graph)
    expected8 = [2]
    print(f"Test 8 - User 9 (friend 10 exists, FoF is 2): {result8} (expected: {expected8})")
    assert result8 == expected8, f"Test 8 Failed: Expected {expected8}, got {result8}"
    
    # Test case 9: A user who is a FoF through multiple paths from target_user
    graph_multi_path = {
        1: {2, 3},    # Target user 1
        2: {1, 4},    # Friend 2 of 1. FoF via 2 is 4.
        3: {1, 4},    # Friend 3 of 1. FoF via 3 is 4.
        4: {2, 3}     # Candidate 4, friends with both 2 and 3.
    }
    # For user_id=1, k=1, graph_multi_path:
    # Direct friends {2,3}
    # Via friend 2 (friends {1,4}): fof=4. mutual_count={4:1}
    # Via friend 3 (friends {1,4}): fof=4. mutual_count={4:2} (incremented)
    # Sorted: [(4,2)]. Sliced to k=1 -> [4]
    result9 = recommend_friends(user_id=1, k=1, graph=graph_multi_path)
    expected9 = [4]
    print(f"Test 9 - User 4 recommended to User 1 (FoF via 2 paths, count=2): {result9} (expected: {expected9})")
    assert result9 == expected9, f"Test 9 Failed: Expected {expected9}, got {result9}"


    print("\nAll revised test cases passed!")

if __name__ == "__main__":
    test_recommend_friends() 