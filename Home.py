import streamlit as st

# Set page config
st.set_page_config(
    page_title="Testdaten Generator",
    page_icon="🎲",
    layout="wide",
)

# Title and introduction
st.title("🎲 Testdaten Generator mit DSGVO-konformer Pseudonymisierung")

st.markdown("""
## Willkommen zum erweiterten Testdaten Generator

Diese Anwendung bietet zwei Hauptfunktionen:

### 1. 🎲 Testdaten Generator
Generieren Sie synthetische Testdaten für Webportale mit anpassbaren Feldern und Formaten.
Wählen Sie die benötigten Felder aus, passen Sie die Parameter an und laden Sie Ihren Datensatz herunter.

### 2. 🔒 Daten Pseudonymisierung
DSGVO-konforme Pseudonymisierung für echte Datensätze. Laden Sie Ihre Daten hoch und wenden Sie
verschiedene Pseudonymisierungsmethoden auf sensible Felder an.

## Navigation
Verwenden Sie das Seitenmenü am linken Rand, um zwischen den Funktionen zu wechseln:
- **Testdaten Generator**: Zum Erstellen vollständig synthetischer Daten
- **Pseudonymizer**: Zum DSGVO-konformen Pseudonymisieren echter Daten
- **Community Showcase**: Entdecken Sie interessante Datenszenarien aus der Community

## Hinweis zur DSGVO
Die Pseudonymisierungsfunktion bietet verschiedene Methoden, um personenbezogene Daten gemäß den Anforderungen
der Datenschutz-Grundverordnung zu pseudonymisieren, sodass sie für Testzwecke verwendet werden können.
""")

st.info("""
**Was ist der Unterschied zwischen den beiden Funktionen?**

- **Testdaten Generator**: Erzeugt vollständig künstliche Daten, die keine realen Personen repräsentieren.
- **Daten Pseudonymisierung**: Verändert existierende Daten so, dass sie nicht mehr auf reale Personen zurückführbar sind, 
  während für Testzwecke wichtige Eigenschaften und Strukturen erhalten bleiben.
""")

# Show the features side by side
col1, col2 = st.columns(2)

with col1:
    st.subheader("Testdaten Generator")
    st.markdown("""
    **Hauptfunktionen:**
    - Generierung realistischer synthetischer Daten
    - Anpassbare Felder und Formate
    - Export in CSV, JSON, und SQL
    - Speichern und Laden von Konfigurationen
    - Mehrsprachige Unterstützung
    """)
    
    st.markdown("**Ideal für:**")
    st.markdown("- Testdaten für Entwicklungsumgebungen")
    st.markdown("- Schulungsszenarien")
    st.markdown("- Demo-Anwendungen")
    st.markdown("- Performance-Tests")

with col2:
    st.subheader("Daten Pseudonymisierung")
    st.markdown("""
    **Hauptfunktionen:**
    - Pseudonymisierung realer Daten nach DSGVO
    - Mehrere Pseudonymisierungsmethoden:
       - Hash (nicht umkehrbar)
       - Maskierung (teilweise Sichtbarkeit)
       - Ersetzung (realistische Fake-Daten)
       - Offset (für numerische und Datumswerte)
    - Side-by-side Vergleich Original vs. Pseudonymisiert
    """)
    
    st.markdown("**Ideal für:**")
    st.markdown("- Erfüllung von DSGVO-Anforderungen")
    st.markdown("- Sicherung sensibler Kundendaten")
    st.markdown("- Nutzung echter Datenstrukturen für Tests")
    st.markdown("- Export für Drittparteien")