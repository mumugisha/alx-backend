#!/usr/bin/env python3
"""
The goal here is that if between two queries, certain
rows are removed from the dataset,
the user does not miss items from dataset when changing page
"""

import csv
from typing import List, Dict


class Server:
    """Server class to paginate a database of popular baby names."""

    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None
        self.__indexed_dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset"""
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]  # Skip header

        return self.__dataset

    def indexed_dataset(self) -> Dict[int, List]:
        """Dataset indexed by sorting position, starting at 0"""
        if self.__indexed_dataset is None:
            dataset = self.dataset()
            self.__indexed_dataset = {
                i: dataset[i] for i in range(len(dataset))
            }
        return self.__indexed_dataset

    def get_hyper_index(self, index: int = None, page_size: int = 10) -> Dict:
        """
        Returns a dictionary with pagination information,
        resilient to deletions.

        Parameters:
            index (int): Starting index for pagination.
            page_size (int): Number of items per page.

        Returns:
            Dict: Contains current index, next index, page size, and page data.
        """
        indexed_dataset = self.indexed_dataset()

        # Validate index within range if provided
        if index is not None:
            assert 0 <= index < len(indexed_dataset), "Index out of range"

        start_index = 0 if index is None else index
        data = []
        current_index = start_index

        # Collect items until reaching page_size or end of dataset
        while len(data) < page_size and current_index < len(indexed_dataset):
            item_lists = indexed_dataset.get(current_index)
            if item_lists:
                data.append(item_lists)
            current_index += 1

        next_index = current_index

        return {
            "index": start_index,
            "next_index": next_index,
            "page_size": len(data),
            "data": data,
        }
