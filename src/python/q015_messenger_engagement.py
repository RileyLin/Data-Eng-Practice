"""
Question 8.4.1: Analyzing Messenger Engagement Patterns

Design a Python function to analyze user engagement patterns in a messaging application
like Facebook Messenger. Consider metrics such as:
- Daily/weekly active users in chats
- Average number of messages per user
- Distribution of chat types (1:1 vs. group)
- Usage of features like reactions, stickers, or voice notes
- Identifying highly engaged users vs. users at risk of churn based on activity.

The function should take a list of user activity logs as input and return
a summary of these engagement metrics.

DATA STRUCTURE EXAMPLES:

Input: user_activity_logs (List[Dict])
- Example: [
    {'user_id': 'u1', 'timestamp': 1678886400, 'action': 'send_message', 'chat_id': 'c1', 'chat_type': '1:1'},
    {'user_id': 'u2', 'timestamp': 1678886460, 'action': 'send_message', 'chat_id': 'c1', 'chat_type': '1:1'},
    {'user_id': 'u1', 'timestamp': 1678886520, 'action': 'add_reaction', 'message_id': 'm1'},
    {'user_id': 'u3', 'timestamp': 1678886580, 'action': 'send_message', 'chat_id': 'g1', 'chat_type': 'group'}
]

Output: engagement_summary (Dict)
- Example: {
    'daily_active_users': 1500,
    'avg_messages_per_user': 12.5,
    'chat_type_distribution': {'1:1': 0.7, 'group': 0.3},
    'top_reaction': '❤️'
}
"""

def analyze_messenger_engagement(user_activity_logs):
    """
    Analyzes user engagement patterns in a messaging application.
    (Placeholder implementation)
    """
    # Placeholder: Replace with actual logic
    if not user_activity_logs:
        return None 

    user_id_set = set()

    total_one_message = 0
    total_group_message = 0



    for log in user_activity_logs:
        if not all(i in log for i in ['user_id','action','chat_type']):
            continue 
        user_id = log['user_id']
        action = log['action']
        chat_type = log['chat_type']

        user_id_set.add(user_id)
        
        if action =='send_message':
            if chat_type == '1:1':
                total_one_message+=1
            else:
                total_group_message+=1
    
    total_messages = total_one_message+total_group_message

    one_message_perc = (total_one_message/total_messages) if total_messages else 0 

    group_message_perc = (total_group_message/total_messages) if total_messages else 0

    num_of_users = len(user_id_set)

    avg_message = (total_messages/num_of_users) if num_of_users else 0 

    result = {
        'daily_active_users':num_of_users,
        'avg_message_per_users':avg_message,
        'chat_type_distribution': {'1:1': one_message_perc, 'group': group_message_perc},
        'top_reaction': None

    }

    print(result)
    return result


#Example Test Cases (Conceptual)
def test_analyze_messenger_engagement():
    logs = [
        {'user_id': 'u1', 'timestamp': 1678886400, 'action': 'send_message', 'chat_id': 'c1', 'chat_type': '1:1'},
        {'user_id': 'u2', 'timestamp': 1678886460, 'action': 'send_message', 'chat_id': 'c1', 'chat_type': '1:1'}
    ]
    summary = analyze_messenger_engagement(logs)
    assert summary['daily_active_users'] == 2
    assert summary['avg_message_per_users'] == 1.0
    assert summary['chat_type_distribution']['1:1'] == 1.0
    assert summary['chat_type_distribution']['group'] == 0.0
    print("Test case 1 (Basic 1:1) passed.")

def test_empty_log():
    logs = []
    summary = analyze_messenger_engagement(logs)
    # Current code will error here due to division by zero if not handled
    # For now, let's assert the state before potential error, or expect an error
    # Depending on desired behavior for empty logs / no messages
    assert summary['daily_active_users'] == 0
    assert summary['avg_message_per_users'] == 0 # Expected if handled
    assert summary['chat_type_distribution']['1:1'] == 0 # Expected if handled
    assert summary['chat_type_distribution']['group'] == 0 # Expected if handled
    print("Test case 2 (Empty Log) passed - requires handling for 0 messages.")

def test_group_messages_only():
    logs = [
        {'user_id': 'u1', 'timestamp': 1678886400, 'action': 'send_message', 'chat_id': 'g1', 'chat_type': 'group'},
        {'user_id': 'u1', 'timestamp': 1678886460, 'action': 'send_message', 'chat_id': 'g1', 'chat_type': 'group'},
        {'user_id': 'u2', 'timestamp': 1678886500, 'action': 'send_message', 'chat_id': 'g2', 'chat_type': 'group'},
    ]
    summary = analyze_messenger_engagement(logs)
    assert summary['daily_active_users'] == 2
    assert summary['avg_message_per_users'] == 1.5
    assert summary['chat_type_distribution']['1:1'] == 0.0
    assert summary['chat_type_distribution']['group'] == 1.0
    print("Test case 3 (Group Messages Only) passed.")

def test_mixed_messages_and_users():
    logs = [
        {'user_id': 'u1', 'timestamp': 1678886400, 'action': 'send_message', 'chat_id': 'c1', 'chat_type': '1:1'},
        {'user_id': 'u1', 'timestamp': 1678886402, 'action': 'add_reaction', 'message_id': 'm1', 'reaction_type': '❤️'},
        {'user_id': 'u2', 'timestamp': 1678886460, 'action': 'send_message', 'chat_id': 'c1', 'chat_type': '1:1'},
        {'user_id': 'u1', 'timestamp': 1678886520, 'action': 'send_message', 'chat_id': 'g1', 'chat_type': 'group'},
        {'user_id': 'u3', 'timestamp': 1678886580, 'action': 'send_message', 'chat_id': 'g1', 'chat_type': 'group'},
        {'user_id': 'u3', 'timestamp': 1678886582, 'action': 'add_reaction', 'message_id': 'm2', 'reaction_type': '👍'},
        {'user_id': 'u3', 'timestamp': 1678886585, 'action': 'add_reaction', 'message_id': 'm3', 'reaction_type': '❤️'},
    ]
    summary = analyze_messenger_engagement(logs)
    assert summary['daily_active_users'] == 3
    # u1: 2 messages, u2: 1 message, u3: 1 message. Total 4 messages.
    assert summary['avg_message_per_users'] == 4 / 3
    # 1:1 messages: 2 (from u1, u2)
    # Group messages: 2 (from u1, u3)
    assert summary['chat_type_distribution']['1:1'] == 0.5
    assert summary['chat_type_distribution']['group'] == 0.5
    # top_reaction is not implemented yet, so it will be None
    assert summary['top_reaction'] is None 
    print("Test case 4 (Mixed Messages, Users, Actions) passed.")

def test_no_messages_sent():
    logs = [
        {'user_id': 'u1', 'timestamp': 1678886402, 'action': 'add_reaction', 'message_id': 'm1', 'reaction_type': '❤️'},
        {'user_id': 'u2', 'timestamp': 1678886585, 'action': 'add_reaction', 'message_id': 'm3', 'reaction_type': '❤️'},
    ]
    summary = analyze_messenger_engagement(logs)
    assert summary['daily_active_users'] == 2
    # Current code will error here due to division by zero for avg_message_per_users and chat_type_distribution
    # Asserting expected behavior if handled:
    assert summary['avg_message_per_users'] == 0
    assert summary['chat_type_distribution']['1:1'] == 0
    assert summary['chat_type_distribution']['group'] == 0
    print("Test case 5 (No Messages Sent) passed - requires handling for 0 messages.")

if __name__ == "__main__":
    test_analyze_messenger_engagement()
    # test_empty_log()
    test_group_messages_only()
    test_mixed_messages_and_users()
    test_no_messages_sent() 