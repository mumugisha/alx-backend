#!/usr/bin/env python3
"""
Find the correct indexes to paginate the dataset correctly and
return the appropriate page of the dataset, with additional metadata.
"""

import csv
import math
from typing import List, Tuple, Optional, Dict


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """
    Calculates the start and end indexes for pagination.

    Parameters:
        page (int): The page number (1-indexed).
        page_size (int): The number of items per page.

    Returns:
        Tuple[int, int]: A tuple containing the start
        and end indexes for pagination.
    """
    start_index = (page - 1) * page_size
    end_index = page * page_size
    return (start_index, end_index)


class Server:
    """Server class to paginate a database of popular baby names."""
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None

    def dataset(self) -> List[List[str]]:
        """Cached dataset"""
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List[str]]:
        """
        Returns a page from the dataset.

        Parameters:
            page (int): The page number (1-indexed).
            page_size (int): The number of items per page.

        Returns:
            List[List[str]]: A list of lists, where each list
                             represents a row in the dataset.
        """
        assert isinstance(page, int) and page > 0
        assert isinstance(page_size, int) and page_size > 0

        dataset = self.dataset()
        start_index, end_index = index_range(page, page_size)

        if start_index >= len(dataset):
            return []

        return dataset[start_index:end_index]

    def get_hyper(
            self,
            page: int = 1,
            page_size: int = 10
    ) -> Dict[str, Optional[int]]:
        """
        Returns a dictionary with pagination information.

        Parameters:
            page (int): The page number (1-indexed).
            page_size (int): The number of items per page.

        Returns:
            Dict[str, Optional[int]]: A dictionary with pagination details.
        """
        data = self.get_page(page, page_size)
        total_numbers_items = len(self.dataset())
        total_pages = math.ceil(total_numbers_items / page_size)

        return {
            "page_size": len(data),
            "page": page,
            "data": data,
            "next_page": page + 1 if page < total_pages else None,
            "prev_page": page - 1 if page > 1 else None,
            "total_pages": total_pages
        }