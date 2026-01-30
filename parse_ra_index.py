import re
import sys
import yaml
import argparse
from numbr import Cast as num
from datetime import datetime
from titlecase import titlecase

def parse_ra_index(year):
    """
    Parse from the provided text content with year assignment.
    
    Args:
        year: The liturgical year (e.g., 2026)
              Dates from Jan 1 onward get this year.
              Dates before Jan 1 get year-1.
    
    Returns:
        dict: {'Month Day, Year - Celebration': page}
    """
    
    text = """
First Sunday of Advent
November 30 4
Second Sunday of Advent
December 7 6
The Immaculate Conception of 
the Blessed Virgin Mary
December 8 8
Our Lady of Guadalupe
December 12 10
Third Sunday of Advent
December 14 12
Fourth Sunday of Advent
December 21 14
The Nativity of the Lord (Christmas): 
At the Vigil Mass
December 24 16
The Nativity of the Lord (Christmas): 
At the Mass during the Night
December 25 18
The Nativity of the Lord (Christmas): 
At the Mass at Dawn
December 25 20
The Nativity of the Lord (Christmas): 
At the Mass during the Day
December 25 22
The Holy Family of Jesus, Mary and Joseph
December 28 24
Solemnity of Mary, the Holy Mother of God
January 1 26
The Epiphany of the Lord
January 4 28
The Baptism of the Lord
January 11 30
Second Sunday in Ordinary Time
January 18 32
Third Sunday in Ordinary Time
January 25 34
Fourth Sunday in Ordinary Time
February 1 36
Fifth Sunday in Ordinary Time
February 8 38
Sixth Sunday in Ordinary Time
February 15 40
Ash Wednesday
February 18 42
First Sunday of Lent
February 22 44
Second Sunday of Lent
March 1 46
Third Sunday of Lent
March 8 48
Fourth Sunday of Lent
March 15 50
Fifth Sunday of Lent
March 22 52
Palm Sunday of the Passion of the Lord
March 29 54
Thursday of the Lord's Supper (Holy Thursday): 
At the Evening Mass
April 2 56
Friday of the Passion of the Lord (Good Friday)
April 3 58
The Easter Vigil in the Holy Night
April 4 60
Easter Sunday of the Resurrection of the Lord: 
At the Mass during the Day
April 5 72
Second Sunday of Easter 
(or Sunday of Divine Mercy)
April 12 74
Third Sunday of Easter
April 19 76
Fourth Sunday of Easter
April 26 78
Fifth Sunday of Easter
May 3 80
Sixth Sunday of Easter
May 10 82
The Ascension of the Lord
May 14 or May 17 84
Seventh Sunday of Easter
May 17 86
Pentecost Sunday: At the Vigil Mass 
(Extended Form)
May 23 88
Pentecost Sunday: At the Mass during the Day
May 24 94
The Most Holy Trinity
May 31 96
The Most Holy Body and Blood of Christ 
(Corpus Christi)
June 7 98
11th Sunday in Ordinary Time
June 14 100
12th Sunday in Ordinary Time
June 21 102
13th Sunday in Ordinary Time
June 28 104
14th Sunday in Ordinary Time
July 5 106
15th Sunday in Ordinary Time
July 12 108
16th Sunday in Ordinary Time
July 19 110
17th Sunday in Ordinary Time
July 26 112
18th Sunday in Ordinary Time
August 2 114
19th Sunday in Ordinary Time
August 9 116
The Assumption of the Blessed Virgin Mary: 
At the Vigil Mass
August 14 118
The Assumption of the Blessed Virgin Mary: 
At the Mass during the Day
August 15 120
20th Sunday in Ordinary Time
August 16 122
21st Sunday in Ordinary Time
August 23 124
22nd Sunday in Ordinary Time
August 30 126
23rd Sunday in Ordinary Time
September 6 128
24th Sunday in Ordinary Time
September 13 130
25th Sunday in Ordinary Time
September 20 132
26th Sunday in Ordinary Time
September 27 134
27th Sunday in Ordinary Time
October 4 136
28th Sunday in Ordinary Time
October 11 138
29th Sunday in Ordinary Time
October 18 140
30th Sunday in Ordinary Time
October 25 142
All Saints
November 1 144
32nd Sunday in Ordinary Time
November 8 146
33rd Sunday in Ordinary Time
November 15 148
Our Lord Jesus Christ, King of the Universe
November 22 150
Thanksgiving Day
November 26 152"""
    
    ra_index = {}
    lines = text.split('\n')
    
    current_celebration = []
    previous_year = year - 1
    
    # Months that should get previous year (liturgical year starts in Advent)
    previous_year_months = ['November', 'December']
    
    for line in lines:
        line = line.strip()
        
        # Skip empty lines and page headers
        if not line or (line.isdigit() and len(line) <= 3):
            continue
        
        # Check if line contains a date and page number
        date_page_match = re.match(
            r'^((?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2}(?:\s+or\s+\w+\s+\d{1,2})?)\s+(\d{1,3})$',
            line
        )
        
        if date_page_match:
            date = date_page_match.group(1)
            page = int(date_page_match.group(2))
            
            # Determine which year to use
            month = date.split()[0]
            if month in previous_year_months:
                date_with_year = f"{date}, {previous_year}"
            else:
                date_with_year = f"{date}, {year}"
            
            # Join accumulated celebration lines
            celebration = ' '.join(current_celebration)

            # Modify key to remove leading 'The' and 'At the'
            if celebration.startswith('The '):
                celebration = celebration[4:]
            celebration = celebration.replace('At the ', '')
            
            # Convert ordinal numbers to words
            try:
                newnum = num(celebration[:4], target='Ordinal Word')
                celebration = titlecase(newnum) + celebration[4:]
            except ValueError:
                pass

            # Create key
            key = f"{date_with_year} - {celebration}"
            ra_index[key] = page
            
            # Reset for next entry
            current_celebration = []
        else:
            # This is part of a celebration name
            current_celebration.append(line)
    
    return ra_index


def save_ra_index(ra_dict, output_path='ra-index'):
    """Save RA index dictionary to Python file."""
    
    # Write to a YAML file
    with open(f'{output_path}.yml', 'w', encoding='utf-8') as f:
        yaml.dump(ra_dict, f)

    # Write to a Python file with helper functions
    with open(f'{output_path}.py', 'w', encoding='utf-8') as f:
        f.write('"""Respond & Acclaim Index"""\n\n')
        f.write('ra_index = {\n')
        
        for key, page in ra_dict.items():
            key_escaped = key.replace('"', '\\"')
            f.write(f'    "{key_escaped}": {page},\n')
        
        f.write('}\n\n')
        
        f.write('def get_page(date_celebration):\n')
        f.write('    """Get page number by date and celebration."""\n')
        f.write('    return ra_index.get(date_celebration)\n\n')
        
        f.write('def search_celebration(search_term):\n')
        f.write('    """Search for celebrations by partial name match."""\n')
        f.write('    search_lower = search_term.lower()\n')
        f.write('    return {k: v for k, v in ra_index.items()\n')
        f.write('            if search_lower in k.lower()}\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Parse Respond & Acclaim index with liturgical year'
    )
    parser.add_argument(
        'year',
        type=int,
        help='Liturgical year (e.g., 2026). November-December get year-1, January onwards get this year.'
    )
    parser.add_argument(
        '-o', '--output',
        default='ra-index',
        help='Output file path (default: ra-index)'
    )
    
    args = parser.parse_args()
    
    print(f"Parsing Respond & Acclaim index for liturgical year {args.year}...")
    print(f"  November-December: {args.year - 1}")
    print(f"  January onwards: {args.year}")
    
    # Parse with year
    ra_dict = parse_ra_index(args.year)
    
    print(f"\n✓ Parsed {len(ra_dict)} entries")
    
    # Show first and last few entries to verify years
    print("\nFirst 3 entries (should be previous year):")
    for i, (key, page) in enumerate(list(ra_dict.items())[:3]):
        print(f"  {i+1}. '{key}': {page}")
    
    print("\nEntries around New Year:")
    items = list(ra_dict.items())
    for key, page in items[12:16]:  # Around December 28 -> January 1
        print(f"  '{key}': {page}")
    
    # Save to file
    save_ra_index(ra_dict, args.output)
    print(f"\n✓ Saved to {args.output}")