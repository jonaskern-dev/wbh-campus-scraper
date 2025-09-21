#!/usr/bin/env python3
"""
Anonymize personal data in test fixtures.

Replaces real names, grades, and dates with generic test data.
"""

import argparse
import json
import random
import re
from datetime import datetime, timedelta
from pathlib import Path


def random_grade():
    """Generate random passing grade (1.0 to 4.0 in 0.3 increments)."""
    grades = ["1.0", "1.3", "1.7", "2.0", "2.3", "2.7", "3.0", "3.3", "3.7", "4.0"]
    return random.choice(grades)


def random_date(start_year=2023, end_year=2025):
    """Generate random date between start and end year."""
    start = datetime(start_year, 1, 1)
    end = datetime(end_year, 12, 31)
    delta = end - start
    random_days = random.randint(0, delta.days)
    date = start + timedelta(days=random_days)
    return date.strftime("%d.%m.%Y")


def anonymize_html_files(old_firstname, new_firstname, old_lastname, new_lastname):
    """Anonymize HTML test fixture files."""
    fixtures_dir = Path("tests/fixtures")
    html_files = fixtures_dir.glob("curriculum_*.html")

    for html_file in html_files:
        print(f"Anonymizing {html_file.name}...")

        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Replace names using provided parameters
        if old_firstname and new_firstname:
            content = re.sub(rf'\b{re.escape(old_firstname)}\b', new_firstname, content, flags=re.IGNORECASE)
        if old_lastname and new_lastname:
            content = re.sub(rf'\b{re.escape(old_lastname)}\b', new_lastname, content, flags=re.IGNORECASE)

        # Replace email addresses if any
        content = re.sub(r'[\w\.-]+@[\w\.-]+\.\w+', 'max.mustermann@example.com', content)

        # Replace student numbers (if they look like 7-8 digit numbers)
        content = re.sub(r'\b\d{7,8}\b', '12345678', content)

        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(content)


def anonymize_json_files():
    """Anonymize JSON expected output files."""
    fixtures_dir = Path("tests/fixtures")
    json_files = fixtures_dir.glob("expected_output_*.json")

    for json_file in json_files:
        print(f"Anonymizing {json_file.name}...")

        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Anonymize elements
        for element in data.get('elements', []):
            # Anonymize mark_and_points if present
            if element.get('mark_and_points'):
                mp = element['mark_and_points']

                # Replace grades
                if mp.get('mark') and mp['mark'] not in [None, 'ok', 'nicht bestanden']:
                    # Generate random grade
                    new_grade = random_grade()
                    mp['mark'] = new_grade
                    mp['mark_label'] = new_grade

                # Replace dates
                if mp.get('esa_send_date'):
                    mp['esa_send_date'] = random_date()

                if mp.get('esa_grade_date'):
                    # Grade date should be after send date
                    send_date = mp.get('esa_send_date', random_date())
                    try:
                        base_date = datetime.strptime(send_date, "%d.%m.%Y")
                        grade_date = base_date + timedelta(days=random.randint(1, 14))
                        mp['esa_grade_date'] = grade_date.strftime("%d.%m.%Y")
                    except:
                        mp['esa_grade_date'] = random_date()

                # Update tooltip if present
                if mp.get('mark_and_points_tooltip'):
                    tooltip = mp['mark_and_points_tooltip']
                    if mp.get('esa_send_date'):
                        tooltip = re.sub(
                            r'Lösungseingang:</b> \d{2}\.\d{2}\.\d{4}',
                            f'Lösungseingang:</b> {mp["esa_send_date"]}',
                            tooltip
                        )
                    if mp.get('esa_grade_date'):
                        tooltip = re.sub(
                            r'Benotungsdatum:</b> \d{2}\.\d{2}\.\d{4}',
                            f'Benotungsdatum:</b> {mp["esa_grade_date"]}',
                            tooltip
                        )
                    mp['mark_and_points_tooltip'] = tooltip

                # Set failed exams to 5.0
                if mp.get('exam_css_class') == 'examFailed':
                    mp['mark'] = '5.0'
                    mp['mark_label'] = '5.0'

        # Save anonymized data
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)


def main():
    """Run anonymization on all test fixtures."""
    parser = argparse.ArgumentParser(
        description="Anonymize personal data in test fixtures",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --firstname John --lastname Doe
  %(prog)s -f John -l Doe --new-firstname Max --new-lastname Mustermann
  %(prog)s  # Just anonymize grades and dates without name changes
        """
    )

    parser.add_argument(
        '-f', '--firstname',
        help='Original first name to replace'
    )
    parser.add_argument(
        '-l', '--lastname',
        help='Original last name to replace'
    )
    parser.add_argument(
        '--new-firstname',
        default='Max',
        help='New first name (default: Max)'
    )
    parser.add_argument(
        '--new-lastname',
        default='Mustermann',
        help='New last name (default: Mustermann)'
    )
    parser.add_argument(
        '--seed',
        type=int,
        default=42,
        help='Random seed for reproducible results (default: 42)'
    )

    args = parser.parse_args()

    print("Starting anonymization of test fixtures...")

    # Set seed for reproducible "random" data
    random.seed(args.seed)

    anonymize_html_files(args.firstname, args.new_firstname, args.lastname, args.new_lastname)
    anonymize_json_files()

    print("\nAnonymization complete!")
    print("Note: HTML files are very large, so name replacement might take a moment to reflect.")
    print("Please review the changes and re-run tests to ensure everything still works.")


if __name__ == "__main__":
    main()