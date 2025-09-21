# Extraction Pattern Explained

## Das Hex-Pattern für Studiengang-Informationen

### Der Pattern:
```python
STUDY_PROGRAM_PATTERN = r'5374756469656e67616e67[0-9a-fA-F\s]+42616368656c6f72|5374756469656e67616e67[0-9a-fA-F\s]+4d6173746572'
```

### Was bedeutet das?

Dieser Pattern sucht nach **hexadezimal-kodierten Strings** im HTML für ALLE Studiengänge:

1. **`5374756469656e67616e67`** = Hex für "Studiengang"
2. **`[0-9a-fA-F\s]+`** = Beliebige Hex-Zeichen und Leerzeichen (für Nummer und Name)
3. **`42616368656c6f72`** = Hex für "Bachelor" ODER
4. **`4d6173746572`** = Hex für "Master"

Der Pattern findet damit jeden Studiengang, egal ob Informatik, Maschinenbau, Wirtschaftsinformatik etc.

### Warum Hex?

```python
# So wird Text zu Hex:
"Studiengang".encode().hex()  # → '5374756469656e67616e67'
"Informatik".encode().hex()   # → '496e666f726d6174696b'
"Ba".encode().hex()           # → '4261'

# Und zurück:
bytes.fromhex('5374756469656e67616e67').decode()  # → 'Studiengang'
```

### Der komplette Ablauf:

## 1. HTML enthält verschlüsselte URLs

Im WBH Campus HTML sind URLs oft hex-kodiert:
```html
<!-- Im HTML versteckt: -->
<script>
var url = "5374756469656e67616e672031313130...";
</script>
```

## 2. Pattern findet Hex-String

```python
hex_matches = re.findall(STUDY_PROGRAM_PATTERN, html_content)
# Findet: '5374756469656e67616e672031313130204261...'
```

## 3. Dekodierung

```python
hex_str = hex_matches[0][:200]  # Begrenzt auf 200 Zeichen
decoded = bytes.fromhex(hex_str).decode('utf-8', errors='ignore')
# Ergebnis: "Studiengang 1110 Informatik (Bachelor)..."
```

## 4. Extraktion der Infos

```python
studiengang_match = re.search(r'Studiengang\s+(\d+)\s+([^<>&]+)', decoded)
# Findet:
#   Group 1: "1110" (Studiengang-Nummer)
#   Group 2: "Informatik (Bachelor)" (Studiengang-Name)
```

## Warum dieser Ansatz?

### Problem:
- WBH Campus kodiert viele Daten in JavaScript
- Studiengang-Info ist nicht im JSON enthalten
- Info ist aber in hex-kodierten URLs versteckt

### Lösung:
1. Suche nach typischen Hex-Mustern
2. Dekodiere gefundene Hex-Strings
3. Extrahiere strukturierte Daten

## Beispiel aus echtem HTML:

```html
<!-- Irgendwo im HTML: -->
<a href="javascript:loadContent('5374756469656e67616e6720313131302042616368656c6f7220496e666f726d6174696b')">
```

Dekodiert:
```
"Studiengang 1110 Bachelor Informatik"
```

## Der Regex erklärt:

```regex
5374756469656e67616e67  # "Studiengang" in Hex
[0-9a-fA-F\s]+          # Hex-Zeichen für Nummer und Fachbereich
42616368656c6f72        # "Bachelor" in Hex
|                       # ODER
5374756469656e67616e67  # "Studiengang" in Hex
[0-9a-fA-F\s]+          # Hex-Zeichen für Nummer und Fachbereich
4d6173746572            # "Master" in Hex
```

## Fallback-Mechanismus:

Falls das Pattern nicht greift, analysiert der Scraper den Kursinhalt:
```python
# Analyse der Kursnamen für Hinweise auf den Studiengang
if any('Informatik' in str(c.get('name', '')) for c in courses[:10]):
    data['studiengang_nummer'] = '1110'
    data['studiengang_name'] = 'Informatik (Bachelor)'
elif any('Wirtschaftsinformatik' in str(c.get('name', '')) for c in courses[:10]):
    data['studiengang_nummer'] = '1120'
    data['studiengang_name'] = 'Wirtschaftsinformatik (Bachelor)'
elif any('Maschinenbau' in str(c.get('name', '')) for c in courses[:10]):
    data['studiengang_nummer'] = '2110'
    data['studiengang_name'] = 'Maschinenbau (Bachelor)'
else:
    data['studiengang_nummer'] = '0000'
    data['studiengang_name'] = 'Unbekannter Studiengang'
```

## Hauptdaten-Extraktion (JSON)

Parallel dazu wird das eigentliche JSON extrahiert:

```python
JSON_PATTERN = r'WL\.DEBUG\.iCurriculumJSON\s*=\s*(\{.*?\});'
```

Dieses Pattern findet:
```javascript
WL.DEBUG.iCurriculumJSON = {
    "ilgid": 46566,
    "iCourseList": [...],
    // ... alle Kursdaten
};
```

## Zusammenfassung:

1. **Hauptdaten**: Kommen aus `WL.DEBUG.iCurriculumJSON` (JSON)
2. **Studiengang-Info**: Wird aus hex-kodierten URLs extrahiert (universell für alle Studiengänge)
3. **Fallback**: Analysiert Kursnamen wenn Hex-Pattern fehlschlägt
4. **Kombination**: Alle Datenquellen werden in WBHScraper zusammengeführt

Der Pattern ist flexibel genug für alle WBH-Studiengänge (Bachelor und Master) und hat intelligente Fallback-Mechanismen!

## Hex-Kodierung Cheat Sheet:

| Text | Hex |
|------|-----|
| Studiengang | 5374756469656e67616e67 |
| Bachelor | 42616368656c6f72 |
| Master | 4d6173746572 |
| Informatik | 496e666f726d6174696b |
| Wirtschaftsinformatik | 576972747363686166747322696e666f726d6174696b |
| Maschinenbau | 4d61736368696e656e626175 |
| 1110 | 31313130 |
| 1120 | 31313230 |
| 2110 | 32313130 |

## Debug-Tipps:

```python
# Hex-String analysieren:
import binascii

# Text zu Hex
text = "Studiengang 1110 Informatik"
hex_str = text.encode().hex()
print(hex_str)

# Hex zu Text
hex_data = "5374756469656e67616e6720313131302042616368656c6f72"
text = bytes.fromhex(hex_data).decode()
print(text)  # "Studiengang 1110 Bachelor"
```

Diese Technik macht den Scraper robust gegen verschiedene HTML-Versionen des WBH Campus!