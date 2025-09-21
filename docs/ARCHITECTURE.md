# Architecture

## Project Structure

```
wbh-campus-scraper/
├── scraper/                    # Main package
│   ├── __init__.py            # Package exports
│   ├── scraper.py             # WBHScraper (extraction + transformation)
│   └── models/                # Data models (one class per file)
│       ├── __init__.py        # Model exports
│       ├── enums.py           # ElementType, DocumentType
│       ├── document.py        # Document model
│       ├── exam_info.py       # ExamInfo model
│       ├── sub_element.py     # SubElement model
│       ├── element.py         # Element model
│       ├── module.py          # Module model
│       ├── study_program.py   # StudyProgram & StudyProgramInfo
│       └── builder.py         # StudyProgramBuilder
│
├── tests/                      # Test suite
│   ├── fixtures/              # Test data
│   │   ├── curriculum.html   # Input HTML
│   │   └── expected_output.json
│   ├── test_models.py         # Unit tests for models
│   ├── test_integration.py    # Integration tests
│   ├── test_end_to_end.py    # End-to-end tests
│   └── test_complete_pipeline.py # CLI pipeline tests
│
├── docs/                       # Documentation
│   ├── DATA_STRUCTURE.md     # JSON structure documentation
│   ├── API.md                # API reference
│   ├── USAGE.md              # User guide
│   └── ARCHITECTURE.md       # This file
│
├── main.py                    # CLI entry point
├── setup.py                   # Package configuration
├── README.md                  # Main documentation
├── README_DE.md              # German documentation
└── CLAUDE.md                  # Development instructions

```

## Class Hierarchy

### Models
Each model has its own file for better maintainability:

```
models/
├── enums.py
│   ├── ElementType (Enum)
│   └── DocumentType (Enum)
│
├── document.py
│   └── Document (dataclass)
│
├── exam_info.py
│   └── ExamInfo (dataclass)
│
├── sub_element.py
│   └── SubElement (dataclass)
│
├── element.py
│   └── Element (dataclass)
│
├── module.py
│   └── Module (dataclass)
│
├── study_program.py
│   ├── StudyProgramInfo (dataclass)
│   └── StudyProgram (dataclass)
│
└── builder.py
    └── StudyProgramBuilder (class)
```

## Data Flow

```
1. HTML Input (curriculum.html)
        ↓
2. WBHScraper(file_path) - Initialize with HTML file
        ↓
3. scraper.raw_json - Access raw JSON data (default)
        ↓
4. scraper.transform() - Transform to structured models (optional)
        ↓
5. StudyProgramBuilder (constructs models internally)
        ↓
6. StudyProgram (complete data structure)
        ↓
7. scraper.save_to_file() - JSON Output (data.json)
```

## Design Principles

### 1. Separation of Concerns
- **WBHScraper**: Extracts JSON from HTML and optionally transforms to models
- **Models**: Define data structures
- **Builder**: Constructs the data model (internal to WBHScraper)

### 2. Single Responsibility
- Each model class has its own file
- Each class has a single, clear purpose
- Models are pure data structures (dataclasses)

### 3. Clean Architecture
- Models are pure data structures
- WBHScraper handles both extraction and transformation
- Builder is encapsulated within WBHScraper
- Raw JSON access is the default, transformation is optional

### 4. Testability
- Pure functions where possible
- Dependency injection (debug mode)
- Comprehensive test coverage
- Fixtures for reproducible tests

## Model Responsibilities

### Core Data Models
- **Document**: File attachment information
- **ExamInfo**: Exam-specific metadata
- **SubElement**: Content within elements
- **Element**: Study units (courses, exams, seminars)
- **Module**: Groups of related elements
- **StudyProgram**: Complete program structure

### Helper Classes
- **StudyProgramBuilder**: Constructs StudyProgram from raw data
- **Enums**: Type definitions for consistency

## Testing Strategy

### Unit Tests (test_models.py)
- Test each model in isolation
- Verify JSON serialization
- Check dataclass functionality

### Integration Tests (test_integration.py)
- Test component interaction
- Verify data extraction
- Check calculations

### End-to-End Tests (test_end_to_end.py)
- Complete HTML to JSON conversion
- Deep structure comparison
- File I/O operations

### Pipeline Tests (test_complete_pipeline.py)
- Command-line interface
- Real-world usage scenarios
- Output formatting options

## Future Extensions

### Planned Features
1. **Direct campus access**: Login and scrape without HTML export
2. **Document downloads**: Automatic PDF/EPUB retrieval
3. **Progress tracking**: Monitor study progress
4. **Brew package**: Easy installation via Homebrew

### Extension Points
- Add new element types in `enums.py`
- Extend models with additional fields
- Add new output formats in scraper
- Implement caching in scraper