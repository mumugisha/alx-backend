#!/usr/bin/env python3
"""BaseCaching module
"""
from base_caching import BaseCaching


class FIFOCache(BaseCaching):
    """FIFO Cache defines the caching system
    """

    def __init__(self):
        """Initialize the FIFO cache
        """
        super().__init__()
        self.order = []

    def put(self, key: str, item: any) -> None:
        """Add an item in the cache

        Args:
            key: The key for the item
            item: The item to cache
        """
        if key is None or item is None:
            return

        if key not in self.cache_data:
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                discarded_key = self.order.pop(0)
                del self.cache_data[discarded_key]
                print("DISCARD: {}".format(discarded_key))

        self.cache_data[key] = item
        self.order.append(key)

    def get(self, key: str) -> any:
        """Get an item by key

        Args:
            key: The key for the item
        Returns:
            The cached item or None if not found
        """
        if key is None or key not in self.cache_data:
            return None
        return self.cache_data[key]
