#!/usr/bin/env python3
"""
Meta Data Engineer Interview - Scenario 3: Ads Attribution Analytics  
Problem 4: Python Data Processing - Real-time Attribution Engine

Time Limit: 8 minutes

Scenario: Build an ad attribution system that tracks user interactions across
multiple touchpoints and assigns conversion credit to ads. Must handle complex
customer journeys with multiple devices and privacy constraints.

Your Task:
1. Track user touchpoints across ad impressions and conversions
2. Implement attribution models (last-click, first-click, linear)
3. Handle cross-device attribution with probabilistic matching
4. Calculate advertiser ROI metrics in real-time

Requirements:
- Process 1M+ ad events per minute
- Support multiple attribution windows (1, 7, 28 days)
- Handle privacy-safe user matching
- Real-time conversion attribution

Follow-up: How would you adapt this for iOS privacy changes?
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from collections import defaultdict, deque
from dataclasses import dataclass
from enum import Enum
import hashlib
import threading


class EventType(Enum):
    AD_IMPRESSION = "ad_impression"
    AD_CLICK = "ad_click"
    PURCHASE = "purchase"
    ADD_TO_CART = "add_to_cart"
    PAGE_VIEW = "page_view"


class AttributionModel(Enum):
    LAST_CLICK = "last_click"
    FIRST_CLICK = "first_click"
    LINEAR = "linear"
    TIME_DECAY = "time_decay"


@dataclass
class AdEvent:
    user_id: str  # Hashed/pseudonymized ID
    event_type: EventType
    timestamp: datetime
    campaign_id: str
    ad_group_id: str
    device_id: Optional[str] = None
    conversion_value: Optional[float] = None
    metadata: Dict = None


# Sample ad events
SAMPLE_EVENTS = [
    AdEvent("user_hash_123", EventType.AD_IMPRESSION, datetime.now() - timedelta(days=5), "camp_1", "adg_1"),
    AdEvent("user_hash_123", EventType.AD_CLICK, datetime.now() - timedelta(days=3), "camp_1", "adg_1"),
    AdEvent("user_hash_123", EventType.PURCHASE, datetime.now(), "camp_1", "adg_1", conversion_value=49.99),
]


class AttributionEngine:
    """
    Real-time ad attribution system
    
    TODO: Implement your solution here
    Requirements:
    - Track user journey across multiple touchpoints
    - Support multiple attribution models
    - Handle attribution windows (1, 7, 28 days)
    - Calculate conversion attribution in real-time
    """
    
    def __init__(self, attribution_window_days: int = 28):
        # YOUR CODE HERE
        pass
        
    def add_event(self, event: AdEvent):
        """
        Add ad event to attribution tracking
        
        TODO: Implement your solution here
        """
        # YOUR CODE HERE
        pass
        
    def get_attribution(self, conversion_event: AdEvent, 
                       model: AttributionModel) -> Dict[str, float]:
        """
        Calculate attribution for a conversion event
        
        TODO: Implement your solution here
        Returns: Dict mapping campaign_id to attribution credit (0.0-1.0)
        
        Attribution Models:
        - LAST_CLICK: 100% credit to last clicked ad
        - FIRST_CLICK: 100% credit to first clicked ad  
        - LINEAR: Equal credit across all touchpoints
        - TIME_DECAY: More credit to recent touchpoints
        """
        # YOUR CODE HERE
        pass
        
    def get_campaign_conversions(self, campaign_id: str, 
                               days_back: int = 7) -> Dict[str, float]:
        """
        Get conversion metrics for campaign
        
        TODO: Implement your solution here
        Returns: {
            'total_conversions': float,
            'conversion_value': float,
            'attributed_conversions': float
        }
        """
        # YOUR CODE HERE
        pass


class CrossDeviceLinker:
    """
    Link user activities across multiple devices
    
    TODO: Implement your solution here
    Requirements:
    - Probabilistic device matching using signals
    - Privacy-safe linking without PII
    - Handle login events and behavioral patterns
    - Confidence scoring for matches
    """
    
    def __init__(self):
        # YOUR CODE HERE
        pass
        
    def add_device_signal(self, user_id: str, device_id: str, 
                         signals: Dict[str, str]):
        """
        Add device signals for cross-device linking
        
        TODO: Implement your solution here
        Signals might include: IP address, user agent, timezone, etc.
        """
        # YOUR CODE HERE
        pass
        
    def get_linked_devices(self, device_id: str) -> List[Tuple[str, float]]:
        """
        Get devices linked to given device
        
        TODO: Implement your solution here
        Returns: List of (device_id, confidence_score) tuples
        """
        # YOUR CODE HERE
        pass
        
    def get_unified_user_id(self, device_id: str) -> str:
        """
        Get unified user ID for device
        
        TODO: Implement your solution here
        """
        # YOUR CODE HERE
        pass


def calculate_roas(attributed_conversions: float, 
                  conversion_value: float,
                  ad_spend: float) -> Dict[str, float]:
    """
    Calculate Return on Ad Spend (ROAS) metrics
    
    TODO: Implement your solution here
    Requirements:
    - Calculate ROAS = Revenue / Ad Spend
    - Calculate CPA = Ad Spend / Conversions
    - Calculate conversion rate
    - Handle edge cases (zero spend, zero conversions)
    
    Returns:
        Dict with ROAS, CPA, conversion_rate, and other key metrics
    """
    # YOUR CODE HERE
    pass


def privacy_safe_hash(user_identifier: str, salt: str = "meta_salt") -> str:
    """
    Create privacy-safe hash of user identifier
    
    TODO: Implement your solution here
    Requirements:
    - One-way hash function
    - Consistent across sessions
    - Difficult to reverse
    - Include salt for security
    """
    # YOUR CODE HERE
    pass


def test_attribution_engine():
    """Test the attribution engine"""
    print("Testing Attribution Engine...")
    
    engine = AttributionEngine()
    
    # Add sample events
    for event in SAMPLE_EVENTS:
        engine.add_event(event)
    
    # Test attribution calculation
    conversion_event = SAMPLE_EVENTS[-1]  # Purchase event
    
    attribution = engine.get_attribution(conversion_event, AttributionModel.LAST_CLICK)
    print(f"Last-click attribution: {attribution}")
    
    attribution = engine.get_attribution(conversion_event, AttributionModel.LINEAR)
    print(f"Linear attribution: {attribution}")
    
    # Test campaign metrics
    metrics = engine.get_campaign_conversions("camp_1")
    print(f"Campaign metrics: {metrics}")


def test_cross_device_linker():
    """Test cross-device linking"""
    print("\nTesting Cross-Device Linker...")
    
    linker = CrossDeviceLinker()
    
    # Add device signals
    linker.add_device_signal("user_123", "device_mobile", {
        "ip_address": "192.168.1.100",
        "user_agent": "Mobile Safari",
        "timezone": "UTC-8"
    })
    
    linker.add_device_signal("user_123", "device_desktop", {
        "ip_address": "192.168.1.100",  # Same IP
        "user_agent": "Chrome Desktop",
        "timezone": "UTC-8"  # Same timezone
    })
    
    # Test device linking
    linked = linker.get_linked_devices("device_mobile")
    print(f"Linked devices: {linked}")
    
    unified_id = linker.get_unified_user_id("device_mobile")
    print(f"Unified user ID: {unified_id}")


def test_roas_calculation():
    """Test ROAS calculation"""
    print("\nTesting ROAS Calculation...")
    
    # Test normal case
    roas_metrics = calculate_roas(
        attributed_conversions=100.0,
        conversion_value=5000.0,
        ad_spend=1000.0
    )
    print(f"ROAS metrics: {roas_metrics}")
    
    # Test edge case - zero spend
    roas_metrics = calculate_roas(
        attributed_conversions=50.0,
        conversion_value=2500.0,
        ad_spend=0.0
    )
    print(f"Zero spend ROAS: {roas_metrics}")


def test_privacy_hashing():
    """Test privacy-safe hashing"""
    print("\nTesting Privacy Hashing...")
    
    user_email = "user@example.com"
    hashed_1 = privacy_safe_hash(user_email)
    hashed_2 = privacy_safe_hash(user_email)
    
    print(f"Original: {user_email}")
    print(f"Hash 1: {hashed_1}")
    print(f"Hash 2: {hashed_2}")
    print(f"Consistent: {hashed_1 == hashed_2}")


if __name__ == "__main__":
    print("Meta Ads Attribution Analytics - Python Processing Challenge")
    print("=" * 60)
    
    # Run tests to verify your implementation
    test_attribution_engine()
    test_cross_device_linker()
    test_roas_calculation()
    test_privacy_hashing()
    
    print("\n" + "=" * 60)
    print("Complete your implementation and run again to test!")
    print("Focus on:")
    print("1. Accurate attribution model implementation")
    print("2. Privacy-safe cross-device linking")
    print("3. Real-time performance at scale")
    print("4. Robust ROAS calculation with edge cases") 