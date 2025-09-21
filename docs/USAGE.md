# Usage Guide

## Getting the HTML File

### Step 1: Access WBH Online Campus
1. Log in to your WBH Online Campus account
2. Navigate to: **Mein Studium** → **Studiengänge**
3. Select your current study program (e.g., "Informatik (Bachelor)")

### Step 2: Save the HTML
1. Right-click anywhere on the page
2. Select **"Save Page As..."** or **"Seite speichern unter..."**
3. Choose **"Webpage, Complete"** or **"Webseite, komplett"**
4. Save as `curriculum.html` (or any name with `.html` extension)

## Basic Usage

### Command Line

```bash
# Basic extraction
python main.py curriculum.html

# Custom output file
python main.py curriculum.html -o my_study_data.json

# Enable debug mode (saves raw JSON)
python main.py curriculum.html --debug

# Compact JSON (no pretty printing)
python main.py curriculum.html --no-pretty
```

### Python Script

```python
from scraper import WBHScraper

# Create scraper with HTML file
scraper = WBHScraper("curriculum.html")

# Get raw JSON data (default)
raw_data = scraper.raw_json

# Or get transformed data
study_program = scraper.transform()

# Save to JSON
scraper.save_to_file("my_data.json")
```

## Advanced Usage

### Processing Multiple Files

```python
from pathlib import Path
from scraper import WBHScraper

# Process all HTML files in a directory
html_dir = Path("./html_exports")
output_dir = Path("./json_output")
output_dir.mkdir(exist_ok=True)

for html_file in html_dir.glob("*.html"):
    print(f"Processing {html_file.name}...")

    scraper = WBHScraper(html_file)
    study_program = scraper.transform()
    output_file = output_dir / f"{html_file.stem}.json"
    scraper.save_to_file(output_file)

    print(f"  → Saved to {output_file}")
```

### Analyzing Study Progress

```python
from scraper import WBHScraper
from scraper.models import ElementType

scraper = WBHScraper("curriculum.html")
study_program = scraper.transform()

# Calculate progress
# Sum up credit points from all modules
total_cp = sum(m.credit_points or 0 for m in study_program.modules.values())
print(f"Total Credit Points: {total_cp}/180")

# Check progress by semester
for semester in range(1, 8):
    elements = study_program.get_elements_by_semester(semester)
    exams = [e for e in elements if e.is_exam]
    semester_cp = sum(e.credit_points or 0 for e in exams)
    print(f"Semester {semester}: {len(elements)} elements, {semester_cp} CP")

# Find unfinished exams
exams = study_program.get_elements_by_type(ElementType.EXAM)
pending_exams = [e for e in exams if not e.is_passed]
print(f"\nPending exams: {len(pending_exams)}")
for exam in pending_exams[:5]:  # Show first 5
    print(f"  - {exam.code}: {exam.name} ({exam.credit_points} CP)")
```

### Extracting Document Information

```python
from scraper import WBHScraper
from collections import defaultdict

scraper = WBHScraper("curriculum.html")
study_program = scraper.transform()

# Collect all documents
document_stats = defaultdict(int)
total_size_kb = 0

for element in study_program.elements:
    for doc in element.documents:
        document_stats[doc.content_type.value] += 1

        # Parse size (if available)
        if doc.size and 'KB' in doc.size:
            try:
                size = float(doc.size.replace('KB', '').strip())
                total_size_kb += size
            except ValueError:
                pass

print("Document Statistics:")
for doc_type, count in sorted(document_stats.items()):
    print(f"  {doc_type.upper()}: {count} files")

print(f"\nEstimated total size: {total_size_kb/1024:.1f} MB")
```

### Creating a Study Overview

```python
from scraper import WBHScraper
import json

scraper = WBHScraper("curriculum.html")
study_program = scraper.transform()

# Create overview
overview = {
    "program": f"{study_program.study_program.number} - {study_program.study_program.name}",
    "modules": len(study_program.modules),
    "total_credit_points": sum(m.credit_points or 0 for m in study_program.modules.values()),
    "semesters": {}
}

# Analyze each semester
for semester in range(1, 8):
    elements = study_program.get_elements_by_semester(semester)
    if elements:
        exams = [e for e in elements if e.is_exam]
        overview["semesters"][f"Semester {semester}"] = {
            "elements": len(elements),
            "exams": len(exams),
            "credit_points": sum(e.credit_points or 0 for e in exams)
        }

# Save overview
with open("study_overview.json", "w", encoding="utf-8") as f:
    json.dump(overview, f, indent=2, ensure_ascii=False)

print("Study overview saved to study_overview.json")
```

## Working with the Output

### Loading JSON Data

```python
import json

with open("data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Access different parts
study_program = data["study_program"]
modules = data["modules"]
elements = data["elements"]
```

### Converting to CSV

```python
import json
import csv

# Load data
with open("data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Export elements to CSV
with open("elements.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["ID", "Code", "Name", "Type", "Semester", "CP"])

    for element in data["elements"]:
        writer.writerow([
            element["id"],
            element["code"],
            element["name"],
            element["type"],
            element.get("semester", 0),
            element.get("credit_points", "")
        ])

print("Elements exported to elements.csv")
```

### Creating a Markdown Report

```python
from scraper import WBHScraper

scraper = WBHScraper("curriculum.html")
study_program = scraper.transform()

# Generate Markdown report
report = []
report.append(f"# {study_program.study_program.name}")
report.append(f"\n**Program Number:** {study_program.study_program.number}")
report.append(f"**Total Credit Points:** {sum(m.credit_points or 0 for m in study_program.modules.values())}")
report.append(f"\n## Modules ({len(study_program.modules)})\n")

for module_id, module in study_program.modules.items():
    if module.credit_points:
        report.append(f"- **{module.name}** ({module.credit_points} CP)")

        # List exams in module
        exams = [e for e in study_program.elements
                if e.module_id == module_id and e.is_exam]
        for exam in exams:
            report.append(f"  - {exam.code}: {exam.name}")

# Save report
with open("study_report.md", "w", encoding="utf-8") as f:
    f.write("\n".join(report))

print("Report saved to study_report.md")
```

## Troubleshooting

### No Data Found
**Error:** "No curriculum JSON data found in HTML"

**Solution:**
- Ensure you saved the complete webpage (not just HTML)
- Try saving from different pages in the Online Campus
- Check if you're logged in properly

### File Not Found
**Error:** "FileNotFoundError"

**Solution:**
- Check the file path is correct
- Use absolute paths if relative paths don't work
- Ensure the file has `.html` extension

### Encoding Issues
**Error:** Unicode/encoding errors

**Solution:**
```python
# Specify encoding explicitly
scraper = WBHScraper("curriculum.html")
study_program = scraper.transform()

# When saving, ensure UTF-8
scraper.save_to_file("data.json", pretty=True)
```

## Tips and Best Practices

1. **Regular Backups**: Save your HTML exports regularly to track progress
2. **Version Control**: Keep different versions of exports (e.g., `2024_01_curriculum.html`)
3. **Validation**: Always check the statistics to ensure complete extraction
4. **Documentation**: Document any custom scripts or modifications

## Integration with Other Tools

### Export for Excel
```python
import pandas as pd
import json

# Load data
with open("data.json", "r") as f:
    data = json.load(f)

# Convert to DataFrame
df = pd.DataFrame(data["elements"])

# Export to Excel
df.to_excel("study_elements.xlsx", index=False)
print("Data exported to study_elements.xlsx")
```

### Integration with Study Planner
```python
# Future integration with wbh-organizer
from wbh_campus_scraper import WBHScraper
from wbh_organizer import StudyPlanner

scraper = WBHScraper("curriculum.html")
data = scraper.raw_json

planner = StudyPlanner(data)
planner.create_folder_structure()
planner.generate_study_plan()
```