# WBH Campus Scraper

Extrahiert und verarbeitet Studienprogrammdaten aus HTML-Exporten des WBH Online Campus.

## Schnellstart

```bash
# 1. HTML vom WBH Campus exportieren:
#    Mein Studium → Studiengänge → [Ihr Studiengang] (z.B. Informatik)
#    → Komplette Webseite speichern als curriculum.html

# 2. Daten extrahieren (nach Installation)
wbh-scraper curriculum.html

# Oder während der Entwicklung
python3 main.py curriculum.html

# Mit Optionen
wbh-scraper curriculum.html --debug  # Debug-Modus aktivieren
wbh-scraper curriculum.html -o meine_daten.json  # Eigene Ausgabedatei
```

## Was wird extrahiert?

Eine strukturierte JSON-Datei (`data.json`) mit:
- **Studienprogramm-Informationen** (ID, Nummer, Name)
- **Alle Module** mit korrekten Credit Points
- **Alle Elemente** (Lernhefte, Prüfungen, Seminare)
- **Alle Dokumente** (PDF, EPUB, HTML, MP3, ZIP)
- **Semester-Zuordnungen** automatisch berechnet
- **Modul-Hierarchie** erhalten

## Funktionen

- **OOP-Architektur** mit sauberen Datenmodellen
- **Automatische CP-Extraktion** aus Prüfungen
- **Dokument-Informationen** für Downloads
- **Debug-Modus** für Entwicklung
- **Statistiken** und Analysen
- **Unit-Tests** für Qualitätssicherung

## Projektstruktur

```
wbh-campus-scraper/
├── scraper/            # Hauptpaket
│   ├── models/         # Datenmodelle
│   └── scraper.py      # Hauptklasse
├── tests/              # Unit-Tests
├── main.py            # CLI-Einstiegspunkt
└── setup.py           # Paket-Setup
```

## Funktionsweise

1. **Scraping**: Extrahiert JSON-Daten aus HTML (`WL.DEBUG.iCurriculumJSON`)
2. **Parsing**: Verarbeitet Rohdaten zu strukturierten Modellen
3. **Aufbau**: Erstellt vollständige Studienprogramm-Hierarchie
4. **Export**: Speichert als sauberes JSON mit allen Beziehungen

## Python API

```python
from scraper import WBHScraper

# Scraper mit HTML-Datei initialisieren
scraper = WBHScraper("curriculum.html")

# Direkter Zugriff auf Raw-JSON (Standard)
raw_data = scraper.raw_json

# Oder transformierte Daten abrufen
study_program = scraper.transform()
print(f"Programm: {study_program.study_program.number} {study_program.study_program.name}")
print(f"Module gesamt: {len(study_program.modules)}")

# In Datei speichern
scraper.save_to_file("output.json")
```

## Installation

```bash
# Über Homebrew
brew tap jonaskern-dev/tap
brew install wbh-campus-scraper

# Über pip von GitHub
pip install git+https://github.com/jonaskern-dev/wbh-campus-scraper.git

# Für Entwicklung
git clone https://github.com/jonaskern-dev/wbh-campus-scraper.git
cd wbh-campus-scraper
pip install -e .

# Nach der Installation ist der Befehl verfügbar:
wbh-scraper --version

# Tests ausführen
python -m unittest discover tests
```

## Lizenz

MIT Lizenz

## Autor

Jonas Kern - [info@jonaskern.de](mailto:info@jonaskern.de) - [https://jonaskern.dev](https://jonaskern.dev)

---

*Version 0.4.0 - Release*