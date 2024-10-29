#!/usr/bin/env python3
""" BasicCache module """

from base_caching import BaseCaching


class BasicCache(BaseCaching):
    """
    BasicCache class that inherits from BaseCaching and
    provides a simple caching system.Tthis caching system has no
    limit on the number of items it can store.
    """

    def put(self, key, item):
        """
        Assigns the item value to the key in the cache_data dictionary.
        If key or item is None, it does nothing.
        """
        if key is not None and item is not None:
            self.cache_data[key] = item

    def get(self, key):
        """
        Returns the value linked to key in cache_data.
        If key is None or does not exist, returns None.
        """
        if key is None or key not in self.cache_data:
            return None
        return self.cache_data[key]
