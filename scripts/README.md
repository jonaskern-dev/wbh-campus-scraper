# Helper Scripts

This directory contains utility scripts for maintaining and managing the project.

## helpers/anonymize_fixtures.py

Anonymizes personal data in test fixtures by replacing real names, grades, and dates with generic test data.

### Usage

```bash
# Anonymize with custom names
python scripts/helpers/anonymize_fixtures.py -f OldFirstname -l OldLastname

# Anonymize with custom replacement names
python scripts/helpers/anonymize_fixtures.py -f OldFirstname -l OldLastname --new-firstname Max --new-lastname Mustermann

# Just anonymize grades and dates without name changes
python scripts/helpers/anonymize_fixtures.py
```

### Options

- `-f, --firstname`: Original first name to replace
- `-l, --lastname`: Original last name to replace
- `--new-firstname`: New first name (default: Max)
- `--new-lastname`: New last name (default: Mustermann)
- `--seed`: Random seed for reproducible results (default: 42)

### Features

- Replaces personal names in HTML and JSON files
- Randomizes grades between 1.0-4.0 for passing, 5.0 for failing
- Randomizes dates between 2023-2025
- Uses seed for reproducible "random" data
- Preserves file structure and test functionality