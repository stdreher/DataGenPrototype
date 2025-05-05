# Testdaten Generator (Test Data Generator)

Ein Streamlit-basierter Test-Datengenerator mit einer Benutzeroberfläche zur Spezifikation und zufälligen Permutation von Webportal-Benutzerdaten.

## Funktionsübersicht

Der Testdaten Generator ist ein Tool zur Erstellung synthetischer Testdaten für Webportale und Anwendungen. Es bietet folgende Hauptfunktionen:

- **Flexible Datengenerierung**: Generieren Sie synthetische Daten mit anpassbaren Feldern und Formaten
- **Feldkonfiguration**: Passen Sie Parameter für jedes Feld an (z.B. Passwortlänge, Zahleneinschluss usw.)
- **Datenexport**: Exportieren Sie generierte Daten als CSV oder JSON
- **Datenbankanbindung**: Speichern und laden Sie Ihre Generierungskonfigurationen für die Wiederverwendung
- **Mehrsprachig**: Vollständig in Deutsch mit Unterstützung für verschiedene Daten-Locales

## Technische Details

Der Testdaten Generator wurde mit folgenden Technologien entwickelt:

- **Streamlit**: Benutzeroberfläche und Anwendungsrahmen
- **Pandas**: Datenverarbeitung und -manipulation
- **Faker**: Generierung synthetischer Daten
- **SQLAlchemy**: Datenbankinteraktion
- **PostgreSQL**: Persistente Speicherung von Konfigurationen

## Anleitung

### Installation und Start

1. Stellen Sie sicher, dass Python 3.11 oder höher installiert ist
2. Klonen Sie das Repository
3. Installieren Sie die erforderlichen Pakete:
   ```
   pip install streamlit pandas numpy faker sqlalchemy psycopg2-binary
   ```
4. Starten Sie die Anwendung: `streamlit run app.py`

### Abhängigkeiten

- **streamlit**: Version 1.35.0 oder höher
- **pandas**: Version 2.2.0 oder höher
- **numpy**: Version 1.26.0 oder höher
- **faker**: Version 37.0.0 oder höher
- **sqlalchemy**: Version 2.0.35 oder höher
- **psycopg2-binary**: Version 2.9.9 oder höher

### Verwendung

#### 1. Felder auswählen und konfigurieren

- Wählen Sie die gewünschten Felder aus den verschiedenen Kategorien (Identität, Adresse, Kontakt usw.)
- Alle Felder sind standardmäßig deaktiviert, so dass Sie nur die benötigten Felder auswählen können
- Konfigurieren Sie die Parameter für jedes ausgewählte Feld nach Ihren Anforderungen
- Aktivieren Sie die Permutation für einzelne Felder, um die Daten zufällig zu mischen

#### 2. Daten generieren

- Geben Sie die Anzahl der zu generierenden Datensätze an
- Wählen Sie die gewünschte Locale aus (beeinflusst das Format der generierten Daten)
- Verwenden Sie optional einen Zufallsseed für reproduzierbare Ergebnisse
- Klicken Sie auf "Daten generieren", um den Prozess zu starten
- Nutzen Sie den "Zurücksetzen" Button, um die Datenvorschau zu löschen und von vorne zu beginnen

#### 3. Daten exportieren

- Sehen Sie sich die Vorschau der generierten Daten an
- Wählen Sie das gewünschte Exportformat (CSV oder JSON)
- Laden Sie die generierten Daten herunter

#### 4. Konfigurationen speichern und laden

- Speichern Sie Ihre bevorzugten Generierungskonfigurationen in der Datenbank
- Laden Sie gespeicherte Konfigurationen bei Bedarf
- Löschen Sie nicht mehr benötigte Konfigurationen

## Verfügbare Datenfelder

Der Generator unterstützt eine Vielzahl von Feldern, gruppiert in die folgenden Kategorien:

### Identität
- Benutzername
- E-Mail
- Passwort
- Vollständiger Name

### Adresse
- Straßenadresse
- Stadt
- Bundesland
- Postleitzahl
- Land

### Kontakt
- Telefonnummer
- Berufsbezeichnung
- Unternehmen

### Persönlich
- Geburtsdatum
- Geschlecht
- Kreditkarte

### Internet
- User-Agent
- IPv4-Adresse
- IPv6-Adresse
- MAC-Adresse

### Sonstiges
- UUID
- Farbe
- Währungscode

## Datenbank-Funktionalität

Die Anwendung verwendet eine PostgreSQL-Datenbank zur Speicherung von Generierungskonfigurationen. Folgende Operationen werden unterstützt:

- **Speichern**: Speichern Sie die aktuelle Konfiguration mit Name und Beschreibung
- **Laden**: Laden Sie eine gespeicherte Konfiguration anhand ihrer ID
- **Löschen**: Entfernen Sie nicht mehr benötigte Konfigurationen
- **Auflisten**: Zeigen Sie alle gespeicherten Konfigurationen an

## Projektstruktur

- `app.py`: Hauptanwendung mit Streamlit-Benutzeroberfläche
- `data_generator.py`: Kernfunktionen zur Datengenerierung
- `field_definitions.py`: Definitionen und Parameter für alle unterstützten Felder
- `export_utils.py`: Hilfsfunktionen für den Datenexport
- `database_utils.py`: Funktionen für die Datenbankinteraktion
- `.streamlit/config.toml`: Streamlit-Konfiguration

## Anpassung und Erweiterung

### Hinzufügen neuer Felder

Um ein neues Feld hinzuzufügen:

1. Definieren Sie eine Generator-Funktion in `field_definitions.py`
2. Fügen Sie die Felddefinition zum `field_definitions`-Dictionary hinzu
3. Ordnen Sie das Feld einer Kategorie in `field_categories` in `app.py` zu

### Unterstützung für neue Exportformate

Um ein neues Exportformat hinzuzufügen:

1. Implementieren Sie eine Exportfunktion in `export_utils.py`
2. Fügen Sie das Format zur Auswahlmöglichkeit in `app.py` hinzu
3. Behandeln Sie das neue Format im Export-Abschnitt

## Lizenz

Dieses Projekt ist unter der MIT-Lizenz lizenziert. Siehe die LICENSE-Datei für Details.