# Scenario 10: PYMK (People You May Know) - Python Questions

## Question 1: Friend Recommendation Algorithm

**Problem**: Implement a friend recommendation system that suggests users based on mutual friends, geographic proximity, and user activity patterns.

### Solution:
```python
def generate_recommendations(target_user_id: int, users_data: list[dict], max_recommendations: int) -> list[int]:
    """
    Generate friend recommendations based on multiple signals.
    
    Scoring System:
    - Mutual Friends: +5 points per mutual friend
    - Same Country: +3 points 
    - Activity Bonus: +2 points if active in last 7 days
    - Private Account Penalty: -10 points if private with 0 mutual friends
    
    Args:
        target_user_id: User to generate recommendations for
        users_data: List of user dictionaries with user_id, country_code, is_private, friend_ids, last_active_days_ago
        max_recommendations: Maximum number of recommendations to return
        
    Returns:
        List of user_ids sorted by recommendation score (descending)
    """
    # Find target user
    target_user = None
    for user in users_data:
        if user['user_id'] == target_user_id:
            target_user = user
            break
    
    if not target_user:
        return []
    
    target_friend_ids = set(target_user.get('friend_ids', []))
    target_country = target_user.get('country_code', '')
    
    recommendations = {}
    
    for candidate_user in users_data:
        candidate_id = candidate_user['user_id']
        
        # Skip target user and existing friends
        if candidate_id == target_user_id or candidate_id in target_friend_ids:
            continue
        
        score = 0
        
        # Calculate mutual friends
        candidate_friends = set(candidate_user.get('friend_ids', []))
        mutual_friends_count = len(target_friend_ids.intersection(candidate_friends))
        score += mutual_friends_count * 5
        
        # Same country bonus
        if candidate_user.get('country_code', '') == target_country:
            score += 3
        
        # Activity bonus
        if candidate_user.get('last_active_days_ago', 999) <= 7:
            score += 2
        
        # Private account penalty
        if candidate_user.get('is_private', False) and mutual_friends_count == 0:
            score -= 10
        
        # Only include positive scores or private users with mutual friends
        if score > 0 or (candidate_user.get('is_private', False) and mutual_friends_count > 0):
            recommendations[candidate_id] = score
    
    # Sort by score (desc) then user_id (asc) for ties
    sorted_recommendations = sorted(
        recommendations.items(), 
        key=lambda x: (-x[1], x[0])
    )
    
    # Return top N user_ids
    return [user_id for user_id, _ in sorted_recommendations[:max_recommendations]]

# Test cases
def test_generate_recommendations():
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
    
    result = generate_recommendations(1, test_users, 3)
    expected = [4, 5, 10]  # User 4 (score 10), User 5 & 10 (score 7 each)
    assert result == expected, f"Expected {expected}, got {result}"
    print("Friend recommendation test passed!")

if __name__ == "__main__":
    test_generate_recommendations()
```

## Question 2: Social Graph Analysis

**Problem**: Analyze a social network to identify influencers, community clusters, and connection patterns.

### Solution:
```python
from collections import defaultdict, deque

class SocialGraphAnalyzer:
    """Analyze social network structure and patterns"""
    
    def __init__(self, users_data):
        self.users_data = {user['user_id']: user for user in users_data}
        self.graph = self._build_graph()
    
    def _build_graph(self):
        """Build adjacency list representation of social graph"""
        graph = defaultdict(set)
        
        for user_id, user in self.users_data.items():
            friends = user.get('friend_ids', [])
            for friend_id in friends:
                if friend_id in self.users_data:  # Only include existing users
                    graph[user_id].add(friend_id)
                    graph[friend_id].add(user_id)  # Undirected graph
        
        return graph
    
    def find_influencers(self, top_n=5):
        """Find most influential users based on centrality metrics"""
        influence_scores = {}
        
        for user_id in self.users_data:
            # Calculate multiple centrality measures
            degree_centrality = len(self.graph[user_id])
            betweenness_centrality = self._calculate_betweenness_centrality(user_id)
            
            # Combined influence score
            influence_scores[user_id] = {
                'degree_centrality': degree_centrality,
                'betweenness_centrality': betweenness_centrality,
                'influence_score': degree_centrality * 0.7 + betweenness_centrality * 0.3
            }
        
        # Sort by influence score
        sorted_influencers = sorted(
            influence_scores.items(),
            key=lambda x: x[1]['influence_score'],
            reverse=True
        )
        
        return sorted_influencers[:top_n]
    
    def _calculate_betweenness_centrality(self, target_user):
        """Calculate betweenness centrality for a user (simplified)"""
        betweenness = 0
        
        # For each pair of other users, check if target_user is on shortest path
        for source in self.users_data:
            if source == target_user:
                continue
                
            for destination in self.users_data:
                if destination == target_user or destination == source:
                    continue
                
                shortest_paths = self._find_all_shortest_paths(source, destination)
                paths_through_target = sum(
                    1 for path in shortest_paths if target_user in path
                )
                
                if len(shortest_paths) > 0:
                    betweenness += paths_through_target / len(shortest_paths)
        
        return betweenness
    
    def _find_all_shortest_paths(self, source, destination):
        """Find all shortest paths between two users using BFS"""
        if source not in self.graph or destination not in self.graph:
            return []
        
        # BFS to find shortest path length
        queue = deque([(source, [source])])
        visited = {source}
        shortest_length = None
        all_paths = []
        
        while queue:
            current, path = queue.popleft()
            
            if shortest_length and len(path) > shortest_length:
                break
            
            if current == destination:
                if shortest_length is None:
                    shortest_length = len(path)
                if len(path) == shortest_length:
                    all_paths.append(path)
                continue
            
            for neighbor in self.graph[current]:
                if neighbor not in visited or len(path) + 1 <= shortest_length:
                    queue.append((neighbor, path + [neighbor]))
                    visited.add(neighbor)
        
        return all_paths
    
    def detect_communities(self):
        """Detect communities using simple connected components"""
        visited = set()
        communities = []
        
        for user_id in self.users_data:
            if user_id not in visited:
                community = self._dfs_component(user_id, visited)
                if len(community) > 1:  # Only include actual communities
                    communities.append(community)
        
        return sorted(communities, key=len, reverse=True)
    
    def _dfs_component(self, start_user, visited):
        """DFS to find connected component (community)"""
        component = []
        stack = [start_user]
        
        while stack:
            user = stack.pop()
            if user not in visited:
                visited.add(user)
                component.append(user)
                
                for neighbor in self.graph[user]:
                    if neighbor not in visited:
                        stack.append(neighbor)
        
        return component
    
    def recommend_connections(self, user_id, max_recommendations=5):
        """Recommend new connections based on network structure"""
        if user_id not in self.graph:
            return []
        
        user_friends = self.graph[user_id]
        recommendations = defaultdict(int)
        
        # Friends of friends
        for friend in user_friends:
            for friend_of_friend in self.graph[friend]:
                if (friend_of_friend != user_id and 
                    friend_of_friend not in user_friends):
                    recommendations[friend_of_friend] += 1
        
        # Sort by number of mutual friends
        sorted_recommendations = sorted(
            recommendations.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        return [user_id for user_id, score in sorted_recommendations[:max_recommendations]]
    
    def analyze_network_health(self):
        """Analyze overall network health metrics"""
        total_users = len(self.users_data)
        total_connections = sum(len(friends) for friends in self.graph.values()) // 2
        
        # Calculate clustering coefficient
        clustering_coefficients = []
        for user_id in self.users_data:
            coefficient = self._local_clustering_coefficient(user_id)
            clustering_coefficients.append(coefficient)
        
        avg_clustering = sum(clustering_coefficients) / len(clustering_coefficients) if clustering_coefficients else 0
        
        # Calculate average path length (sample-based for efficiency)
        avg_path_length = self._estimate_average_path_length()
        
        return {
            'total_users': total_users,
            'total_connections': total_connections,
            'average_connections_per_user': total_connections * 2 / total_users if total_users > 0 else 0,
            'average_clustering_coefficient': avg_clustering,
            'estimated_average_path_length': avg_path_length,
            'network_density': total_connections / (total_users * (total_users - 1) / 2) if total_users > 1 else 0
        }
    
    def _local_clustering_coefficient(self, user_id):
        """Calculate local clustering coefficient for a user"""
        neighbors = self.graph[user_id]
        if len(neighbors) < 2:
            return 0
        
        possible_edges = len(neighbors) * (len(neighbors) - 1) // 2
        actual_edges = 0
        
        for neighbor1 in neighbors:
            for neighbor2 in neighbors:
                if neighbor1 < neighbor2 and neighbor2 in self.graph[neighbor1]:
                    actual_edges += 1
        
        return actual_edges / possible_edges if possible_edges > 0 else 0
    
    def _estimate_average_path_length(self, sample_size=100):
        """Estimate average path length using sampling"""
        import random
        
        user_ids = list(self.users_data.keys())
        if len(user_ids) < 2:
            return 0
        
        path_lengths = []
        
        for _ in range(min(sample_size, len(user_ids) * len(user_ids))):
            source = random.choice(user_ids)
            destination = random.choice(user_ids)
            
            if source != destination:
                shortest_path = self._find_shortest_path_length(source, destination)
                if shortest_path > 0:
                    path_lengths.append(shortest_path)
        
        return sum(path_lengths) / len(path_lengths) if path_lengths else 0
    
    def _find_shortest_path_length(self, source, destination):
        """Find shortest path length using BFS"""
        if source == destination:
            return 0
        
        queue = deque([(source, 0)])
        visited = {source}
        
        while queue:
            current, distance = queue.popleft()
            
            for neighbor in self.graph[current]:
                if neighbor == destination:
                    return distance + 1
                
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, distance + 1))
        
        return -1  # No path found

# Test the social graph analyzer
def test_social_graph_analyzer():
    sample_users = [
        {'user_id': 1, 'friend_ids': [2, 3, 4]},
        {'user_id': 2, 'friend_ids': [1, 3, 5]},
        {'user_id': 3, 'friend_ids': [1, 2, 4, 5]},
        {'user_id': 4, 'friend_ids': [1, 3]},
        {'user_id': 5, 'friend_ids': [2, 3, 6]},
        {'user_id': 6, 'friend_ids': [5, 7]},
        {'user_id': 7, 'friend_ids': [6]}
    ]
    
    analyzer = SocialGraphAnalyzer(sample_users)
    
    # Test influencer detection
    influencers = analyzer.find_influencers(3)
    print("Top influencers:", influencers)
    
    # Test community detection
    communities = analyzer.detect_communities()
    print("Communities found:", communities)
    
    # Test network health
    health_metrics = analyzer.analyze_network_health()
    print("Network health:", health_metrics)
    
    # Test connection recommendations
    recommendations = analyzer.recommend_connections(1)
    print("Recommendations for user 1:", recommendations)
    
    print("Social graph analysis test completed!")

if __name__ == "__main__":
    test_social_graph_analyzer()
```

## Question 3: Privacy-Aware Connection Filtering

**Problem**: Implement a privacy-aware filtering system that respects user preferences and prevents inappropriate suggestions.

### Solution:
```python
class PrivacyAwareRecommendationFilter:
    """Filter friend recommendations based on privacy preferences and safety rules"""
    
    def __init__(self):
        self.blocked_relationships = set()  # (user1, user2) tuples
        self.privacy_preferences = {}  # user_id -> preferences dict
    
    def add_blocked_relationship(self, user1_id, user2_id):
        """Add a blocked relationship (bidirectional)"""
        self.blocked_relationships.add((min(user1_id, user2_id), max(user1_id, user2_id)))
    
    def set_privacy_preferences(self, user_id, preferences):
        """Set privacy preferences for a user"""
        self.privacy_preferences[user_id] = preferences
    
    def filter_recommendations(self, target_user_id, candidate_recommendations, users_data):
        """
        Filter recommendations based on privacy rules and safety constraints
        
        Args:
            target_user_id: User receiving recommendations
            candidate_recommendations: List of (user_id, score) tuples
            users_data: Full user data for context
            
        Returns:
            Filtered list of (user_id, score) tuples
        """
        filtered_recommendations = []
        
        target_user = self._get_user_by_id(target_user_id, users_data)
        if not target_user:
            return []
        
        target_preferences = self.privacy_preferences.get(target_user_id, {})
        
        for candidate_id, score in candidate_recommendations:
            candidate_user = self._get_user_by_id(candidate_id, users_data)
            if not candidate_user:
                continue
            
            # Apply all privacy filters
            if self._should_filter_recommendation(
                target_user, candidate_user, target_preferences
            ):
                continue
            
            filtered_recommendations.append((candidate_id, score))
        
        return filtered_recommendations
    
    def _should_filter_recommendation(self, target_user, candidate_user, target_preferences):
        """Determine if a recommendation should be filtered out"""
        target_id = target_user['user_id']
        candidate_id = candidate_user['user_id']
        
        # Check blocked relationships
        if self._is_blocked_relationship(target_id, candidate_id):
            return True
        
        # Check geographic privacy
        if not self._check_geographic_privacy(target_user, candidate_user, target_preferences):
            return True
        
        # Check workplace privacy
        if not self._check_workplace_privacy(target_user, candidate_user, target_preferences):
            return True
        
        # Check contact book privacy
        if not self._check_contact_privacy(target_user, candidate_user, target_preferences):
            return True
        
        # Check mutual friends privacy
        if not self._check_mutual_friends_privacy(target_user, candidate_user, target_preferences):
            return True
        
        # Check candidate's privacy preferences
        candidate_preferences = self.privacy_preferences.get(candidate_id, {})
        if not self._check_candidate_privacy_preferences(
            target_user, candidate_user, candidate_preferences
        ):
            return True
        
        return False
    
    def _is_blocked_relationship(self, user1_id, user2_id):
        """Check if relationship is blocked"""
        return (min(user1_id, user2_id), max(user1_id, user2_id)) in self.blocked_relationships
    
    def _check_geographic_privacy(self, target_user, candidate_user, preferences):
        """Check geographic privacy constraints"""
        if preferences.get('disable_location_suggestions', False):
            return False
        
        # Check if suggestion is purely based on location proximity
        target_location = target_user.get('location', {})
        candidate_location = candidate_user.get('location', {})
        
        if (target_location and candidate_location and 
            self._is_same_location(target_location, candidate_location) and
            not self._has_other_connection_signals(target_user, candidate_user)):
            
            if preferences.get('restrict_location_only_suggestions', False):
                return False
        
        return True
    
    def _check_workplace_privacy(self, target_user, candidate_user, preferences):
        """Check workplace privacy constraints"""
        target_workplace = target_user.get('workplace', '')
        candidate_workplace = candidate_user.get('workplace', '')
        
        if target_workplace and target_workplace == candidate_workplace:
            if preferences.get('disable_workplace_suggestions', False):
                return False
            
            # Check for hierarchical relationships
            if (target_user.get('job_level', 0) != candidate_user.get('job_level', 0) and
                preferences.get('disable_hierarchy_suggestions', False)):
                return False
        
        return True
    
    def _check_contact_privacy(self, target_user, candidate_user, preferences):
        """Check contact book privacy constraints"""
        if preferences.get('disable_contact_suggestions', False):
            # Check if suggestion is based on contact book import
            if self._is_contact_based_suggestion(target_user, candidate_user):
                return False
        
        return True
    
    def _check_mutual_friends_privacy(self, target_user, candidate_user, preferences):
        """Check mutual friends privacy constraints"""
        min_mutual_friends = preferences.get('min_mutual_friends_for_suggestion', 0)
        
        target_friends = set(target_user.get('friend_ids', []))
        candidate_friends = set(candidate_user.get('friend_ids', []))
        mutual_friends = len(target_friends.intersection(candidate_friends))
        
        return mutual_friends >= min_mutual_friends
    
    def _check_candidate_privacy_preferences(self, target_user, candidate_user, candidate_preferences):
        """Check if candidate wants to appear in suggestions"""
        # Check if candidate has opted out of appearing in suggestions
        if candidate_preferences.get('opt_out_of_suggestions', False):
            return False
        
        # Check if candidate restricts suggestions to mutual friends only
        if candidate_preferences.get('suggestions_mutual_friends_only', False):
            target_friends = set(target_user.get('friend_ids', []))
            candidate_friends = set(candidate_user.get('friend_ids', []))
            if len(target_friends.intersection(candidate_friends)) == 0:
                return False
        
        return True
    
    def _is_same_location(self, loc1, loc2):
        """Check if two locations are the same (simplified)"""
        return (loc1.get('city', '') == loc2.get('city', '') and
                loc1.get('country', '') == loc2.get('country', ''))
    
    def _has_other_connection_signals(self, target_user, candidate_user):
        """Check if there are connection signals beyond location"""
        # Check for mutual friends
        target_friends = set(target_user.get('friend_ids', []))
        candidate_friends = set(candidate_user.get('friend_ids', []))
        if len(target_friends.intersection(candidate_friends)) > 0:
            return True
        
        # Check for shared workplace, school, etc.
        if (target_user.get('workplace', '') == candidate_user.get('workplace', '') or
            target_user.get('school', '') == candidate_user.get('school', '')):
            return True
        
        return False
    
    def _is_contact_based_suggestion(self, target_user, candidate_user):
        """Check if suggestion is based on contact book (simplified)"""
        # In real implementation, would check against contact import data
        target_contacts = target_user.get('imported_contacts', [])
        candidate_phone = candidate_user.get('phone_number', '')
        candidate_email = candidate_user.get('email', '')
        
        return (candidate_phone in target_contacts or 
                candidate_email in target_contacts)
    
    def _get_user_by_id(self, user_id, users_data):
        """Helper to find user by ID"""
        for user in users_data:
            if user['user_id'] == user_id:
                return user
        return None

# Test the privacy filter
def test_privacy_filter():
    filter_system = PrivacyAwareRecommendationFilter()
    
    # Set up test data
    users_data = [
        {
            'user_id': 1, 
            'friend_ids': [2], 
            'workplace': 'TechCorp',
            'location': {'city': 'San Francisco', 'country': 'US'},
            'imported_contacts': ['user3@email.com']
        },
        {
            'user_id': 2, 
            'friend_ids': [1, 3], 
            'workplace': 'TechCorp',
            'location': {'city': 'San Francisco', 'country': 'US'}
        },
        {
            'user_id': 3, 
            'friend_ids': [2], 
            'workplace': 'OtherCorp',
            'email': 'user3@email.com',
            'location': {'city': 'San Francisco', 'country': 'US'}
        },
        {
            'user_id': 4, 
            'friend_ids': [], 
            'workplace': 'TechCorp',
            'location': {'city': 'New York', 'country': 'US'}
        }
    ]
    
    # Set privacy preferences
    filter_system.set_privacy_preferences(1, {
        'disable_workplace_suggestions': True,
        'min_mutual_friends_for_suggestion': 1
    })
    
    # Add blocked relationship
    filter_system.add_blocked_relationship(1, 4)
    
    # Test filtering
    candidate_recommendations = [(2, 10), (3, 8), (4, 6)]
    filtered = filter_system.filter_recommendations(1, candidate_recommendations, users_data)
    
    print("Original candidates:", candidate_recommendations)
    print("Filtered recommendations:", filtered)
    print("Privacy filter test completed!")

if __name__ == "__main__":
    test_privacy_filter()
```

## Key Concepts

1. **Graph Algorithms**: Social network analysis using graph theory
2. **Privacy Engineering**: Building privacy-aware recommendation systems
3. **Machine Learning**: Scoring and ranking algorithms for recommendations
4. **System Design**: Scalable architecture for large social networks
5. **Trust & Safety**: Preventing inappropriate suggestions and protecting user privacy 