#!/usr/bin/env python3
""" BaseCaching module
"""
from base_caching import BaseCaching


class LIFOCache(BaseCaching):
    """ LIFO Cache defines the caching system
    """

    def __init__(self):
        """ Initialize
        """
        super().__init__()

    def put(self, key, item):
        """ Add an item to the cache
        Args:
            key: The key to add.
            item: The item to add.
        """
        if key is None or item is None:
            return

        self.cache_data[key] = item

        if len(self.cache_data) > BaseCaching.MAX_ITEMS:
            # Get the last key inserted (LIFO)
            last_key = list(self.cache_data.keys())[-1]
            print("DISCARD: {}".format(last_key))
            del self.cache_data[last_key]

    def get(self, key):
        """ Get an item by key
        Args:
            key: The key to look up.
        Returns:
            The value associated with the key, or None if not found.
        """
        if key is None or key not in self.cache_data:
            return None
        return self.cache_data[key]

    def print_cache(self):
        """ Print the current cache data
        """
        print("Current cache:")
        for key in self.cache_data:
            print("{}: {}".format(key, self.cache_data[key]))
