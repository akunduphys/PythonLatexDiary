Semi Manual diary in Latex with inputs in command-line-based Python. Old School.


# LaTeX Diary System

A Python-based diary application that creates and manages diary entries using LaTeX for beautiful PDF output. The system organizes entries chronologically and supports rich formatting, emojis, and custom boxes for additional content.

## Features

- **Date-based Entry System**: Create entries for today or any past date
- **Chronological Organization**: Entries are automatically sorted and organized by year and month
- **LaTeX Output**: Beautiful PDF generation with consistent formatting
- **Mood Tracking**: Include emojis to represent your mood/feeling for each entry
- **Flexible Content Boxes**: Add optional content in colored boxes for highlighting important information
- **Entry Appending**: Add content to existing entries for the same date
- **Automatic Compilation**: Automatically generates a complete LaTeX document with all entries

## Requirements

- Python 3.x
- LaTeX distribution (e.g., TeX Live, MiKTeX)
- Required LaTeX packages:
  - lipsum
  - xcolor
  - framed
  - datetime
  - inputenc
  - fontenc
  - fourier
  - marginnote
  - tikz
  - hyperref
  - graphicx

## Installation

1. Clone this repository
2. Ensure you have a LaTeX distribution installed
3. Create an `Emoji` directory with the following emoji images:
   - amazed-smiley
   - beer-smiley
   - coffee-smiley
   - confused-smiley
   - headbang-smiley
   - shutupandcalc
   - code-smiley

## Usage

Run the script:
```bash
python Diary.py
```

Follow the interactive prompts to:
1. Choose the entry date (today or a specific date)
2. Write your main diary entry
3. Add optional content for two colored boxes
4. Select your mood/feeling (using numbers 1-7 or keywords)

## Directory Structure
.
├── YYYY/ # Year folders
│ └── Month_YYYY.tex # Monthly entry files
├── Emoji/ # Emoji images
├── MainFile.tex # Main LaTeX file
├── input.tex # LaTeX input definitions
└── Diary.py # Python script


## Mood Options

1. Amazing, happy, excited (😄)
2. Relaxed, chill (🍺)
3. Tired, sleepy (☕)
4. Confused, unsure (😕)
5. Frustrated, angry (😠)
6. Focused (🧮)
7. Productive, coding (💻)

## Output

The system generates:
- Individual `.tex` files for each month
- A master `MainFile.tex` that includes all entries
- A compiled PDF with all diary entries

## Contributing

Feel free to submit issues and enhancement requests!

## License

akunduphys@gmail.com
