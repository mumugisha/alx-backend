#!/usr/bin/env python3
"""
Defines the function `index_range`, which calculates the start
and end indexes for pagination given a page and page_size.
"""

from typing import tuple


def index_range(page: int, page_size: int) -> tuple[int, int]:
    """
    Calculates the start and end indexes for pagination.

    """
    start_index = (page - 1) * page_size
    end_index = page + page_size
    return (start_index, end_index)
