#!/usr/bin/env python3
""" BaseCaching module
"""
from base_caching import BaseCaching


class LFUCache(BaseCaching):
    """ LFUCache defines the caching system
    """

    def __init__(self):
        """ Initialize
        """
        super().__init__()
        self.usage = []
        self.leastfrequency = {}

    def put(self, key, item):
        """ Add an item to the cache
        """
        if key is None or item is None:
            return

        length = len(self.cache_data)
        if length >= BaseCaching.MAX_ITEMS and key not in self.cache_data:
            lfu_alg = min(self.leastfrequency.values())
            lfu_alg_keys = []
            for a, b in self.leastfrequency.items():
                if b == lfu_alg:
                    lfu_alg_keys.append(a)

            if len(lfu_alg_keys) > 1:
                lru_lfu_alg = {}
                for a in lfu_alg_keys:
                    lru_lfu_alg[a] = self.usage.index(a)
                discard = min(lru_lfu_alg, key=lru_lfu_alg.get)
            else:
                discard = lfu_alg_keys[0]

            print("DISCARD: {}".format(discard))
            del self.cache_data[discard]
            del self.usage[self.usage.index(discard)]
            del self.leastfrequency[discard]

        if key in self.leastfrequency:
            self.leastfrequency[key] += 1
        else:
            self.leastfrequency[key] = 1

        if key not in self.usage:
            self.usage.append(key)
        self.cache_data[key] = item

    def get(self, key):
        """ Get an item by key.
        """
        if key is not None and key in self.cache_data.keys():
            del self.usage[self.usage.index(key)]
            self.usage.append(key)
            self.leastfrequency[key] += 1
            return self.cache_data[key]
        return None
