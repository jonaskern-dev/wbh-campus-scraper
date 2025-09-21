# API Documentation

## WBHScraper Class

The main class for extracting and transforming WBH Campus data from HTML exports.

### Constructor

```python
# Initialize with HTML file
scraper = WBHScraper("curriculum.html", debug=False)

# Or without file (load later)
scraper = WBHScraper(debug=False)
```

**Parameters:**
- `file_path` (Path, optional): Path to HTML file to load immediately
- `debug` (bool, optional): Enable debug mode. When True, saves raw JSON data. Default: False

### Properties

#### raw_json

Access the raw extracted JSON data (default output).

```python
scraper = WBHScraper("curriculum.html")
raw_data = scraper.raw_json  # Direct access to raw JSON
```

**Returns:**
- `dict`: Raw JSON data extracted from HTML
- `None`: If no data has been loaded

### Methods

#### parse_file(file_path)

Parse an HTML file and extract JSON data.

```python
raw_data = scraper.parse_file("curriculum.html")
```

**Parameters:**
- `file_path` (Path): Path to the HTML file

**Returns:**
- `dict`: Raw JSON data

**Raises:**
- `FileNotFoundError`: If the HTML file doesn't exist
- `ValueError`: If no valid JSON data found in HTML

#### transform()

Transform raw JSON data into structured StudyProgram model.

```python
study_program = scraper.transform()
```

**Returns:**
- `StudyProgram`: Object containing all structured data

**Raises:**
- `ValueError`: If no data is available to transform

#### save_to_file(file_path, pretty=True)

Save extracted data to a JSON file.

```python
scraper.save_to_file("output.json", pretty=True)
```

**Parameters:**
- `file_path` (str or Path): Output file path
- `pretty` (bool, optional): Format JSON with indentation. Default: True


## StudyProgram Class

Container for complete study program data.

### Properties

- `id` (int): Program identifier
- `number` (str): Program number
- `name` (str): Program name
- `modules` (Dict[str, Module]): Modules dictionary
- `elements` (List[Element]): All elements

### Methods

#### get_total_credit_points()

Calculate total credit points from all modules.

```python
total_cp = study_program.get_total_credit_points()
# Returns: 141.0
```

#### get_elements_by_semester(semester)

Get all elements for a specific semester.

```python
semester_1_elements = study_program.get_elements_by_semester(1)
```

**Parameters:**
- `semester` (int): Semester number (0 for additional elements)

**Returns:**
- `List[Element]`: Elements in the specified semester

#### get_elements_by_type(element_type)

Filter elements by type.

```python
from scraper.models import ElementType

exams = study_program.get_elements_by_type(ElementType.EXAM)
```

**Parameters:**
- `element_type` (ElementType): Type to filter by

**Returns:**
- `List[Element]`: Elements of the specified type

#### add_module(module)

Add a module to the study program.

```python
module = Module(id=1, name="Test Module")
study_program.add_module(module)
```

#### add_element(element)

Add an element to the study program.

```python
element = Element(id=1, code="TEST", name="Test", type=ElementType.EXAM)
study_program.add_element(element)
```

#### to_dict()

Convert to dictionary for JSON serialization.

```python
data_dict = study_program.to_dict()
json.dump(data_dict, file)
```

## Module Class

Represents a study module.

### Properties

- `id` (int): Module identifier
- `name` (str): Module name
- `code` (str, optional): Module code
- `credit_points` (float, optional): Credit points
- `element_ids` (List[int]): All element IDs
- `exam_ids` (List[int]): Exam element IDs
- `study_material_ids` (List[int]): Study material IDs

### Methods

#### add_element(element_id, is_exam=False)

Add an element to the module.

```python
module.add_element(123, is_exam=True)
```

## Element Class

Represents a study element (course, exam, seminar).

### Properties

- `id` (int): Element identifier
- `code` (str): Element code
- `name` (str): Element name
- `type` (ElementType): Element type
- `study_month` (int): Study month (default: 0)
- `semester` (int): Semester (default: 0)
- `module_id` (int, optional): Parent module ID
- `credit_points` (float, optional): Credit points
- `is_passed` (bool): Completion status (default: False)
- `exam_info` (ExamInfo, optional): Exam-specific data
- `documents` (List[Document]): Attached documents
- `sub_elements` (List[SubElement]): Sub-elements

### Computed Properties

#### is_exam

Check if element is an exam.

```python
if element.is_exam:
    print(f"Exam with {element.credit_points} CP")
```

## Document Class

Represents a downloadable document.

### Properties

- `filename` (str): File name
- `content_type` (DocumentType): Document type
- `size` (str, optional): File size
- `url` (str): Download URL
- `description` (str, optional): Description

## Enums

### ElementType

```python
from scraper.models import ElementType

# Available types:
ElementType.EXAM            # "exam"
ElementType.LEARNING_MODULE # "learning_module"
ElementType.SEMINAR        # "seminar"
```

### DocumentType

```python
from scraper.models import DocumentType

# Available types:
DocumentType.PDF     # "pdf"
DocumentType.EPUB    # "epub"
DocumentType.HTML    # "html"
DocumentType.MP3     # "mp3"
DocumentType.ZIP     # "zip"
DocumentType.UNKNOWN # "unknown"
```

## Complete Example

```python
from scraper import WBHScraper
from scraper.models import ElementType

# Method 1: Initialize with file
scraper = WBHScraper("curriculum.html", debug=False)

# Access raw JSON directly (default)
raw_data = scraper.raw_json
print(f"Found {len(raw_data['iCourseList'])} courses")

# Transform to structured data
study_program = scraper.transform()

# Access program information
print(f"Program: {study_program.number} - {study_program.name}")
print(f"Total Modules: {len(study_program.modules)}")
print(f"Total Credit Points: {study_program.get_total_credit_points()}")

# Iterate through modules
for module_id, module in study_program.modules.items():
    if module.credit_points:
        print(f"  {module.name}: {module.credit_points} CP")

# Filter elements
exams = study_program.get_elements_by_type(ElementType.EXAM)
print(f"\nFound {len(exams)} exams")

semester_1 = study_program.get_elements_by_semester(1)
print(f"Semester 1 has {len(semester_1)} elements")

# Find specific elements
for element in study_program.elements:
    if "Bachelorarbeit" in element.name:
        print(f"\nThesis: {element.name} ({element.credit_points} CP)")

    # Check for documents
    if element.documents:
        print(f"\n{element.name} has {len(element.documents)} documents:")
        for doc in element.documents:
            print(f"  - {doc.filename} ({doc.content_type.value}, {doc.size})")

# Save to JSON
scraper.save_to_file("output.json", pretty=True)

# Method 2: Load file later
scraper2 = WBHScraper()
scraper2.file_path = Path("curriculum.html")
raw_data2 = scraper2.parse_file(scraper2.file_path)
study_program2 = scraper2.transform()
```

## Error Handling

```python
from scraper import WBHScraper
from pathlib import Path

try:
    scraper = WBHScraper(Path("curriculum.html"))

    # Access raw JSON
    raw_data = scraper.raw_json

    # Transform to structured data
    study_program = scraper.transform()

    # Save to file
    scraper.save_to_file("output.json")

except FileNotFoundError:
    print("HTML file not found")
except ValueError as e:
    print(f"Extraction failed: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```