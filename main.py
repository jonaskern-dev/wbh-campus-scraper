#!/usr/bin/env python3
"""
WBH Campus Data Extractor CLI

Main entry point for extracting study data from WBH Online Campus HTML exports.
"""

import argparse
import json
import sys
from pathlib import Path

from scraper import WBHScraper


def main():
    """Main CLI function."""
    parser = argparse.ArgumentParser(
        description="Extract study data from WBH Online Campus HTML exports",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s curriculum.html                    # Extract and save to data.json
  %(prog)s curriculum.html -o output.json     # Custom output file
  %(prog)s curriculum.html --debug            # Enable debug mode
  %(prog)s curriculum.html --pretty           # Pretty print JSON output
        """
    )

    parser.add_argument(
        "input",
        type=Path,
        help="Input HTML file (e.g., curriculum.html)"
    )

    parser.add_argument(
        "-o", "--output",
        type=Path,
        default=Path("data.json"),
        help="Output JSON file (default: data.json)"
    )

    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug mode (saves raw JSON)"
    )

    parser.add_argument(
        "--pretty",
        action="store_true",
        default=True,
        help="Pretty print JSON output (default: True)"
    )

    parser.add_argument(
        "--no-pretty",
        dest="pretty",
        action="store_false",
        help="Disable pretty printing for compact JSON"
    )

    parser.add_argument(
        "-v", "--version",
        action="version",
        version="%(prog)s 0.2.0"
    )

    args = parser.parse_args()

    # Check input file
    if not args.input.exists():
        print(f"Error: Input file '{args.input}' not found!")
        sys.exit(1)

    try:
        # Initialize scraper with file path
        print(f"Loading {args.input}...")
        scraper = WBHScraper(file_path=args.input, debug=args.debug)

        # Transform data (automatically loads from file path)
        study_program = scraper.transform()

        print(f"Successfully extracted data")

        # Save to file
        scraper.save_to_file(args.output, pretty=args.pretty)
        print(f"Data saved to {args.output}")

        # Show brief info
        print()
        print(f"{study_program.study_program.number} - {study_program.study_program.name}")
        print(f"   {len(study_program.modules)} modules, {len(study_program.elements)} elements")

        return 0

    except Exception as e:
        print(f"Error: {e}")
        if args.debug:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())