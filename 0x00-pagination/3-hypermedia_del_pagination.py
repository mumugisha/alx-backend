#!/usr/bin/env python3
"""
Deletion-resilient hypermedia pagination
"""

import csv
from typing import List, Dict, Any, Optional


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None
        self.__indexed_dataset = None

    def dataset(self) -> List[List[str]]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def indexed_dataset(self) -> Dict[int, List[str]]:
        """Dataset indexed by sorting position, starting at 0
        """
        if self.__indexed_dataset is None:
            dataset = self.dataset()
            truncated_dataset = dataset[:1000]
            self.__indexed_dataset = {
                i: truncated_dataset[i]
                for i in range(len(truncated_dataset))
            }
        return self.__indexed_dataset

    def get_hyper_index(
        self,
        index: Optional[int] = None,
        page_size: int = 10
    ) -> Dict[str, Any]:
        """
        Provides a deletion-resilient pagination response.

        Parameters:
            index (Optional[int]): The starting index for pagination.
                                   Defaults to None, which is treated as 0.
            page_size (int): The number of items to include in the page.

        Returns:
            Dict[str, Any]: A dictionary containing the current index,
                            next index, page size, and page data.
        """
        dataset = self.indexed_dataset()
        total_items = len(dataset)

        # Default to 0 if index is None
        if index is None:
            index = 0

        # Assert that index is within the valid range of the dataset
        assert 0 <= index < total_items, (
            f"Index {index} is out of range."
        )

        data = []
        current_index = index

        # Collect `page_size` items while skipping missing rows
        while len(data) < page_size and current_index < total_items:
            item = dataset.get(current_index)
            if item:
                data.append(item)
            current_index += 1

        # Return the pagination information
        return {
            "index": index,
            "next_index": (
                current_index if current_index < total_items else None
            ),
            "page_size": len(data),
            "data": data
        }


if __name__ == "__main__":
    server = Server()
    print(server.get_hyper_index(0, 10))
