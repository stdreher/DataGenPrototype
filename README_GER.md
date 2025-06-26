# 🎲 Testdaten Generator (Test Data Generator)

Ein Streamlit-basierter Test-Datengenerator mit einer Benutzeroberfläche zur Spezifikation und zufälligen Permutation von Webportal-Benutzerdaten sowie DSGVO-konformen Pseudonymisierungsfunktionen.

## Funktionsübersicht

Der Testdaten Generator ist ein Tool zur Erstellung synthetischer Testdaten für Webportale und Anwendungen. Es bietet folgende Hauptfunktionen:

- **Flexible Datengenerierung**: Generieren Sie synthetische Daten mit anpassbaren Feldern und Formaten
- **Feldkonfiguration**: Passen Sie Parameter für jedes Feld an (z.B. Passwortlänge, Zahleneinschluss usw.)
- **Datenexport**: Exportieren Sie generierte Daten als CSV, JSON oder SQL
- **Datenbankanbindung**: Speichern und laden Sie Ihre Generierungskonfigurationen für die Wiederverwendung
- **DSGVO-Konformität**: Datenpseudonymisierungsfunktionen mit mehreren Methoden
- **Datenschutz**: Direkter Vergleich von originalen und pseudonymisierten Daten
- **Mehrsprachig**: Vollständig in Deutsch mit Unterstützung für verschiedene Daten-Locales
- **Animationen**: Würfel- und Schloss-Animationen für Datenoperationen

## Technische Details

Der Testdaten Generator wurde mit folgenden Technologien entwickelt:

- **Streamlit**: Benutzeroberfläche und Anwendungsrahmen
- **Pandas**: Datenverarbeitung und -manipulation
- **Faker**: Generierung synthetischer Daten
- **SQLAlchemy**: Datenbankinteraktion
- **PostgreSQL**: Persistente Speicherung von Konfigurationen
- **Hashlib**: Sichere Datenpseudonymisierung

## Anleitung

### Installation und Start

1. Stellen Sie sicher, dass Python 3.11 oder höher installiert ist
2. Klonen Sie das Repository
3. Installieren Sie die erforderlichen Pakete:
   ```
   pip install streamlit pandas numpy faker sqlalchemy psycopg2-binary openpyxl
   ```
4. Starten Sie die Anwendung: `streamlit run Home.py`

### Abhängigkeiten

- **streamlit**: Version 1.35.0 oder höher
- **pandas**: Version 2.2.0 oder höher
- **numpy**: Version 1.26.0 oder höher
- **faker**: Version 37.0.0 oder höher
- **sqlalchemy**: Version 2.0.35 oder höher
- **psycopg2-binary**: Version 2.9.9 oder höher
- **openpyxl**: Version 3.1.2 oder höher

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
- Wählen Sie das gewünschte Exportformat (CSV, JSON oder SQL)
- Bei SQL-Export können Sie den Tabellennamen anpassen und eine Vorschau des SQL-Scripts anzeigen lassen
- Laden Sie die generierten Daten herunter

#### 4. Konfigurationen speichern und laden

- Speichern Sie Ihre bevorzugten Generierungskonfigurationen in der Datenbank
- Eine automatische Zusammenfassung mit 1. Anzahl der Datensätze, 2. Daten-Locale und 3. Exportformat wird im Beschreibungsfeld angezeigt
- Laden Sie gespeicherte Konfigurationen mit dem Formular "Konfiguration laden" 
- Löschen Sie nicht mehr benötigte Konfigurationen mit dem Formular "Konfiguration löschen"
- Nutzen Sie die ID aus der darunter angezeigten Liste der gespeicherten Konfigurationen

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

## SQL-Export-Funktionalität

Der Generator verfügt über eine fortschrittliche SQL-Export-Funktion, die es ermöglicht, die generierten Testdaten direkt als SQL-Script zu exportieren:

- **Datentyperkennung**: Die Anwendung erkennt automatisch die geeigneten SQL-Datentypen für Ihre Felder
- **Anpassbarer Tabellenname**: Definieren Sie einen benutzerdefinierten Namen für die SQL-Tabelle
- **Kompatibilität**: Die erzeugten SQL-Scripts sind mit PostgreSQL, MySQL, SQLite und den meisten anderen SQL-Dialekten kompatibel
- **Vorschau**: Eine Vorschau des SQL-Scripts wird vor dem Download angezeigt
- **Batch-Inserts**: Die Daten werden in Batches eingefügt, um die Effizienz zu verbessern
- **Sicherheit**: Werte werden ordnungsgemäß für SQL escaped, um SQL-Injection zu verhindern

Das erzeugte SQL-Script enthält:
1. CREATE TABLE-Anweisung mit angemessenen Datentypen
2. Optionale DELETE-Anweisung zum Leeren der Tabelle
3. INSERT-Anweisungen für alle Datensätze
4. Dokumentierende Kommentare mit Zeitstempel

## Datenbank-Funktionalität

Die Anwendung verwendet eine PostgreSQL-Datenbank zur Speicherung von Generierungskonfigurationen. Folgende Operationen werden unterstützt:

- **Speichern**: Speichern Sie die aktuelle Konfiguration mit Name und Beschreibung
- **Laden**: Laden Sie eine gespeicherte Konfiguration anhand ihrer ID
- **Löschen**: Entfernen Sie nicht mehr benötigte Konfigurationen
- **Auflisten**: Zeigen Sie alle gespeicherten Konfigurationen an

## Projektstruktur

- `Home.py`: Haupteinstiegspunkt der Anwendung mit Navigation
- `pages/1_Testdaten_Generator.py`: Oberfläche zur Testdatengenerierung
- `pages/2_Pseudonymizer.py`: Oberfläche zur Datenpseudonymisierung
- `data_generator.py`: Kernfunktionen zur Datengenerierung
- `field_definitions.py`: Definitionen und Parameter für alle unterstützten Felder
- `export_utils.py`: Hilfsfunktionen für den Datenexport
- `database_utils.py`: Funktionen für die Datenbankinteraktion
- `pseudonymize_utils.py`: Funktionen für DSGVO-konforme Datenpseudonymisierung
- `.streamlit/config.toml`: Streamlit-Konfiguration

## Datenpseudonymisierungsfunktion

Die Anwendung enthält ein robustes DSGVO-konformes Datenpseudonymisierungssystem, das folgende Funktionen bietet:

- **Mehrere Methoden**: Wählen Sie aus verschiedenen Pseudonymisierungstechniken:
  - **Hash**: Irreversible SHA-256-Hashwerte sensibler Daten
  - **Maskieren**: Teilweise Maskierung von Daten (z.B. "jo**********@example.com")
  - **Ersetzen**: Ersetzung durch realistische, aber gefälschte Werte
  - **Versatz**: Verschiebung numerischer Werte um einen konstanten Betrag

- **Datei-Upload**: Laden Sie Datendateien in CSV-, Excel- oder JSON-Formaten hoch
- **Spaltenauswahl**: Wählen Sie, welche Spalten pseudonymisiert werden sollen und welche Methoden anzuwenden sind
- **Direkter Vergleich**: Sehen Sie originale und pseudonymisierte Daten nebeneinander
- **Exportoptionen**: Laden Sie die pseudonymisierten Daten in verschiedenen Formaten herunter
- **Intelligente Erkennung**: Automatische Vorschläge für geeignete Pseudonymisierungsmethoden

### Verwendung des Pseudonymisierers

1. Navigieren Sie zur Pseudonymizer-Seite
2. Laden Sie eine Datendatei mit sensiblen Informationen hoch
3. Wählen Sie die zu pseudonymisierenden Spalten aus
4. Wählen Sie eine Pseudonymisierungsmethode für jede Spalte
5. Wenden Sie die Pseudonymisierung an
6. Überprüfen Sie die Ergebnisse und exportieren Sie sie, wenn Sie zufrieden sind

## Anpassung und Erweiterung

### Hinzufügen neuer Felder

Um ein neues Feld hinzuzufügen:

1. Definieren Sie eine Generator-Funktion in `field_definitions.py`
2. Fügen Sie die Felddefinition zum `field_definitions`-Dictionary hinzu
3. Ordnen Sie das Feld einer Kategorie in der entsprechenden Seiten-Datei zu

### Unterstützung für neue Exportformate

Um ein neues Exportformat hinzuzufügen:

1. Implementieren Sie eine Exportfunktion in `export_utils.py`
2. Fügen Sie das Format zur Auswahlmöglichkeit in der Benutzeroberfläche hinzu
3. Behandeln Sie das neue Format im Export-Abschnitt

### Hinzufügen neuer Pseudonymisierungsmethoden

Um eine neue Pseudonymisierungsmethode hinzuzufügen:

1. Implementieren Sie die Methode in `pseudonymize_utils.py`
2. Fügen Sie die Methode zur `get_pseudonymization_methods()`-Funktion hinzu
3. Aktualisieren Sie die Pseudonymisierungsoberfläche in `pages/2_Pseudonymizer.py`

## Lizenz

Dieses Projekt ist unter der MIT-Lizenz lizenziert. Siehe die LICENSE-Datei für Details.