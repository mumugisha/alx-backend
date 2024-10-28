#!/usr/bin/env python3
"""
A module for paginating a dataset with considerations
for potential row deletions between pagination queries,
ensuring the user does not miss any items.
"""
import csv
from typing import List, Dict, Any


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

    def get_hyper_index(
        self,
        index: int = 0,
        page_size: int = 10
    ) -> Dict[str, Any]:
        """
        Returns a dictionary with pagination information,
        accounting for deletions.

        Parameters:
            index (int): The starting index for pagination.
            page_size (int): The number of items to include in the page.

        Returns:
            Dict[str, Any]: Pagination information including
            current and next index.
        """
        dataset = self.indexed_dataset()
        total_items = len(dataset)

        # Ensure the index is within the valid range
        assert 0 <= index < total_items, "Index is out of range"

        data = []
        received = {"index": index}
        current_index = index

        # Collect items until reaching page_size or end of dataset
        while len(data) < page_size and current_index < total_items:
            item = dataset.get(current_index)
            if item:
                data.append(item)
            current_index += 1

        received["data"] = data
        received["page_size"] = len(data)
        received["next_index"] = (
            current_index if current_index < total_items else None
        )

        return received


if __name__ == "__main__":
    server = Server()
    print(server.get_hyper_index(0, 10))
