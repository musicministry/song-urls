# =========================================================================== #
# parse_gather_index_pdf.py
#
# This script, created by claude.ai, parses the original Gather index in PDF
# format to create a Python dictionary with the song name as the key and the
# number as the value. This dictionary is written to file `gather.py` along
# with some utility functions for querying the dictionary.
#
# This script was mostly successful, but parsing PDF files is tricky and, so
# the output was imperfect. Entry order is preserved to facilitate manual
# review and correction. Use of `gather_index_txt.py`, which had a much higher
# success rate, is recommended instead of this script.
# 
# =========================================================================== #

import re
import PyPDF2
from collections import OrderedDict

def parse_hymnal_index_preserve_order(pdf_path):
    """
    Parse hymnal index PDF and preserve original order.
    Returns OrderedDict to maintain sequence.
    """
    
    # Use OrderedDict to preserve insertion order
    hymns = OrderedDict()
    
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        
        for page_num, page in enumerate(pdf_reader.pages):
            text = page.extract_text()
            
            # Split into lines
            lines = text.split('\n')
            
            for line in lines:
                # Skip headers and page numbers
                if ('Index of First Lines' in line or 
                    'continued' in line.lower() or
                    'Acknowledgements' in line):
                    continue
                
                # Skip if line is just a number (page number)
                if line.strip().isdigit() and len(line.strip()) <= 4:
                    continue
                
                # Skip empty lines
                if not line.strip():
                    continue
                
                # Pattern: number followed by title
                match = re.match(r'^\s*(\d+)\s+(.+)$', line.strip())
                
                if match:
                    number = int(match.group(1))
                    title = match.group(2).strip()
                    
                    # Store in order encountered
                    hymns[title] = number
    
    return hymns


def save_to_file_preserve_order(hymns_dict, output_path='hymns_data.py'):
    """
    Save hymns dictionary to Python file in original order.
    Adds line numbers as comments for easy manual correction.
    """
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('"""Hymnal Index - Auto-generated"""\n')
        f.write('# Entries are in the same order as the original PDF\n')
        f.write('# Line numbers added as comments for manual correction\n\n')
        f.write('hymns = {\n')
        
        for i, (title, number) in enumerate(hymns_dict.items(), start=1):
            # Escape quotes in titles
            title_escaped = title.replace("'", "\\'")
            # Add line number as comment
            f.write(f"    '{title_escaped}': {number},  # Line {i}\n")
        
        f.write('}\n\n')
        
        # Add helper functions
        f.write('def get_hymn_number(title):\n')
        f.write('    """Get hymn number by title."""\n')
        f.write('    return hymns.get(title)\n\n')
        
        f.write('def search_hymns(search_term):\n')
        f.write('    """Search for hymns by partial title match."""\n')
        f.write('    search_lower = search_term.lower()\n')
        f.write('    return {title: num for title, num in hymns.items() \n')
        f.write('            if search_lower in title.lower()}\n')


if __name__ == '__main__':
    pdf_path = 'gather3_index.pdf'
    
    print(f"Parsing {pdf_path}...")
    hymns = parse_hymnal_index_preserve_order(pdf_path)
    
    print(f"✓ Parsed {len(hymns)} hymns")
    
    # Save to file in original order
    output_path = 'gather.py'
    save_to_file_preserve_order(hymns, output_path)
    print(f"✓ Saved to {output_path} (in original order)")
    
    print("\nFirst 10 entries:")
    for i, (title, number) in enumerate(list(hymns.items())[:10], 1):
        print(f"  {i}. {number}: {title}")