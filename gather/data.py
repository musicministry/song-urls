"""Hymnal Index - Auto-generated"""

hymns = {
    'A Celtic Rune': 664,
    'A Hymn of Glory Let Us Sing!': 545,
    # ... all your hymns
}

def get_hymn_number(title):
    """Get hymn number by title."""
    return hymns.get(title)

def search_hymns(search_term):
    """Search for hymns by partial title match."""
    search_lower = search_term.lower()
    return {title: num for title, num in hymns.items() 
            if search_lower in title.lower()}