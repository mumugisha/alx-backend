#!/usr/bin/env python3
""" BaseCaching module
"""
from base_caching import BaseCaching


class LFUCache(BaseCaching):
    """ LFUCache defines a caching system with LFU algorithm
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

        if (len(self.cache_data) >= BaseCaching.MAX_ITEMS
                and key not in self.cache_data):
            lfu_alg = min(self.leastfrequency.values())
            lfu_alg_keys = [
                k for k, v in self.leastfrequency.items()
                if v == lfu_alg
            ]

            if len(lfu_alg_keys) > 1:
                lru_lfu = {
                    k: self.usage.index(k)
                    for k in lfu_alg_keys
                }
                discard = min(lru_lfu, key=lru_lfu.get)
            else:
                discard = lfu_alg_keys[0]

            print("DISCARD: {}".format(discard))
            del self.cache_data[discard]
            self.usage.remove(discard)
            del self.leastfrequency[discard]

        self.cache_data[key] = item
        self.leastfrequency[key] = self.leastfrequency.get(key, 0) + 1
        if key in self.usage:
            self.usage.remove(key)
        self.usage.append(key)

    def get(self, key):
        """ Get an item by key.
        """
        if key is not None and key in self.cache_data:
            self.usage.remove(key)
            self.usage.append(key)
            self.leastfrequency[key] += 1
            return self.cache_data[key]
        return None
