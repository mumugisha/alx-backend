#!/usr/bin/env python3
"""
Pagination that handles deletions from the dataset dynamically, allowing
seamless transitions between pages even when rows are removed.
"""

import csv
from typing import List, Dict, Optional, Tuple


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """
    Calculate start and end indexes based on page number and page size.

    Parameters:
        page (int): Page number (1-indexed).
        page_size (int): Number of items per page.

    Returns:
        Tuple[int, int]: Start and end indexes for pagination.
    """
    start_index = (page - 1) * page_size
    end_index = page * page_size
    return start_index, end_index


class Server:
    """Server class to paginate a dataset of
    popular baby names, accounting for deletions."""

    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None
        self.__indexed_dataset = None

    def dataset(self) -> List[List[str]]:
        """Load and cache dataset."""
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]  # Exclude header
        return self.__dataset

    def indexed_dataset(self) -> Dict[int, List[str]]:
        """
        Create an indexed version of the dataset where keys are row indices.

        Returns:
            Dict[int, List[str]]: A dictionary with original index as the key
            and data row as the value.
        """
        if self.__indexed_dataset is None:
            dataset = self.dataset()
            self.__indexed_dataset = {
                i: dataset[i] for i in range(len(dataset))
            }
        return self.__indexed_dataset

    def get_hyper_index(
        self, index: int = 0, page_size: int = 10
    ) -> Dict[str, Optional[int]]:
        """
        Returns a dictionary of paginated data, accounting for deletions
        in dataset.

        Parameters:
            index (int): Starting index for the page.
            page_size (int): Number of items per page.

        Returns:
            Dict[str, Optional[int]]: Paginated data with metadata.
        """
        indexed_data = self.indexed_dataset()
        total_items = len(indexed_data)

        # Adjust the index if it's out of range
        if index >= total_items or index < 0:
            return {
                "index": index,
                "next_index": None,
                "page_size": page_size,
                "data": []
            }

        data = []
        collected_data = 0
        keys = sorted(indexed_data.keys())
        next_index = index

        # Collect items while skipping deleted entries
        while collected_data < page_size and next_index < len(keys):
            item = indexed_data[keys[next_index]]
            if item:
                data.append(item)
                collected_data += 1
            next_index += 1

        return {
            "index": index,
            "next_index": keys[next_index] if next_index < len(keys) else None,
            "page_size": page_size,
            "data": data
        }


if __name__ == "__main__":
    server = Server()
    print(server.get_hyper_index(0, 10))
