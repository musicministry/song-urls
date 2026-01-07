import re
import PyPDF2

def parse_hymnal_index_robust(pdf_path):
    """
    Parse hymnal index PDF with better handling of multi-line entries.
    """
    
    hymns = {}
    
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        
        for page in pdf_reader.pages:
            text = page.extract_text()
            
            # Remove headers and footers
            text = re.sub(r'Index of First Lines.*?continued', '', text, flags=re.IGNORECASE)
            text = re.sub(r'^\d{3,4}$', '', text, flags=re.MULTILINE)  # Remove page numbers
            
            # Find all entries: number followed by text
            # Pattern matches: " 664 A Celtic Rune"
            pattern = r'\s+(\d+)\s+([^\d\n][^\n]*?)(?=\s+\d+\s+|\Z)'
            
            matches = re.finditer(pattern, text, re.MULTILINE | re.DOTALL)
            
            for match in matches:
                number = int(match.group(1))
                title = match.group(2).strip()
                
                # Clean up title
                # Remove newlines within title
                title = ' '.join(title.split())
                
                # Skip if title looks like a header
                if 'Index' in title or 'continued' in title.lower():
                    continue
                
                hymns[title] = number
    
    return hymns


def save_to_python_file(hymns_dict, output_path='gather.py'):
    """Save hymns dictionary as a Python file."""
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('"""Hymnal Index - Auto-generated"""\n\n')
        f.write('hymns = {\n')
        
        for title, number in sorted(hymns_dict.items(), key=lambda x: x[1]):
            title_escaped = title.replace("'", "\\'")
            f.write(f"    '{title_escaped}': {number},\n")
        
        f.write('}\n\n')
        
        # Add helper function
        f.write('def get_hymn_number(title):\n')
        f.write('    """Get hymn number by title."""\n')
        f.write('    return hymns.get(title)\n\n')
        
        f.write('def search_hymns(search_term):\n')
        f.write('    """Search for hymns by partial title match."""\n')
        f.write('    search_lower = search_term.lower()\n')
        f.write('    return {title: num for title, num in hymns.items() \n')
        f.write('            if search_lower in title.lower()}\n')


if __name__ == '__main__':
    import sys
    
    # Get PDF path from command line or use default
    pdf_path = sys.argv[1] if len(sys.argv) > 1 else '2_G3_Indexes.pdf'
    
    print(f"Parsing {pdf_path}...")
    hymns = parse_hymnal_index_robust(pdf_path)
    
    print(f"✓ Parsed {len(hymns)} hymns")
    
    # Show sample entries
    print("\nSample entries:")
    for title, number in list(hymns.items())[:10]:
        print(f"  {number}: {title}")
    
    # Save to file
    output_path = 'gather.py'
    save_to_python_file(hymns, output_path)
    print(f"\n✓ Saved to {output_path}")
    
    # Test the output
    print("\nTesting import...")
    exec(open(output_path).read())
    print(f"  hymns dictionary has {len(hymns)} entries")
    print(f"  'A Hymn of Glory Let Us Sing!' = {hymns.get('A Hymn of Glory Let Us Sing!')}")