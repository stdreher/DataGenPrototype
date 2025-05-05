import streamlit as st
import pandas as pd
import numpy as np
import json
import time
from io import StringIO, BytesIO

from data_generator import generate_data
from field_definitions import field_definitions
from export_utils import export_to_csv, export_to_json

# Set page config
st.set_page_config(
    page_title="Testdaten Generator",
    page_icon="🧪",
    layout="wide",
)

# Title and introduction
st.title("🧪 Testdaten Generator")
st.markdown("""
Generieren Sie synthetische Testdaten für Webportale mit anpassbaren Feldern und Formaten.
Wählen Sie die benötigten Felder aus, passen Sie die Parameter an und laden Sie Ihren Datensatz herunter.
""")

# Sidebar for controls
with st.sidebar:
    st.header("Generierungseinstellungen")
    
    # Number of records
    num_records = st.number_input(
        "Anzahl der zu generierenden Datensätze",
        min_value=1,
        max_value=10000,
        value=100,
        help="Die Gesamtzahl der zu erzeugenden Dateneinträge"
    )
    
    # Locale selection
    locale_options = [
        "en_US", "en_GB", "fr_FR", "de_DE", "es_ES", 
        "it_IT", "ja_JP", "zh_CN", "pt_BR", "ru_RU"
    ]
    locale = st.selectbox(
        "Daten-Locale",
        options=locale_options,
        index=3,  # Setting default to German (de_DE)
        help="Die Locale bestimmt den Stil und das Format der generierten Daten"
    )
    
    # Random seed for reproducibility
    use_seed = st.checkbox("Zufallsseed verwenden (für reproduzierbare Ergebnisse)", value=False)
    seed = None
    if use_seed:
        seed = st.number_input("Zufallsseed", min_value=0, max_value=999999, value=42)
    
    # Export format
    export_format = st.radio(
        "Exportformat",
        options=["CSV", "JSON"],
        index=0
    )
    
    st.divider()
    
    st.markdown("### Über")
    st.markdown("""
    Dieses Tool generiert synthetische Daten mit der Faker-Bibliothek.
    Die Daten werden zufällig erzeugt und basieren nicht auf realen Personen.
    """)

# Main content area
st.header("1. Felder auswählen und konfigurieren")

# Field selection
field_cols = st.columns(3)

# Initialize selected fields in session state if not present
if 'selected_fields' not in st.session_state:
    st.session_state.selected_fields = {
        "username": True,
        "email": True,
        "password": True, 
        "full_name": True,
        "street_address": True,
        "city": True,
        "zip_code": True,
        "country": True,
        "phone_number": True
    }

# Group fields by category for better organization
field_categories = {
    "Identität": ["username", "email", "password", "full_name"],
    "Adresse": ["street_address", "city", "state", "zip_code", "country"],
    "Kontakt": ["phone_number", "job_title", "company"],
    "Persönlich": ["date_of_birth", "gender", "credit_card"],
    "Internet": ["user_agent", "ipv4", "ipv6", "mac_address"],
    "Sonstiges": ["uuid", "color", "currency_code"]
}

# Create tabs for each category
tabs = st.tabs(list(field_categories.keys()))

# Initialize configuration in session state if not present
if 'field_config' not in st.session_state:
    st.session_state.field_config = {}

# Populate tabs with field checkboxes and config options
for i, (category, fields) in enumerate(field_categories.items()):
    with tabs[i]:
        for field in fields:
            col1, col2 = st.columns([1, 3])
            
            with col1:
                # Set default for fields not in session state yet
                if field not in st.session_state.selected_fields:
                    st.session_state.selected_fields[field] = False
                
                # Create checkbox for field selection
                st.session_state.selected_fields[field] = st.checkbox(
                    field_definitions[field]["display_name"], 
                    value=st.session_state.selected_fields[field],
                    key=f"checkbox_{field}"
                )
            
            # Only show configuration if the field is selected
            if st.session_state.selected_fields[field]:
                with col2:
                    # Initialize config for this field if not present
                    if field not in st.session_state.field_config:
                        st.session_state.field_config[field] = {}
                    
                    # Get field definition
                    definition = field_definitions[field]
                    
                    # Create configuration options based on field type
                    for param, param_config in definition.get("params", {}).items():
                        param_type = param_config["type"]
                        param_default = param_config.get("default")
                        param_label = param_config.get("label", param)
                        param_help = param_config.get("help", "")
                        
                        # Initialize parameter if not present
                        if param not in st.session_state.field_config[field]:
                            st.session_state.field_config[field][param] = param_default
                        
                        # Create appropriate input widget based on parameter type
                        if param_type == "int":
                            st.session_state.field_config[field][param] = st.number_input(
                                param_label,
                                min_value=param_config.get("min", 1),
                                max_value=param_config.get("max", 100),
                                value=st.session_state.field_config[field][param],
                                help=param_help,
                                key=f"{field}_{param}"
                            )
                        elif param_type == "float":
                            st.session_state.field_config[field][param] = st.slider(
                                param_label,
                                min_value=param_config.get("min", 0.0),
                                max_value=param_config.get("max", 1.0),
                                value=st.session_state.field_config[field][param],
                                help=param_help,
                                key=f"{field}_{param}"
                            )
                        elif param_type == "bool":
                            st.session_state.field_config[field][param] = st.checkbox(
                                param_label,
                                value=st.session_state.field_config[field][param],
                                help=param_help,
                                key=f"{field}_{param}"
                            )
                        elif param_type == "select":
                            st.session_state.field_config[field][param] = st.selectbox(
                                param_label,
                                options=param_config.get("options", []),
                                index=param_config.get("options", []).index(st.session_state.field_config[field][param]) if st.session_state.field_config[field][param] in param_config.get("options", []) else 0,
                                help=param_help,
                                key=f"{field}_{param}"
                            )
                        elif param_type == "string":
                            st.session_state.field_config[field][param] = st.text_input(
                                param_label,
                                value=st.session_state.field_config[field][param],
                                help=param_help,
                                key=f"{field}_{param}"
                            )

# Generate button
st.header("2. Daten generieren und Vorschau anzeigen")
generate_button = st.button("Daten generieren", type="primary", use_container_width=True)

# Check if any fields are selected
selected_field_names = [f for f, v in st.session_state.selected_fields.items() if v]

if not selected_field_names:
    st.warning("Bitte wählen Sie mindestens ein Feld aus, um Daten zu generieren.")
    st.stop()

# Generate data when the button is clicked
if generate_button:
    with st.spinner("Daten werden generiert..."):
        # Get the fields that are selected
        selected_fields_config = {
            field: st.session_state.field_config.get(field, {})
            for field in selected_field_names
        }
        
        # Generate the data
        try:
            df = generate_data(
                selected_fields_config, 
                num_records=num_records, 
                locale=locale,
                seed=seed
            )
            
            # Store the dataframe in session state
            st.session_state.generated_df = df
            
            # Add success message
            st.success(f"{num_records} Datensätze erfolgreich generiert!")
        except Exception as e:
            st.error(f"Fehler bei der Datengenerierung: {str(e)}")
            st.stop()

# Display the generated data if available
if 'generated_df' in st.session_state:
    # Display stats
    df = st.session_state.generated_df
    st.subheader("Datensatz-Vorschau")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Anzahl Datensätze", df.shape[0])
    with col2:
        st.metric("Anzahl Felder", df.shape[1])
    with col3:
        memory_usage = df.memory_usage(deep=True).sum()
        if memory_usage < 1024:
            memory_str = f"{memory_usage} Bytes"
        elif memory_usage < 1024 * 1024:
            memory_str = f"{memory_usage/1024:.1f} KB"
        else:
            memory_str = f"{memory_usage/(1024*1024):.1f} MB"
        st.metric("Speichernutzung", memory_str)
    
    # Display the dataframe
    st.dataframe(df, height=400)
    
    # Create a download button
    st.header("3. Generierte Daten herunterladen")
    
    if export_format == "CSV":
        csv_data = export_to_csv(df)
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        st.download_button(
            label="CSV herunterladen",
            data=csv_data,
            file_name=f"testdaten_{timestamp}.csv",
            mime="text/csv",
            use_container_width=True
        )
    else:  # JSON
        json_data = export_to_json(df)
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        st.download_button(
            label="JSON herunterladen",
            data=json_data,
            file_name=f"testdaten_{timestamp}.json",
            mime="application/json",
            use_container_width=True
        )
