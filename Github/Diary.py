from datetime import datetime
import os
import sys
import re

def get_multiline_input(prompt):
    """
    Get multiline input from user until empty line is entered.
    
    Args:
        prompt (str): Prompt message to display
        
    Returns:
        str: Combined multiline input
    """
    print(prompt)
    lines = []
    while True:
        try:
            line = input()
            if line == "":
                break
            lines.append(line)
        except EOFError:
            break
    return "\n".join(lines)

def get_date_input():
    """
    Get and validate date input from user.
    Returns datetime object for the entry date.
    """
    while True:
        is_today = input("Is this entry for today? (y/n): ").strip().lower()
        if is_today in ['y', 'yes']:
            return datetime.now()
        elif is_today in ['n', 'no']:
            while True:
                try:
                    date_str = input("Enter date (dd/mm/yy): ").strip()
                    # Parse the date string
                    entry_date = datetime.strptime(date_str, '%d/%m/%y')
                    # Check if date is not in future
                    if entry_date > datetime.now():
                        print("Error: Cannot enter future date")
                        continue
                    return entry_date
                except ValueError:
                    print("Error: Invalid date format. Please use dd/mm/yy")
        else:
            print("Please answer 'y' or 'n'")

def format_latex_diary(entry_content, mini_page_content, box_content, entry_date, emoji="emoheadbang"):
    """
    Format content into a LaTeX diary entry using specified date.
    
    Args:
        entry_content (str): Main diary entry text
        mini_page_content (str): Content for first colored box (optional)
        box_content (str): Content for second colored box (optional)
        entry_date (datetime): Date of the entry
        emoji (str): Emoji command for the box (default: emoheadbang)
        
    Returns:
        str: Formatted LaTeX content
        
    Raises:
        ValueError: If main entry content is empty
    """
    if not entry_content:
        raise ValueError("Main diary entry cannot be empty")
    
    # Get day name and date components
    day_name = entry_date.strftime('%A')
    date_display = entry_date.strftime('%d/%m/%y')
    month_year = entry_date.strftime('%Y %B')
    
    # Start with the header and main content
    latex_template = f"""% {date_display} - {month_year} Notes

\\begin{{diary}}{{{day_name}}}{{{date_display}}}
    \\mybox{{\\{emoji}}}
{entry_content}
"""
    
    # Add boxes only if they have content
    if mini_page_content or box_content:
        latex_template += "\n"  # Add spacing before boxes
        
        if mini_page_content and box_content:
            # Both boxes have content
            latex_template += f"""\\noindent\\fcolorbox{{red}}{{yellow}}{{%
    \\minipage[t]{{\\dimexpr0.48\\linewidth-2\\fboxsep-2\\fboxrule\\relax}}
    {mini_page_content}
    \\endminipage}}\\hfill
\\fcolorbox{{red}}{{yellow}}{{%
    \\minipage[t]{{\\dimexpr0.48\\linewidth-2\\fboxsep-2\\fboxrule\\relax}}
    {box_content}
    \\endminipage}}"""
        elif mini_page_content:
            # Only first box has content
            latex_template += f"""\\noindent\\fcolorbox{{red}}{{yellow}}{{%
    \\minipage[t]{{\\dimexpr0.98\\linewidth-2\\fboxsep-2\\fboxrule\\relax}}
    {mini_page_content}
    \\endminipage}}"""
        elif box_content:
            # Only second box has content
            latex_template += f"""\\noindent\\fcolorbox{{red}}{{yellow}}{{%
    \\minipage[t]{{\\dimexpr0.98\\linewidth-2\\fboxsep-2\\fboxrule\\relax}}
    {box_content}
    \\endminipage}}"""
    
    # Add closing tag
    latex_template += "\n\\end{diary}\n"
    
    return latex_template

def extract_date_from_entry(entry):
    """
    Extract date from a LaTeX diary entry.
    
    Args:
        entry (str): LaTeX diary entry content
        
    Returns:
        datetime: Entry date or None if not found
    """
    try:
        # Look for date in the format dd/mm/yy
        date_match = re.search(r'\\begin{diary}{[^}]+}{(\d{2}/\d{2}/\d{2})}', entry)
        if date_match:
            return datetime.strptime(date_match.group(1), '%d/%m/%y')
    except:
        pass
    return None

def create_main_file():
    """
    Create a new MainFile.tex with user-specified title and author.
    Called when MainFile.tex doesn't exist.
    """
    print("\nNo existing diary found. Let's create a new one!")
    title = input("Enter the title for your diary: ").strip()
    author = input("Enter your name (author): ").strip()
    
    latex_content = f"""\\documentclass[a4paper]{{book}}
\\usepackage{{lipsum}}
\\usepackage{{xcolor}}
\\usepackage{{framed}}
\\usepackage{{datetime}}
\\usepackage[utf8]{{inputenc}}
\\usepackage[T1]{{fontenc}}
\\usepackage{{fourier}}
\\usepackage{{marginnote}}
\\usepackage{{tikz}}
\\usepackage{{hyperref}}
\\usepackage{{graphicx}}

\\input{{input}}

\\newcommand{{\\emoamazed}}{{\\includegraphics[height=1.8ex]{{"./Emoji/amazed-smiley"}}}}
\\newcommand{{\\emobeer}}{{\\includegraphics[height=1.8ex]{{"./Emoji/beer-smiley"}}}}
\\newcommand{{\\emocoffee}}{{\\includegraphics[height=1.8ex]{{"./Emoji/coffee-smiley"}}}}
\\newcommand{{\\emoconfused}}{{\\includegraphics[height=1.8ex]{{"./Emoji/confused-smiley"}}}}
\\newcommand{{\\emoheadbang}}{{\\includegraphics[height=1.8ex]{{"./Emoji/headbang-smiley"}}}}
\\newcommand{{\\emoshutcalc}}{{\\includegraphics[height=1.8ex]{{"./Emoji/shutupandcalc"}}}}
\\newcommand{{\\emocode}}{{\\includegraphics[height=1.8ex]{{"./Emoji/code-smiley"}}}}
\\newcommand{{\\datestampcust}}[3]{{\\dayofweekname{{#1}}{{#2}}{{#3}} {{#1.#2.#3}}}}
\\newcommand{{\\sep}}{{-----------------------------------------------------------}}

\\title{{\\Huge {title}}}
\\author{{{author}}}
\\date{{}}

\\begin{{document}}
\\maketitle

\\end{{document}}
"""
    
    try:
        # Create Emoji directory if it doesn't exist
        os.makedirs('Emoji', exist_ok=True)
        
        # Write MainFile.tex
        with open('MainFile.tex', 'w', encoding='utf-8') as f:
            f.write(latex_content)
            
        print("\nCreated new diary:")
        print(f"Title: {title}")
        print(f"Author: {author}")
        print("\nNote: Please ensure you have the required emoji images in the Emoji/ directory:")
        print("- amazed-smiley")
        print("- beer-smiley")
        print("- coffee-smiley")
        print("- confused-smiley")
        print("- headbang-smiley")
        print("- shutupandcalc")
        print("- code-smiley")
        
    except Exception as e:
        print(f"Error creating MainFile.tex: {e}", file=sys.stderr)
        raise

def update_main_file():
    """
    Update MainFile.tex with all year folders and month files in chronological order.
    Creates a complete LaTeX document that can be compiled.
    """
    try:
        # Check if MainFile.tex exists, if not create it
        if not os.path.exists('MainFile.tex'):
            create_main_file()
            return
            
        # Read existing title and author if file exists
        with open('MainFile.tex', 'r', encoding='utf-8') as f:
            content = f.read()
            title_match = re.search(r'\\title{\\Huge ([^}]+)}', content)
            author_match = re.search(r'\\author{([^}]+)}', content)
            title = title_match.group(1) if title_match else "My Diary"
            author = author_match.group(1) if author_match else "Anonymous"

        # Month name to number mapping
        month_to_num = {
            'January': 1, 'Jan': 1,
            'February': 2, 'Feb': 2,
            'March': 3, 'Mar': 3,
            'April': 4, 'Apr': 4,
            'May': 5,
            'June': 6, 'Jun': 6,
            'July': 7, 'Jul': 7,
            'August': 8, 'Aug': 8,
            'September': 9, 'Sep': 9,
            'October': 10, 'Oct': 10,
            'November': 11, 'Nov': 11,
            'December': 12, 'Dec': 12
        }
        
        # Get all year folders
        years = [d for d in os.listdir('.') if os.path.isdir(d) and d.isdigit()]
        years.sort()  # Sort years numerically
        
        includes = []
        
        # For each year, get all month files
        for year in years:
            month_files = [f for f in os.listdir(year) if f.endswith('_' + year + '.tex')]
            # Sort month files by month number
            month_files.sort(key=lambda x: month_to_num[x.split('_')[0]])
            
            # Add include statements for each month file
            for month_file in month_files:
                includes.append(f"\\include{{{'./' + year + '/' + month_file.replace('.tex', '')}}}")
        
        # Create complete LaTeX document
        latex_content = f"""\\documentclass[a4paper]{{book}}
\\usepackage{{lipsum}}
\\usepackage{{xcolor}}
\\usepackage{{framed}}
\\usepackage{{datetime}}
\\usepackage[utf8]{{inputenc}}
\\usepackage[T1]{{fontenc}}
\\usepackage{{fourier}}
\\usepackage{{marginnote}}
\\usepackage{{tikz}}
\\usepackage{{hyperref}}
\\usepackage{{graphicx}}

\\input{{input}}

\\newcommand{{\\emoamazed}}{{\\includegraphics[height=1.8ex]{{"./Emoji/amazed-smiley"}}}}
\\newcommand{{\\emobeer}}{{\\includegraphics[height=1.8ex]{{"./Emoji/beer-smiley"}}}}
\\newcommand{{\\emocoffee}}{{\\includegraphics[height=1.8ex]{{"./Emoji/coffee-smiley"}}}}
\\newcommand{{\\emoconfused}}{{\\includegraphics[height=1.8ex]{{"./Emoji/confused-smiley"}}}}
\\newcommand{{\\emoheadbang}}{{\\includegraphics[height=1.8ex]{{"./Emoji/headbang-smiley"}}}}
\\newcommand{{\\emoshutcalc}}{{\\includegraphics[height=1.8ex]{{"./Emoji/shutupandcalc"}}}}
\\newcommand{{\\emocode}}{{\\includegraphics[height=1.8ex]{{"./Emoji/code-smiley"}}}}
\\newcommand{{\\datestampcust}}[3]{{\\dayofweekname{{#1}}{{#2}}{{#3}} {{#1.#2.#3}}}}
\\newcommand{{\\sep}}{{-----------------------------------------------------------}}

\\title{{\\Huge {title}}}
\\author{{{author}}}
\\date{{}}

\\begin{{document}}
\\maketitle

{chr(10).join(includes)}

\\end{{document}}
"""
        
        # Write to MainFile.tex
        with open('MainFile.tex', 'w', encoding='utf-8') as f:
            f.write(latex_content)
            
    except Exception as e:
        print(f"Error updating MainFile.tex: {e}", file=sys.stderr)

def compile_latex():
    """
    Compile MainFile.tex using pdflatex.
    Runs pdflatex twice to ensure proper cross-references and table of contents.
    """
    try:
        # Run pdflatex twice to ensure proper cross-references
        os.system('pdflatex MainFile.tex')
        os.system('pdflatex MainFile.tex')
        print("\nLaTeX compilation completed successfully.")
    except Exception as e:
        print(f"Error during LaTeX compilation: {e}", file=sys.stderr)

def save_latex_file(content, entry_date):
    """
    Save LaTeX content to a file in date-based folder structure.
    Format: YYYY/Month_YYYY.tex (e.g., 2025/March_2025.tex)
    Creates separate entries for the same date.
    """
    year = entry_date.strftime('%Y')
    month = entry_date.strftime('%B')  # Full month name
    file_name = f"{month}_{year}.tex"
    
    try:
        # Create year folder if not exists
        os.makedirs(year, exist_ok=True)
        file_path = os.path.join(year, file_name)
        
        entries = []
        
        # If file exists, read existing entries
        if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
            with open(file_path, 'r', encoding='utf-8') as f:
                existing_content = f.read()
                # Split on \end{diary} to ensure complete entries
                raw_entries = existing_content.split('\\end{diary}')
                for entry in raw_entries:
                    entry = entry.strip()
                    if entry and '\\begin{diary}' in entry:
                        # Add back the closing tag for each valid entry
                        entries.append(f"{entry}\n\\end{{diary}}")
        
        # Add the new content only if it's not already in entries
        if content.strip() not in [e.strip() for e in entries]:
            entries.append(content.strip())
        
        # Sort entries by date in ascending order
        entries.sort(key=lambda x: extract_date_from_entry(x) or datetime.max, reverse=False)
        
        # Write all entries back to file with proper spacing
        with open(file_path, 'w', encoding='utf-8') as f:
            for i, entry in enumerate(entries):
                if i > 0:  # Add double newline between entries
                    f.write('\n\n')
                f.write(entry.strip())
        
        # Update MainFile.tex after adding new entry
        update_main_file()
        
        return file_path
    except OSError as e:
        print(f"Error saving file: {e}", file=sys.stderr)
        raise

def get_emoji_for_feeling(feeling):
    """
    Map feeling to an appropriate emoji command.
    
    Args:
        feeling (str): User's feeling input or number
        
    Returns:
        str: LaTeX emoji command
    """
    # Map feelings to emojis
    feeling_map = {
        'amazing': 'emoamazed',
        'happy': 'emoamazed',
        'excited': 'emoamazed',
        'relaxed': 'emobeer',
        'chill': 'emobeer',
        'tired': 'emocoffee',
        'sleepy': 'emocoffee',
        'confused': 'emoconfused',
        'unsure': 'emoconfused',
        'frustrated': 'emoheadbang',
        'angry': 'emoheadbang',
        'focused': 'emoshutcalc',
        'productive': 'emocode',
        'coding': 'emocode'
    }
    
    # Map numbers to emojis
    number_map = {
        '1': 'emoamazed',  # amazing, happy, excited
        '2': 'emobeer',    # relaxed, chill
        '3': 'emocoffee',  # tired, sleepy
        '4': 'emoconfused',# confused, unsure
        '5': 'emoheadbang',# frustrated, angry
        '6': 'emoshutcalc',# focused
        '7': 'emocode'     # productive, coding
    }
    
    # Check if input is a number
    if feeling in number_map:
        return number_map[feeling]
    
    # Convert to lowercase for case-insensitive matching
    feeling = feeling.lower()
    
    # Find matching emoji
    for key in feeling_map:
        if key in feeling:
            return feeling_map[key]
    return 'emoheadbang'

def print_mood_options():
    """Print available mood options with both descriptions and single words."""
    print("\nHow are you feeling today?")
    print("\nEnter a number or keyword:")
    print("""
    1. amazing, happy, excited     → 😄
    2. relaxed, chill             → 🍺
    3. tired, sleepy              → ☕
    4. confused, unsure           → 😕
    5. frustrated, angry          → 😠
    6. focused                    → 🧮
    7. productive, coding         → 💻
    """)
    print("You can either:")
    print("  - Enter a number (1-7)")
    print("  - Type a keyword (e.g., 'happy', 'tired', 'coding')")
    print("  - Describe your mood in your own words")

def open_pdf():
    """
    Open the compiled PDF file using the default PDF viewer.
    Uses appropriate command based on the operating system.
    """
    try:
        import platform
        system = platform.system().lower()
        
        if system == 'darwin':  # macOS
            os.system('open MainFile.pdf')
        elif system == 'windows':
            os.system('start MainFile.pdf')
        elif system == 'linux':
            os.system('xdg-open MainFile.pdf')
        else:
            print("Could not automatically open PDF. Please open MainFile.pdf manually.")
            
    except Exception as e:
        print(f"Error opening PDF: {e}", file=sys.stderr)

def main():
    """Main function to handle diary entry creation."""
    try:
        # Ensure MainFile.tex exists
        if not os.path.exists('MainFile.tex'):
            create_main_file()
        
        # Get entry date
        entry_date = get_date_input()
        
        # Get user input
        entry_content = get_multiline_input("Enter your diary entry (press Enter twice to finish):")
        mini_content = input("Enter content for the first box: ").strip()
        box_content = input("Enter content for the second box: ").strip()
        
        # Show mood options and get feeling
        print_mood_options()
        feeling = input("\nYour mood (1-7 or keyword): ").strip()
        emoji = get_emoji_for_feeling(feeling)
        
        # Generate LaTeX with specified date
        latex_output = format_latex_diary(
            entry_content,
            mini_content,
            box_content,
            entry_date,
            emoji
        )
        
        # Print the result
        print("\nGenerated LaTeX:")
        print(latex_output)
        
        # Save to file
        file_path = save_latex_file(latex_output, entry_date)
        print(f"\nOutput saved to '{file_path}'")
        
        # Compile the LaTeX file
        compile_latex()
        
        # Open the compiled PDF
        open_pdf()
        
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
