import logging
import time
import requests
from datetime import datetime, timedelta
from settings import config

logger = logging.getLogger(__name__)

class NewsManager:
    """
    Manages News Filtering to avoid trading during High-Impact events.
    """
    def __init__(self):
        self.events = []
        self.last_fetch = 0
        self.fetch_interval = 3600 * 6 # 6 Hours
        # Currencies we care about
        self.watched_currencies = ['USD', 'EUR', 'GBP'] 
        
    def fetch_calendar(self):
        """
        Fetches economic calendar. 
        Note: Reliable free APIs are scarce. We will use a simple heuristic 
        or a known public JSON feed if available. 
        For now, this attempts to pull from a common public endpoint or returns empty.
        """
        # Placeholder for robust fetching. 
        # In a real production env, you'd use an API key from FxStreet or similar.
        # For this implementation, we will rely on manual toggling or a mock list 
        # unless we find a stable public url.
        self.events = []
        self.last_fetch = time.time()
        logger.info("📰 NewsManager: Calendar fetch simulated (Empty). Manual filter only for now.")

    def is_news_time(self, asset: str) -> tuple[bool, str]:
        """
        Checks if the current time is inside a News Blackout window for the given asset.
        
        Args:
            asset (str): e.g. "EURUSD"
            
        Returns:
            (bool, str): (Is News Time?, Reason)
        """
        if not getattr(config, 'news_filter_on', False):
            return False, "Filter OFF"

        # 1. Update calendar if stale
        if time.time() - self.last_fetch > self.fetch_interval:
            self.fetch_calendar()

        # 2. Check events (Placeholder logic)
        # Real logic: Iterate self.events, check if 'currency' in asset, check time window.
        # for event in self.events: ...
        
        # 3. Manual Block Check (if user set a temporary block via existing mechanism?)
        # For now, we assume "Filter ON" implies we are guarding against events we know.
        # Since we don't have a live feed value yet, this safeguards against 'False Positives' 
        # by returning False unless we populate events.
        
        return False, "No Event"

    def toggle(self, state: bool):
        config.news_filter_on = state
        logger.info(f"📰 News Filter set to: {state}")

    def get_status(self):
        state = getattr(config, 'news_filter_on', False)
        return f"News Filter: {'✅ ON' if state else '❌ OFF'}"

# Global Instance
news_manager = NewsManager()
