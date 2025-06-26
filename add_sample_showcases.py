import datetime
import json
from sqlalchemy import select, insert, delete
from database_utils import Session, community_showcases

# Function to add a sample showcase
def add_sample_showcase(title, description, author, category, tags, dataset_id=None, upvotes=0, is_featured=0):
    session = Session()
    try:
        # Check if we already have this showcase (by title)
        stmt = select(community_showcases).where(community_showcases.c.title == title)
        existing = session.execute(stmt).fetchone()
        
        if existing:
            print(f"Showcase '{title}' already exists, skipping...")
            return None
            
        tags_json = json.dumps(tags)
        created_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        stmt = insert(community_showcases).values(
            title=title,
            description=description,
            author=author,
            category=category,
            tags=tags_json,
            dataset_id=dataset_id,
            upvotes=upvotes,
            created_at=created_at,
            is_featured=is_featured
        )
        
        result = session.execute(stmt)
        session.commit()
        
        if result.inserted_primary_key and len(result.inserted_primary_key) > 0:
            showcase_id = result.inserted_primary_key[0]
            print(f"Added sample showcase: {title} (ID: {showcase_id})")
            return showcase_id
        return None
    except Exception as e:
        session.rollback()
        print(f"Error adding sample showcase '{title}': {str(e)}")
        return None
    finally:
        session.close()

# Sample showcases
sample_showcases = [
    {
        "title": "E-Commerce Kundendatenbank mit realistischen Kaufmustern",
        "description": """Diese E-Commerce-Datenkonfiguration erzeugt realistische Kundendaten für einen Online-Shop, komplett mit Adressen, Kontaktinformationen und Kaufmustern.

Besonders nützlich ist die Kombination von Benutzeridentität mit Finanzdaten und Adressen, um Testszenarien für Bestellabwicklung, Rechnungsstellung und Lieferlogistik zu erstellen. Die generierten Daten sind ideal für die Entwicklung und das Testen von:

1. Bestellverwaltungssystemen
2. Kunden-Dashboard-Funktionen
3. Recommender-Systemen basierend auf Kaufhistorie
4. Abrechnungs- und Versandsoftware

Die Daten enthalten keine echten personenbezogenen Informationen, sind aber realistisch genug, um echte Anwendungsfälle zu simulieren.""",
        "author": "Markus Weber",
        "category": "E-Commerce",
        "tags": ["user-profiles", "payments", "e-commerce", "address", "large-dataset"],
        "upvotes": 15,
        "is_featured": 1
    },
    {
        "title": "Gesundheitsdaten mit DSGVO-konformer Pseudonymisierung",
        "description": """Diese Konfiguration erzeugt pseudonymisierte Patientendaten, die für Tests von Gesundheits-IT-Systemen verwendet werden können, während gleichzeitig die DSGVO-Anforderungen eingehalten werden.

Die Daten umfassen:
- Pseudonymisierte Patientenidentifikationen
- Altersgruppen statt exakter Geburtsdaten
- Regionale gesundheitliche Trends ohne persönliche Zuordnung
- Behandlungskategorien und Medikamentenklassen

Dieses Szenario zeigt, wie man anspruchsvolle Gesundheitsdaten generieren kann, die für Testzwecke nützlich sind, ohne echte Patientendaten zu gefährden.""",
        "author": "Dr. Julia Fischer",
        "category": "Gesundheitswesen",
        "tags": ["health-data", "DSGVO", "pseudonymization", "compliance"],
        "upvotes": 23,
        "is_featured": 1
    },
    {
        "title": "Multi-Locale Testdaten für internationale Websites",
        "description": """Diese Datenkonfiguration erzeugt Testdaten für internationale Websites und Anwendungen mit Unterstützung für mehrere Locales.

Die Konfiguration generiert automatisch:
- Namen, Adressen und Telefonnummern im korrekten Format für jede Region
- Mehrsprachige Produktbeschreibungen
- Länderspezifische Währungen und Preisformate
- Regionale Datumsformate und Zeitstempel

Perfect für das Testen von Internationalisierungs- und Lokalisierungsfunktionen in globalen Anwendungen.""",
        "author": "Sandra Müller",
        "category": "Web-Anwendungen",
        "tags": ["multi-language", "i18n", "l10n", "address"],
        "upvotes": 12,
        "is_featured": 0
    },
    {
        "title": "Finanzielle Testdaten für Bankanwendungen",
        "description": """Diese Konfiguration erzeugt realistische Finanzdaten für das Testen von Bankapplikationen und Finanzanalysetools.

Die generierten Daten umfassen:
- Kontonummern im korrekten Format für verschiedene Banken
- Realistische Transaktionsdaten mit Kategorien und Beschreibungen
- Periodische Zahlungen wie Gehälter und Abonnements
- Kreditkartendaten mit gültigen Prüfsummen aber fiktiven Nummern

Die Konfiguration ist ideal für Performance-Tests mit großen Datensätzen, da sie bis zu 100.000 Transaktionen generieren kann, die typische Bankaktivitäten simulieren.""",
        "author": "Thomas Becker",
        "category": "Finanzen",
        "tags": ["financial", "banking", "performance-test", "large-dataset"],
        "upvotes": 19,
        "is_featured": 0
    },
    {
        "title": "CRM-Testdaten mit Kundenlebenszyklen",
        "description": """Diese Datenkonfiguration ist speziell für das Testen von CRM-Systemen konzipiert und generiert vollständige Kundenlebenszyklen von der ersten Anfrage bis zu wiederkehrenden Käufen.

Die Daten simulieren:
- Lead-Generierung mit unterschiedlichen Quellen
- Kundenakquise und Onboarding-Prozesse
- Support-Tickets und Kundeninteraktionen
- Kundenbindungs- und Upselling-Möglichkeiten

Besonders nützlich für das Testen von CRM-Dashboards, Reporting-Funktionen und Kundenanalysen.""",
        "author": "Laura Schmidt",
        "category": "CRM",
        "tags": ["user-profiles", "customer-journey", "sales", "support"],
        "upvotes": 8,
        "is_featured": 0
    },
    {
        "title": "IoT-Sensordaten für Smart Home Anwendungen",
        "description": """Diese Konfiguration erzeugt realistische IoT-Sensordaten, die verschiedene Smart Home Geräte simulieren.

Die generierten Daten umfassen:
- Temperatur- und Feuchtigkeitssensoren mit täglichen Schwankungen
- Bewegungsmelder mit realistischen Aktivitätsmustern
- Stromverbrauchsdaten für verschiedene Haushaltsgeräte
- Beleuchtungssensoren mit Tag/Nacht-Zyklen

Ideal für das Testen von IoT-Dashboards, Datenvisualisierungen und Automatisierungsregeln in Smart Home Anwendungen.""",
        "author": "Michael Schneider",
        "category": "IoT",
        "tags": ["sensors", "time-series", "smart-home", "performance-test"],
        "upvotes": 14,
        "is_featured": 0
    }
]

# Clear existing showcases (optional, comment this out if you want to keep existing data)
def clear_all_showcases():
    session = Session()
    try:
        stmt = delete(community_showcases)
        result = session.execute(stmt)
        session.commit()
        print(f"Cleared {result.rowcount} existing showcases")
    except Exception as e:
        session.rollback()
        print(f"Error clearing showcases: {str(e)}")
    finally:
        session.close()

# Main function to add all sample showcases
def add_all_sample_showcases(clear_first=False):
    if clear_first:
        clear_all_showcases()
        
    for showcase in sample_showcases:
        add_sample_showcase(
            title=showcase["title"],
            description=showcase["description"],
            author=showcase["author"],
            category=showcase["category"],
            tags=showcase["tags"],
            upvotes=showcase["upvotes"],
            is_featured=showcase["is_featured"]
        )
    
    print("Finished adding sample showcases")

# Run when executed directly
if __name__ == "__main__":
    add_all_sample_showcases(clear_first=True)