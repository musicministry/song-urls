"""Respond & Acclaim Index"""

index = {
    "November 30, 2025 - First Sunday of Advent": 4,
    "December 07, 2025 - Second Sunday of Advent": 6,
    "December 08, 2025 - Immaculate Conception of the Blessed Virgin Mary": 8,
    "December 12, 2025 - Our Lady of Guadalupe": 10,
    "December 14, 2025 - Third Sunday of Advent": 12,
    "December 21, 2025 - Fourthth Sunday of Advent": 14,
    "December 24, 2025 - Nativity of the Lord (Christmas): Vigil Mass": 16,
    "December 25, 2025 - Nativity of the Lord (Christmas): Mass during the Night": 18,
    "December 25, 2025 - Nativity of the Lord (Christmas): Mass at Dawn": 20,
    "December 25, 2025 - Nativity of the Lord (Christmas): Mass during the Day": 22,
    "December 28, 2025 - Holy Family of Jesus, Mary and Joseph": 24,
    "January 01, 2026 - Solemnity of Mary, the Holy Mother of God": 26,
    "January 04, 2026 - Epiphany of the Lord": 28,
    "January 11, 2026 - Baptism of the Lord": 30,
    "January 18, 2026 - Second Sunday in Ordinary Time": 32,
    "January 25, 2026 - Third Sunday in Ordinary Time": 34,
    "February 01, 2026 - Fourthth Sunday in Ordinary Time": 36,
    "February 08, 2026 - Fifth Sunday in Ordinary Time": 38,
    "February 15, 2026 - Sixth Sunday in Ordinary Time": 40,
    "February 18, 2026 - Ash Wednesday": 42,
    "February 22, 2026 - First Sunday of Lent": 44,
    "March 01, 2026 - Second Sunday of Lent": 46,
    "March 08, 2026 - Third Sunday of Lent": 48,
    "March 15, 2026 - Fourthth Sunday of Lent": 50,
    "March 22, 2026 - Fifth Sunday of Lent": 52,
    "March 29, 2026 - Palm Sunday of the Passion of the Lord": 54,
    "April 02, 2026 - Thursday of the Lord's Supper (Holy Thursday): Evening Mass": 56,
    "April 03, 2026 - Friday of the Passion of the Lord (Good Friday)": 58,
    "April 04, 2026 - Easter Vigil in the Holy Night": 60,
    "April 05, 2026 - Easter Sunday of the Resurrection of the Lord: Mass during the Day": 72,
    "April 12, 2026 - Second Sunday of Easter (or Sunday of Divine Mercy)": 74,
    "April 19, 2026 - Third Sunday of Easter": 76,
    "April 26, 2026 - Fourthth Sunday of Easter": 78,
    "May 03, 2026 - Fifth Sunday of Easter": 80,
    "May 10, 2026 - Sixth Sunday of Easter": 82,
    "May 14 or May 17, 2026 - Ascension of the Lord": 84,
    "May 17, 2026 - Seventh Sunday of Easter": 86,
    "May 23, 2026 - Pentecost Sunday: Vigil Mass (Extended Form)": 88,
    "May 24, 2026 - Pentecost Sunday: Mass during the Day": 94,
    "May 31, 2026 - Most Holy Trinity": 96,
    "June 07, 2026 - Most Holy Body and Blood of Christ (Corpus Christi)": 98,
    "June 14, 2026 - Eleventh Sunday in Ordinary Time": 100,
    "June 21, 2026 - Twelfth Sunday in Ordinary Time": 102,
    "June 28, 2026 - Thirteenth Sunday in Ordinary Time": 104,
    "July 05, 2026 - Fourteenth Sunday in Ordinary Time": 106,
    "July 12, 2026 - Fifteenth Sunday in Ordinary Time": 108,
    "July 19, 2026 - Sixteenth Sunday in Ordinary Time": 110,
    "July 26, 2026 - Seventeenth Sunday in Ordinary Time": 112,
    "August 02, 2026 - Eighteenth Sunday in Ordinary Time": 114,
    "August 09, 2026 - Nineteenth Sunday in Ordinary Time": 116,
    "August 14, 2026 - Assumption of the Blessed Virgin Mary: Vigil Mass": 118,
    "August 15, 2026 - Assumption of the Blessed Virgin Mary: Mass during the Day": 120,
    "August 16, 2026 - Twentieth Sunday in Ordinary Time": 122,
    "August 23, 2026 - Twenty-First Sunday in Ordinary Time": 124,
    "August 30, 2026 - Twenty-Second Sunday in Ordinary Time": 126,
    "September 06, 2026 - Twenty-Third Sunday in Ordinary Time": 128,
    "September 13, 2026 - Twenty-Fourth Sunday in Ordinary Time": 130,
    "September 20, 2026 - Twenty-Fifth Sunday in Ordinary Time": 132,
    "September 27, 2026 - Twenty-Sixth Sunday in Ordinary Time": 134,
    "October 04, 2026 - Twenty-Seventh Sunday in Ordinary Time": 136,
    "October 11, 2026 - Twenty-Eighth Sunday in Ordinary Time": 138,
    "October 18, 2026 - Twenty-Ninth Sunday in Ordinary Time": 140,
    "October 25, 2026 - Thirtieth Sunday in Ordinary Time": 142,
    "November 01, 2025 - All Saints": 144,
    "November 08, 2025 - Thirty-Second Sunday in Ordinary Time": 146,
    "November 15, 2025 - Thirty-Third Sunday in Ordinary Time": 148,
    "November 22, 2025 - Our Lord Jesus Christ, King of the Universe": 150,
    "November 26, 2025 - Thanksgiving Day": 152,
}

def get_page(date_celebration):
    """Get page number by date and celebration."""
    return index.get(date_celebration)

def search_celebration(search_term):
    """Search for celebrations by partial name match."""
    search_lower = search_term.lower()
    return {k: v for k, v in index.items()
            if search_lower in k.lower()}

def get_page_fuzzy(date_obj, celebration_name, threshold=70):
    """
    Get page number using fuzzy matching on celebration name.
    
    Args:
        date_obj: datetime.date or datetime.datetime object
        celebration_name: Name of the celebration (can be partial or slightly different)
        threshold: Minimum similarity score (0-100, default 70)
    
    Returns:
        tuple: (page_number, matched_key, score) or (None, None, 0) if no match
    
    Example:
        >>> get_page_fuzzy(date(2026, 1, 4), "Epiphany")
        (28, "January 04, 2026 - The Epiphany of the Lord", 100)
    """
    date_str = date_obj.strftime("%B %d, %Y")
    
    # Filter to only entries for this date
    candidates = {k: v for k, v in index.items() if k.startswith(date_str)}
    
    if not candidates:
        return None, None, 0
    
    # If only one entry for this date, return it (common case)
    if len(candidates) == 1:
        key, page = list(candidates.items())[0]
        return page, key, 100
    
    # Multiple entries for this date - use fuzzy matching on celebration part
    # Extract just the celebration names (part after " - ")
    candidate_celebrations = {k: k.split(" - ", 1)[1] for k in candidates.keys()}
    
    # Find best match
    result = process.extractOne(
        celebration_name,
        candidate_celebrations.values(),
        scorer=fuzz.ratio,
        score_cutoff=threshold
    )
    
    if result:
        matched_celebration, score = result[0], result[1]
        
        # Find the original key
        for key, celebration in candidate_celebrations.items():
            if celebration == matched_celebration:
                return candidates[key], key, score
    
    return None, None, 0

def get_page_by_date(date_obj, celebration_substring="", fuzzy=False, threshold=70):
    """
    Get page number using a datetime object.
    
    Args:
        date_obj: datetime.date or datetime.datetime object
        celebration_substring: Substring or full name to match
        fuzzy: If True, use fuzzy matching; if False, use exact substring match
        threshold: Minimum similarity score for fuzzy matching (0-100)
    
    Returns:
        int: Page number, or None if not found
    
    Examples:
        >>> # Exact substring match
        >>> get_page_by_date(date(2026, 1, 4), "Epiphany")
        28
        
        >>> # Fuzzy match (handles typos, variations)
        >>> get_page_by_date(date(2026, 1, 4), "Epifany", fuzzy=True)
        28
    """
    if fuzzy and celebration_substring:
        page, _, _ = get_page_fuzzy(date_obj, celebration_substring, threshold)
        return page
    
    date_str = date_obj.strftime("%B %d, %Y")
    
    if celebration_substring:
        # Search for entries matching this date and celebration
        for key, page in index.items():
            if key.startswith(date_str) and celebration_substring.lower() in key.lower():
                return page
    else:
        # Return first entry for this date
        for key, page in index.items():
            if key.startswith(date_str):
                return page
    
    return None

def get_all_pages_for_date(date_obj):
    """
    Get all entries for a specific date.
    Useful when you need to see all options.
    
    Args:
        date_obj: datetime.date or datetime.datetime object
    
    Returns:
        dict: {celebration_name: page_number}
    
    Example:
        >>> get_all_pages_for_date(date(2025, 12, 25))
        {
            'The Nativity of the Lord (Christmas): At the Mass during the Night': 18,
            'The Nativity of the Lord (Christmas): At the Mass at Dawn': 20,
            'The Nativity of the Lord (Christmas): At the Mass during the Day': 22
        }
    """
    date_str = date_obj.strftime("%B %d, %Y")
    
    results = {}
    for key, page in index.items():
        if key.startswith(date_str):
            celebration = key.split(" - ", 1)[1]
            results[celebration] = page
    
    return results
