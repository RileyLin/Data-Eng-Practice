# Scenario 8: Messenger (WhatsApp/Telegram) - Python Questions

## Question 1: Message Stream Processing & Chat State Management

**Problem**: Simulate processing a stream of incoming messages for a chat application. Manage basic chat state, such as participant lists and simple typing indicators (without actual UI, just state changes).

**Key Requirements**:
-   Process events like `user_joins_chat`, `user_leaves_chat`, `message_sent`, `user_starts_typing`, `user_stops_typing`.
-   Maintain a dictionary representing the state of multiple chats (participants, active typers).
-   Log state changes or output current state after certain events.

### Solution:

```python
from collections import defaultdict
import time

class ChatServer:
    def __init__(self):
        # chat_states: {chat_id: {'participants': set(), 'typing_users': set(), 'last_activity': timestamp}}
        self.chat_states = defaultdict(lambda: {'participants': set(), 'typing_users': set(), 'last_activity': time.time()})
        self.event_log = []

    def process_event(self, event):
        """Processes an incoming chat event."""
        chat_id = event.get('chat_id')
        user_id = event.get('user_id')
        event_type = event.get('event_type')
        timestamp = event.get('timestamp', time.time())

        log_entry = {"timestamp": timestamp, "event": event_type, "chat_id": chat_id, "user_id": user_id}
        self.chat_states[chat_id]['last_activity'] = timestamp

        if event_type == 'user_joins_chat':
            self.chat_states[chat_id]['participants'].add(user_id)
            log_entry["details"] = f"User {user_id} joined. Participants: {self.chat_states[chat_id]['participants']}"
        elif event_type == 'user_leaves_chat':
            self.chat_states[chat_id]['participants'].discard(user_id)
            self.chat_states[chat_id]['typing_users'].discard(user_id) # User also stops typing if they leave
            log_entry["details"] = f"User {user_id} left. Participants: {self.chat_states[chat_id]['participants']}"
        elif event_type == 'message_sent':
            message_content = event.get('content', '')
            self.chat_states[chat_id]['typing_users'].discard(user_id) # Sending a message implies stopping typing
            log_entry["details"] = f"User {user_id} sent: '{message_content}'. Typers: {self.chat_states[chat_id]['typing_users']}"
        elif event_type == 'user_starts_typing':
            if user_id in self.chat_states[chat_id]['participants']:
                self.chat_states[chat_id]['typing_users'].add(user_id)
            log_entry["details"] = f"User {user_id} started typing. Typers: {self.chat_states[chat_id]['typing_users']}"
        elif event_type == 'user_stops_typing':
            self.chat_states[chat_id]['typing_users'].discard(user_id)
            log_entry["details"] = f"User {user_id} stopped typing. Typers: {self.chat_states[chat_id]['typing_users']}"
        else:
            log_entry["details"] = "Unknown event type"
            
        self.event_log.append(log_entry)
        # print(log_entry) # For real-time observation

    def get_chat_state(self, chat_id):
        return self.chat_states.get(chat_id)

    def get_active_chats(self, since_timestamp):
        return {cid: state for cid, state in self.chat_states.items() if state['last_activity'] >= since_timestamp}

# Test Cases
def test_chat_server_processing():
    server = ChatServer()
    events = [
        {'chat_id': 'chat1', 'user_id': 'Alice', 'event_type': 'user_joins_chat', 'timestamp': time.time()},
        {'chat_id': 'chat1', 'user_id': 'Bob', 'event_type': 'user_joins_chat', 'timestamp': time.time() + 1},
        {'chat_id': 'chat1', 'user_id': 'Alice', 'event_type': 'user_starts_typing', 'timestamp': time.time() + 2},
        {'chat_id': 'chat2', 'user_id': 'Charlie', 'event_type': 'user_joins_chat', 'timestamp': time.time() + 3},
        {'chat_id': 'chat1', 'user_id': 'Alice', 'event_type': 'message_sent', 'content': 'Hello Bob!', 'timestamp': time.time() + 4},
        {'chat_id': 'chat1', 'user_id': 'Bob', 'event_type': 'user_starts_typing', 'timestamp': time.time() + 5},
        {'chat_id': 'chat1', 'user_id': 'Bob', 'event_type': 'user_stops_typing', 'timestamp': time.time() + 7},
        {'chat_id': 'chat1', 'user_id': 'Alice', 'event_type': 'user_leaves_chat', 'timestamp': time.time() + 8},
        {'chat_id': 'chat2', 'user_id': 'Charlie', 'event_type': 'message_sent', 'content': 'Hi there', 'timestamp': time.time() + 9},
    ]

    for event in events:
        server.process_event(event)

    chat1_state = server.get_chat_state('chat1')
    print("Chat1 Final State:", chat1_state)
    assert 'Bob' in chat1_state['participants']
    assert 'Alice' not in chat1_state['participants']
    assert not chat1_state['typing_users'] # Alice left, Bob stopped typing

    chat2_state = server.get_chat_state('chat2')
    print("Chat2 Final State:", chat2_state)
    assert 'Charlie' in chat2_state['participants']
    
    active_chats_now = server.get_active_chats(time.time() - 10)
    assert 'chat1' in active_chats_now
    assert 'chat2' in active_chats_now
    print("Chat server processing test passed.")

if __name__ == "__main__":
    test_chat_server_processing()
```

---

## Question 2: Simple End-to-End Encryption Simulation

**Problem**: Implement a highly simplified simulation of end-to-end encryption for messages. This will not use real cryptography but will demonstrate the concept of encrypting with a recipient's key and decrypting with a private key.

**Key Requirements**:
-   Functions for `generate_key_pair` (simulated), `encrypt_message` (using a public key), `decrypt_message` (using a private key).
-   The encryption should be a simple reversible transformation (e.g., Caesar cipher with key, or XOR with key).
-   Demonstrate that a message encrypted with a public key can only be decrypted by the corresponding private key.

### Solution:

```python
import os
import hashlib

def generate_key_pair(user_id):
    """Generates a simplified public/private key pair based on user_id."""
    # Using hash for deterministic "keys" for simulation purposes
    private_key_seed = hashlib.sha256((user_id + "_private_secret").encode()).hexdigest()
    public_key_seed = hashlib.sha256((user_id + "_public_reveal").encode()).hexdigest()
    
    # For Caesar cipher like simulation, key is an integer shift
    private_key = int(private_key_seed[:5], 16) % 25 + 1 # Shift between 1-25
    public_key = int(public_key_seed[:5], 16) % 25 + 1
    
    # Ensure public and private keys for Caesar cipher are related for decryption (same shift value)
    # In a real E2EE, these would be mathematically linked (e.g. RSA, ECC)
    # For this simulation, we'll make them the same for simplicity of Caesar cipher
    # A better simulation would involve more distinct but related keys for a different algorithm.
    shared_shift = private_key 
    return {'public_key': shared_shift, 'private_key': shared_shift} 

def encrypt_message_caesar(message, public_key_shift):
    """Encrypts message using a Caesar cipher with the public key shift."""
    encrypted_text = ""
    for char in message:
        if 'a' <= char <= 'z':
            encrypted_text += chr((ord(char) - ord('a') + public_key_shift) % 26 + ord('a'))
        elif 'A' <= char <= 'Z':
            encrypted_text += chr((ord(char) - ord('A') + public_key_shift) % 26 + ord('A'))
        else:
            encrypted_text += char
    return encrypted_text

def decrypt_message_caesar(encrypted_message, private_key_shift):
    """Decrypts message using a Caesar cipher with the private key shift."""
    decrypted_text = ""
    for char in encrypted_message:
        if 'a' <= char <= 'z':
            decrypted_text += chr((ord(char) - ord('a') - private_key_shift + 26) % 26 + ord('a'))
        elif 'A' <= char <= 'Z':
            decrypted_text += chr((ord(char) - ord('A') - private_key_shift + 26) % 26 + ord('A'))
        else:
            decrypted_text += char
    return decrypted_text

# Test Cases
def test_e2ee_simulation():
    alice_keys = generate_key_pair("Alice")
    bob_keys = generate_key_pair("Bob")

    message_to_bob = "Hello Bob, this is a secret message!"

    # Alice encrypts for Bob using Bob's public key
    encrypted_for_bob = encrypt_message_caesar(message_to_bob, bob_keys['public_key'])
    print(f"Original: {message_to_bob}")
    print(f"Encrypted for Bob (using Bob's PK {bob_keys['public_key']}): {encrypted_for_bob}")

    # Bob decrypts using his private key
    decrypted_by_bob = decrypt_message_caesar(encrypted_for_bob, bob_keys['private_key'])
    print(f"Decrypted by Bob (using Bob's SK {bob_keys['private_key']}): {decrypted_by_bob}")
    assert decrypted_by_bob == message_to_bob

    # Attempt to decrypt with Alice's private key (should fail or produce gibberish)
    decrypted_by_alice_incorrectly = decrypt_message_caesar(encrypted_for_bob, alice_keys['private_key'])
    print(f"Attempted decryption by Alice (using Alice's SK {alice_keys['private_key']}): {decrypted_by_alice_incorrectly}")
    assert decrypted_by_alice_incorrectly != message_to_bob

    print("E2EE simulation test passed.")

if __name__ == "__main__":
    test_chat_server_processing()
    print("\n---\n")
    test_e2ee_simulation()

```

---

## Question 3: User Message Rate Limiting

**Problem**: Implement a function that checks if a user has exceeded a message rate limit (e.g., max N messages in M seconds). This is a common technique to prevent spam or abuse.

**Key Requirements**:
-   Track message timestamps for each user.
-   A function `is_rate_limited(user_id, current_timestamp)` that returns True if the user should be blocked.
-   Configurable rate limit (e.g., 5 messages in 10 seconds).

### Solution:

```python
from collections import defaultdict, deque

class UserRateLimiter:
    def __init__(self, max_messages, time_window_seconds):
        self.max_messages = max_messages
        self.time_window_seconds = time_window_seconds
        # user_message_timestamps: {user_id: deque([timestamp1, timestamp2, ...])}
        self.user_message_timestamps = defaultdict(deque)

    def record_message(self, user_id, timestamp):
        """Records a message event for the user and cleans up old timestamps."""
        user_ts_deque = self.user_message_timestamps[user_id]
        user_ts_deque.append(timestamp)
        
        # Remove timestamps older than the time window
        while user_ts_deque and user_ts_deque[0] <= timestamp - self.time_window_seconds:
            user_ts_deque.popleft()

    def is_rate_limited(self, user_id, current_timestamp):
        """
        Checks if the user is currently rate-limited. 
        Also performs cleanup of their timestamp deque based on current_timestamp.
        """
        user_ts_deque = self.user_message_timestamps[user_id]
        
        # Clean up old timestamps before checking
        while user_ts_deque and user_ts_deque[0] <= current_timestamp - self.time_window_seconds:
            user_ts_deque.popleft()
            
        return len(user_ts_deque) >= self.max_messages

    def attempt_message(self, user_id, timestamp):
        """
        Combines checking rate limit and recording the message if not limited.
        Returns True if message is allowed, False if rate-limited.
        """
        if self.is_rate_limited(user_id, timestamp):
            return False # User is rate-limited
        
        self.record_message(user_id, timestamp)
        return True # Message allowed and recorded

# Test Cases
def test_rate_limiter():
    # Limit: 3 messages in 5 seconds
    limiter = UserRateLimiter(max_messages=3, time_window_seconds=5)
    user_id = "test_user"

    current_time = time.time()
    assert limiter.attempt_message(user_id, current_time) == True # Msg 1
    assert limiter.attempt_message(user_id, current_time + 1) == True # Msg 2
    assert limiter.attempt_message(user_id, current_time + 2) == True # Msg 3
    assert limiter.attempt_message(user_id, current_time + 3) == False # Msg 4 (Rate limited - 4th in <5s)

    # Wait for the window to pass for the first message
    assert limiter.attempt_message(user_id, current_time + 5.1) == True # Msg 1 expired, Msg 4 allowed (now 3rd in last 5s)
    # Timestamps: [t+1, t+2, t+5.1]
    assert limiter.is_rate_limited(user_id, current_time + 5.1) == True # Still 3 messages
    
    assert limiter.attempt_message(user_id, current_time + 6) == False # Still 3 messages in window [t+1, t+2, t+5.1]
                                                                      # Window is [t+1, t+6], messages are t+1,t+2,t+5.1
    # Wait for another message to expire
    # current_time + 7: window starts at current_time + 2
    # messages in window: [current_time + 2, current_time + 5.1]
    assert limiter.is_rate_limited(user_id, current_time + 7) == False
    assert limiter.attempt_message(user_id, current_time + 7) == True # Allowed.
    # Messages in deque: [t+2, t+5.1, t+7]
    assert limiter.is_rate_limited(user_id, current_time + 7) == True

    print("User rate limiter test passed.")

if __name__ == "__main__":
    test_chat_server_processing()
    print("\n---\n")
    test_e2ee_simulation()
    print("\n---\n")
    test_rate_limiter()

```

## Key Concepts Tested
1.  **Real-time Event Processing**: Simulating how a server might handle a stream of events from clients.
2.  **State Management**: Maintaining and updating the state of different entities (chats, users) based on events.
3.  **Basic Cryptography Concepts (Simulation)**: Understanding the principles of public/private key pairs for encryption, even with simplified algorithms.
4.  **Rate Limiting Algorithms**: Implementing a common strategy (sliding window counter with deques) to prevent abuse.
5.  **Data Structures**: Effective use of dictionaries, sets, and deques for managing state and timestamps.
6.  **Time-based Logic**: Handling timestamps for event ordering and windowed calculations (rate limiting). 