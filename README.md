# WBH Campus Scraper

Extrahiert und verarbeitet Studiendaten aus WBH Online Campus HTML-Exports.

## Schnellstart

```bash
# 1. HTML vom WBH Campus exportieren:
#    Mein Studium → Studiengänge → [Ihr Studiengang] (z.B. Informatik)
#    → Webseite komplett speichern als curriculum.html
# 2. Daten extrahieren
python3 main.py curriculum.html

# Oder mit Debug-Modus (speichert Raw-JSON)
python3 main.py curriculum.html --debug
```

## Was wird extrahiert?

Eine strukturierte JSON-Datei (`data.json`) mit:
- **Studiengang-Informationen** (ID, Nummer, Name)
- **25 Module** mit korrekten Credit Points
- **135 Elemente** (Lernhefte, Prüfungen, Seminare)
- **215 Dokumente** (PDF, EPUB, HTML, MP3, ZIP)
- **Semester-Zuordnung** automatisch berechnet
- **Modul-Hierarchie** erhalten

## Features

- **OOP-Architektur** mit sauberen Datenmodellen
- **Automatische CP-Extraktion** aus Prüfungen
- **Dokument-Informationen** für Downloads
- **Debug-Modus** für Entwicklung
- **Statistiken** und Analysen
- **Unit Tests** für Qualitätssicherung

## Projektstruktur

```
wbh-campus-scraper/
├── scraper/            # Hauptpaket
│   ├── models.py       # Datenmodelle
│   ├── parser.py       # HTML/JSON Parser
│   └── scraper.py      # Hauptklasse
├── tests/              # Unit Tests
├── main.py            # CLI Einstiegspunkt
└── setup.py           # Package Setup
```

## Funktionsweise

1. **Scraping**: Extrahiert JSON-Daten aus HTML (`WL.DEBUG.iCurriculumJSON`)
2. **Gruppierung**: Erkennt zusammengehörige Module automatisch
3. **Struktur**: Erstellt Semester-basierte Ordnerstruktur
4. **Dokumentation**: Speichert CP und Status in Textdateien


## Python API

```python
from scraper import WBHScraper

# Scraper mit HTML-Datei initialisieren
scraper = WBHScraper("curriculum.html")

# Raw JSON direkt zugreifen (Standard)
raw_data = scraper.raw_json

# Oder transformierte Daten erhalten
study_program = scraper.transform()
print(f"Studiengang: {study_program.study_program.number} {study_program.study_program.name}")
print(f"Module gesamt: {len(study_program.modules)}")

# In Datei speichern
scraper.save_to_file("output.json")
```

## Installation

```bash
# Development Installation
pip install -e .

# Tests ausführen
python -m pytest tests/
```

## Lizenz

MIT License

## Autor

Jonas Kern - [info@jonaskern.de](mailto:info@jonaskern.de) - [https://jonaskern.dev](https://jonaskern.dev)

---

*Version 0.2.0 - Release*