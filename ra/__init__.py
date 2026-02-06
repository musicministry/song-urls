"""Respond & Acclaim Index Data Package"""

from .data import index, get_page, search_celebration, get_page_fuzzy, get_page_by_date, get_all_pages_for_date

__all__ = ['index', 'get_page', 'search_celebration', 'get_page_fuzzy', 'get_page_by_date', 'get_all_pages_for_date']
__version__ = '0.1.0'