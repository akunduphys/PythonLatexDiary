from datetime import datetime
import os
import sys
import re

def search_entries_by_date(search_date=None):
    """
    Search and display diary entries by date.
    
    Args:
        search_date (str, optional): Date to search for in dd/mm/yy format.
                                   If None, prompts for input.
    """
    try:
        if search_date is None:
            while True:
                date_input = input("Enter date to search (dd/mm/yy) or 'today': ").strip().lower()
                if date_input == 'today':
                    search_date = datetime.now().strftime('%d/%m/%y')
                    break
                try:
                    # Validate date format
                    datetime.strptime(date_input, '%d/%m/%y')
                    search_date = date_input
                    break
                except ValueError:
                    print("Invalid date format. Please use dd/mm/yy")
        
        # Get year from search date
        year = '20' + search_date[-2:]
        found_entries = []
        
        # Check if year folder exists
        if not os.path.exists(year):
            print(f"\nNo entries found for {search_date}")
            return
        
        # Search through all month files in the year
        month_files = [f for f in os.listdir(year) if f.endswith('.tex')]
        for month_file in month_files:
            file_path = os.path.join(year, month_file)
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Split into individual entries
                    entries = [entry.strip() for entry in content.split('\n\n') if entry.strip()]
                    
                    for entry in entries:
                        date_match = re.search(r'\\begin{diary}{([^}]+)}{(\d{2}/\d{2}/\d{2})}', entry)
                        if date_match and date_match.group(2) == search_date:
                            # Extract emoji
                            emoji_match = re.search(r'\\mybox{\\(emo[^}]+)}', entry)
                            emoji = {
                                'emoamazed': '😄',
                                'emobeer': '🍺',
                                'emocoffee': '☕',
                                'emoconfused': '😕',
                                'emoheadbang': '😠',
                                'emoshutcalc': '🧮',
                                'emocode': '💻'
                            }.get(emoji_match.group(1) if emoji_match else 'emoheadbang', '😠')
                            
                            # Extract content
                            content_match = re.search(r'\\mybox{[^}]+}\s*(.*?)(?:\\noindent\\fcolorbox|\\end{diary})', entry, re.DOTALL)
                            main_content = content_match.group(1).strip() if content_match else ""
                            
                            # Extract box contents
                            box_pattern = r'\\minipage[^{]*{[^}]+}(.*?)\\endminipage'
                            boxes = re.findall(box_pattern, entry, re.DOTALL)
                            
                            found_entries.append({
                                'day': date_match.group(1),
                                'content': main_content,
                                'emoji': emoji,
                                'boxes': boxes
                            })
                            
            except Exception as e:
                print(f"Error reading {file_path}: {e}")
        
        if found_entries:
            print(f"\nEntries for {search_date}:")
            print("=" * 60)
            
            for i, entry in enumerate(found_entries, 1):
                if len(found_entries) > 1:
                    print(f"\nEntry #{i}")
                    print("-" * 60)
                
                print(f"Date: {search_date}")
                print(f"Day: {entry['day']}")
                print(f"Mood: {entry['emoji']}")
                print("\nContent:")
                print("-" * 60)
                print(entry['content'].strip())
                
                if entry['boxes']:
                    print("\nAdditional Notes:")
                    print("-" * 60)
                    for j, box in enumerate(entry['boxes'], 1):
                        print(f"Note {j}:")
                        print(box.strip())
                        if j < len(entry['boxes']):
                            print("-" * 30)
                
                print("=" * 60)
        else:
            print(f"\nNo entries found for {search_date}")
            
    except Exception as e:
        print(f"Error searching entries: {e}")

def main():
    """Main function to search diary entries."""
    print("\nDiary Entry Search")
    print("=" * 60)
    
    while True:
        search_entries_by_date()
        
        again = input("\nSearch another date? (y/n): ").strip().lower()
        if again not in ['y', 'yes']:
            break
    
    print("\nGoodbye!")

if __name__ == "__main__":
    sys.exit(main())