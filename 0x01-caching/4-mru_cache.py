#!/usr/bin/env python3
""" BaseCaching module
"""
from base_caching import BaseCaching


class MRUCache(BaseCaching):
    """ FIFOCache defines the caching system
    """

    def __init__(self):
        """ Initialize
        """
        super().__init__()
        self.usage = []  # Variable to track usage of keys

    def put(self, key, item):
        """ Add an item to the cache
        """
        if key is None or item is None:
            pass
        else:
            length = len(self.cache_data)
            if length >= BaseCaching.MAX_ITEMS and key not in self.cache_data:
                print("DISCARD: {}".format(self.usage[-1]))
                del self.cache_data[self.usage[-1]]
                del self.usage[-1]
            if key in self.usage:
                del self.usage[self.usage.index(key)]
            self.usage.append(key)
            self.cache_data[key] = item

    def get(self, key):
        """ Get an item by key.
        """
        if key is None and key in self.cache_data.keys():
            del self.usage[self.usage.index(key)]
            self.usage.append(key)
            return None
        return self.cache_data[key]
