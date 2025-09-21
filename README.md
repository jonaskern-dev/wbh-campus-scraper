# WBH Campus Scraper

Extract and process study program data from WBH Online Campus HTML exports.

## Quick Start

```bash
# 1. Export HTML from WBH Campus:
#    My Studies → Study Programs → [Your Program] (e.g. Computer Science)
#    → Save complete webpage as curriculum.html

# 2. Extract data (after installation)
wbh-scraper curriculum.html

# Or during development
python3 main.py curriculum.html

# With options
wbh-scraper curriculum.html --debug  # Enable debug mode
wbh-scraper curriculum.html -o my_data.json  # Custom output
```

## What Gets Extracted?

A structured JSON file (`data.json`) containing:
- **Study program information** (ID, number, name)
- **All modules** with correct credit points
- **All elements** (study booklets, exams, seminars)
- **All documents** (PDF, EPUB, HTML, MP3, ZIP)
- **Semester assignments** automatically calculated
- **Module hierarchy** preserved

## Features

- **OOP architecture** with clean data models
- **Automatic CP extraction** from exams
- **Document information** for downloads
- **Debug mode** for development
- **Statistics** and analysis
- **Unit tests** for quality assurance

## Project Structure

```
wbh-campus-scraper/
├── scraper/            # Main package
│   ├── models/         # Data models
│   └── scraper.py      # Main class
├── tests/              # Unit tests
├── main.py            # CLI entry point
└── setup.py           # Package setup
```

## How It Works

1. **Scraping**: Extracts JSON data from HTML (`WL.DEBUG.iCurriculumJSON`)
2. **Parsing**: Processes raw data into structured models
3. **Building**: Creates complete study program hierarchy
4. **Export**: Saves as clean JSON with all relationships

## Python API

```python
from scraper import WBHScraper

# Initialize scraper with HTML file
scraper = WBHScraper("curriculum.html")

# Access raw JSON directly (default)
raw_data = scraper.raw_json

# Or get transformed data
study_program = scraper.transform()
print(f"Program: {study_program.study_program.number} {study_program.study_program.name}")
print(f"Total modules: {len(study_program.modules)}")

# Save to file
scraper.save_to_file("output.json")
```

## Installation

```bash
# Via Homebrew
brew tap jonaskern-dev/tap
brew install wbh-campus-scraper

# Via pip from GitHub
pip install git+https://github.com/jonaskern-dev/wbh-campus-scraper.git

# For development
git clone https://github.com/jonaskern-dev/wbh-campus-scraper.git
cd wbh-campus-scraper
pip install -e .

# After installation, the command is available:
wbh-scraper --version

# Run tests
python -m unittest discover tests
```

## License

MIT License

## Author

Jonas Kern - [info@jonaskern.de](mailto:info@jonaskern.de) - [https://jonaskern.dev](https://jonaskern.dev)

---

*Version 0.4.0 - Release*