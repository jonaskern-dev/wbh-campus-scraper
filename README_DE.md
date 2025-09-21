# WBH Campus Scraper

Extrahiert und verarbeitet Studiendaten aus WBH Online Campus HTML-Exports.

## Schnellstart

### 1. HTML vom WBH Online Campus exportieren
1. Navigiere zu: **Mein Studium** → **Studiengänge**
2. Wähle deinen aktuellen Studiengang aus (z.B. "Informatik (Bachelor)")
3. Speichere die komplette Webseite (Strg+S / Cmd+S) als `curriculum.html`

### 2. Daten extrahieren
```bash
# Standard-Extraktion zu data.json
python3 main.py curriculum.html

# Eigene Ausgabe-Datei
python3 main.py curriculum.html -o ausgabe.json

# Mit Debug-Modus (speichert raw JSON)
python3 main.py curriculum.html --debug

# Kompaktes JSON ohne Formatierung
python3 main.py curriculum.html --no-pretty
```

## Was wird extrahiert?

Eine strukturierte JSON-Datei (`data.json`) mit:
- **Studiengangs-Informationen** (ID, Nummer, Name, Abschlusstyp)
- **Module** mit korrekten Credit Points
- **Elemente** (Lernmaterialien, Prüfungen, Seminare)
- **Dokumente** (PDF, EPUB, HTML, MP3, ZIP)
- **Semester-Zuordnungen** automatisch berechnet
- **Modul-Hierarchie** erhalten
- **Noten und Daten** (falls vorhanden)

## Features

- **Saubere OOP-Architektur** mit klar definierten Datenmodellen
- **Automatische CP-Extraktion** aus Prüfungsdaten
- **Dokument-Informationen** für Downloads
- **Noten-Extraktion** mit Bewertungsdaten
- **Debug-Modus** für Entwicklung
- **Umfassende Test-Suite** für Qualitätssicherung
- **Funktioniert mit allen WBH-Studiengängen**

## Projektstruktur

```
wbh-campus-scraper/
├── scraper/                 # Hauptpaket
│   ├── scraper.py          # HTML/JSON-Extraktion und Transformation
│   └── models/             # Datenmodelle
│       ├── element.py      # Studienelemente
│       ├── module.py       # Kursmodule
│       └── study_program.py # Vollständiges Programm
├── tests/                   # Test-Suite
│   └── fixtures/           # Testdaten
├── scripts/                # Hilfsskripte
│   └── helpers/           # Utility-Skripte
├── docs/                   # Dokumentation
├── main.py                # CLI-Einstiegspunkt
└── setup.py              # Package-Setup
```

## Funktionsweise

1. **Scraping**: Extrahiert eingebettetes JSON aus HTML (`WL.DEBUG.iCurriculumJSON`)
2. **Transformation**: Verarbeitet Rohdaten zu strukturierten Modellen
3. **Aufbau**: Konstruiert vollständige Studienprogramm-Hierarchie
4. **Export**: Speichert als sauberes JSON mit allen Beziehungen

## Hauptmerkmale

- Funktioniert für **alle** WBH-Studiengänge
- Keine Konfiguration nötig
- Automatische Modul-Gruppierung
- Erhält alle Metadaten
- Behandelt fehlende Daten elegant

## Python API

```python
from scraper import WBHScraper
from pathlib import Path

# Scraper mit HTML-Datei initialisieren
scraper = WBHScraper(Path("curriculum.html"))

# Raw JSON direkt zugreifen (Standard)
raw_data = scraper.raw_json

# Oder transformierte Daten erhalten
study_program = scraper.transform()
print(f"Programm: {study_program.study_program.number} {study_program.study_program.name}")
print(f"Module gesamt: {len(study_program.modules)}")
print(f"Elemente gesamt: {len(study_program.elements)}")

# In Datei speichern
scraper.save_to_file(Path("ausgabe.json"))
```

## Installation

```bash
# Repository klonen
git clone https://github.com/yourusername/wbh-campus-scraper.git
cd wbh-campus-scraper

# Entwicklungs-Installation
pip install -e .

# Tests ausführen
python -m unittest discover tests
```

## Anforderungen

- Python 3.7+
- Keine externen Abhängigkeiten für Kernfunktionalität

## Tests

```bash
# Alle Tests ausführen
python -m unittest discover tests

# Spezifische Test-Suite ausführen
python -m unittest tests.test_integration

# Mit ausführlicher Ausgabe
python -m unittest discover tests -v
```

## Dokumentation

- [Architektur](docs/ARCHITECTURE.md) - Systemdesign und Datenfluss
- [Datenstruktur](docs/DATA_STRUCTURE.md) - JSON-Ausgabeformat
- [API-Referenz](docs/API.md) - Detaillierte API-Dokumentation
- [Benutzerhandbuch](docs/USAGE.md) - Erweiterte Verwendungsbeispiele

## Hilfsskripte

### Testdaten anonymisieren

```bash
python scripts/helpers/anonymize_fixtures.py -f Vorname -l Nachname
```

Entfernt persönliche Daten aus Test-Fixtures für den Datenschutz.

## Lizenz

MIT License

## Autor

Jonas Kern - [info@jonaskern.de](mailto:info@jonaskern.de) - [https://jonaskern.dev](https://jonaskern.dev)

## Beiträge

Beiträge sind willkommen! Bitte zögern Sie nicht, einen Pull Request einzureichen.

---

*Version 0.2.0 - Release*