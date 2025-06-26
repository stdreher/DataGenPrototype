import streamlit as st
import pandas as pd
import numpy as np
import time
import datetime
import base64
from io import StringIO, BytesIO

from pseudonymize_utils import pseudonymize_data, get_pseudonymization_methods
from export_utils import export_to_csv

# Set page config
st.set_page_config(
    page_title="Daten Pseudonymisierung",
    page_icon="🔒",
    layout="wide",
)

# Add custom CSS for animation
st.markdown("""
<style>
@keyframes lock-animation {
    0% { transform: rotate(0deg) translateY(0); font-size: 2em; }
    25% { transform: rotate(180deg) translateY(-20px); font-size: 3em; }
    50% { transform: rotate(360deg) translateY(0); font-size: 4em; }
    75% { transform: rotate(540deg) translateY(-20px); font-size: 3em; }
    100% { transform: rotate(720deg) translateY(0); font-size: 2em; }
}

.lock-animation {
    display: inline-block;
    animation: lock-animation 1.5s ease-in-out;
}

.lock-container {
    text-align: center;
    padding: 20px;
    height: 100px;
    display: flex;
    align-items: center;
    justify-content: center;
}

.lock-icon {
    font-size: 2em;
}
</style>
""", unsafe_allow_html=True)

# Main page title
st.title("🔒 Daten Pseudonymisierung (DSGVO-konform)")
st.markdown("""
Laden Sie echte Daten hoch und pseudonymisieren Sie diese gemäß DSGVO-Anforderungen.
Wählen Sie die zu pseudonymisierenden Felder und die gewünschten Methoden aus.
""")

# Initialize session states for pseudonymization
if 'uploaded_data' not in st.session_state:
    st.session_state.uploaded_data = None
if 'pseudonymized_data' not in st.session_state:
    st.session_state.pseudonymized_data = None
if 'pseudo_config' not in st.session_state:
    st.session_state.pseudo_config = {}
if 'pseudo_selections' not in st.session_state:
    st.session_state.pseudo_selections = {}

# 1. Data Upload Section
st.header("1. Daten hochladen")

upload_col1, upload_col2 = st.columns([2,1])

with upload_col1:
    uploaded_file = st.file_uploader(
        "Wählen Sie eine CSV- oder Excel-Datei mit Ihren zu pseudonymisierenden Daten",
        type=["csv", "xlsx", "xls"],
        help="Unterstützte Formate: CSV, Excel (.xlsx, .xls)"
    )
    
    if uploaded_file is not None:
        try:
            # Try to determine file type from extension
            file_extension = uploaded_file.name.split('.')[-1].lower()
            
            if file_extension == 'csv':
                # Offer options for CSV parsing
                col1, col2 = st.columns(2)
                with col1:
                    delimiter = st.selectbox(
                        "Trennzeichen",
                        options=[",", ";", "\\t", "|"],
                        index=0,
                        help="Das Zeichen, das Felder in der CSV-Datei trennt"
                    )
                    # Replace literal '\t' with actual tab character
                    if delimiter == "\\t":
                        delimiter = "\t"
                with col2:
                    encoding = st.selectbox(
                        "Zeichenkodierung",
                        options=["utf-8", "utf-8-sig", "latin1", "iso-8859-1"],
                        index=0,
                        help="Die Zeichenkodierung der Datei"
                    )
                
                # Parse the CSV file
                data = pd.read_csv(uploaded_file, sep=delimiter, encoding=encoding)
                
            else:  # Excel file
                # Show sheet selection if it's an Excel file
                data = pd.read_excel(uploaded_file, sheet_name=None)
                sheet_names = list(data.keys())
                
                selected_sheet = st.selectbox(
                    "Tabellenblatt auswählen",
                    options=sheet_names,
                    index=0
                )
                
                # Get the selected sheet
                data = data[selected_sheet]
            
            # Store the data in session state
            st.session_state.uploaded_data = data
            
            # Display success message and data preview
            st.success(f"✅ Datei '{uploaded_file.name}' erfolgreich geladen!")
            
            # Data stats
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Anzahl Datensätze", data.shape[0])
            with col2:
                st.metric("Anzahl Felder", data.shape[1])
            with col3:
                memory_usage = data.memory_usage(deep=True).sum()
                if memory_usage < 1024:
                    memory_str = f"{memory_usage} Bytes"
                elif memory_usage < 1024 * 1024:
                    memory_str = f"{memory_usage/1024:.1f} KB"
                else:
                    memory_str = f"{memory_usage/(1024*1024):.1f} MB"
                st.metric("Speichernutzung", memory_str)
            
            # Preview the data
            st.subheader("Datenvorschau")
            st.dataframe(data.head(5), height=200)
            
        except Exception as e:
            st.error(f"Fehler beim Laden der Datei: {str(e)}")
            st.session_state.uploaded_data = None

with upload_col2:
    st.markdown("### Über Pseudonymisierung")
    st.info("""
    **Pseudonymisierung** ist ein Verfahren, bei dem personenbezogene Daten so verarbeitet werden, 
    dass sie ohne zusätzliche Informationen nicht mehr einer Person zugeordnet werden können.
    
    Gemäß DSGVO (Art. 4) ist dies eine wichtige Maßnahme zum Datenschutz.
    """)
    
# 2. Field selection and method configuration (only if data is uploaded)
if st.session_state.uploaded_data is not None:
    st.header("2. Felder und Pseudonymisierungsmethoden auswählen")
    
    # Get available pseudonymization methods
    pseudo_methods = get_pseudonymization_methods()
    
    # Create tabs for different method groups
    method_tabs = st.tabs(list(pseudo_methods.keys()))
    
    # Get column names from the uploaded data
    columns = list(st.session_state.uploaded_data.columns)
    
    # For each pseudonymization method, create a tab with column selection
    for i, (method_name, method_desc) in enumerate(pseudo_methods.items()):
        with method_tabs[i]:
            st.markdown(f"**{method_desc}**")
            
            # Multi-select for columns to apply this method to
            selected_columns = st.multiselect(
                f"Wählen Sie Spalten für '{method_name}'",
                options=columns,
                default=[col for col, method in st.session_state.pseudo_selections.items() 
                         if method == method_name and col in columns],
                help=f"Wählen Sie die Spalten aus, die mit der Methode '{method_name}' pseudonymisiert werden sollen"
            )
            
            # Store the selections in session state
            # First, remove any previous selections for this method
            st.session_state.pseudo_selections = {
                k: v for k, v in st.session_state.pseudo_selections.items() 
                if v != method_name or k not in columns
            }
            
            # Then add the new selections
            for col in selected_columns:
                st.session_state.pseudo_selections[col] = method_name
            
            # Display additional configuration options based on the method
            if method_name == "mask" and selected_columns:
                col1, col2, col3 = st.columns(3)
                with col1:
                    show_first = st.number_input(
                        "Erste Zeichen anzeigen",
                        min_value=0,
                        max_value=10,
                        value=st.session_state.pseudo_config.get("mask", {}).get("show_first", 2),
                        help="Anzahl der ersten Zeichen, die sichtbar bleiben"
                    )
                with col2:
                    show_last = st.number_input(
                        "Letzte Zeichen anzeigen",
                        min_value=0,
                        max_value=10,
                        value=st.session_state.pseudo_config.get("mask", {}).get("show_last", 2),
                        help="Anzahl der letzten Zeichen, die sichtbar bleiben"
                    )
                with col3:
                    mask_char = st.text_input(
                        "Maskierungszeichen",
                        value=st.session_state.pseudo_config.get("mask", {}).get("char", "*"),
                        max_chars=1,
                        help="Zeichen, das zur Maskierung verwendet wird"
                    )
                
                # Store mask configuration
                st.session_state.pseudo_config["mask"] = {
                    "show_first": show_first,
                    "show_last": show_last,
                    "char": mask_char if mask_char else "*"
                }
            
            elif method_name == "offset" and selected_columns:
                col1, col2 = st.columns(2)
                with col1:
                    numeric_offset = st.number_input(
                        "Numerischer Offset",
                        value=st.session_state.pseudo_config.get("offset", {}).get("numeric_offset", 5),
                        help="Wert, um den numerische Felder verschoben werden"
                    )
                with col2:
                    date_offset = st.number_input(
                        "Datums-Offset (Tage)",
                        value=st.session_state.pseudo_config.get("offset", {}).get("date_offset_days", 10),
                        help="Anzahl der Tage, um die Datumsfelder verschoben werden"
                    )
                
                # Store offset configuration
                st.session_state.pseudo_config["offset"] = {
                    "numeric_offset": numeric_offset,
                    "date_offset_days": date_offset
                }
            
            elif method_name == "replace" and selected_columns:
                preserve_format = st.checkbox(
                    "Format beibehalten (Groß-/Kleinschreibung)",
                    value=st.session_state.pseudo_config.get("replace", {}).get("preserve_format", True),
                    help="Bei Aktivierung wird die Groß-/Kleinschreibung beim Ersetzen beibehalten"
                )
                
                # Store replace configuration
                st.session_state.pseudo_config["replace"] = {
                    "preserve_format": preserve_format
                }
    
    # Show a summary of the selected pseudonymization methods
    if st.session_state.pseudo_selections:
        st.subheader("Zusammenfassung der Pseudonymisierung")
        
        # Create a table of selected columns and methods
        summary_data = {
            "Spalte": list(st.session_state.pseudo_selections.keys()),
            "Methode": list(st.session_state.pseudo_selections.values())
        }
        summary_df = pd.DataFrame(summary_data)
        
        st.table(summary_df)
        
        # Button to apply pseudonymization
        if st.button("Pseudonymisierung anwenden", type="primary"):
            # Create a container for the animation
            pseudo_animation = st.empty()
            
            # Show the animated lock
            pseudo_animation.markdown("""
            <div class="lock-container">
                <div class="lock-icon lock-animation">🔒</div>
            </div>
            """, unsafe_allow_html=True)
            
            try:
                # Apply pseudonymization using the utility function
                pseudonymized_df = pseudonymize_data(
                    st.session_state.uploaded_data,
                    st.session_state.pseudo_selections,
                    st.session_state.pseudo_config,
                    locale="de_DE"  # Use default locale for consistency
                )
                
                # Store the result in session state
                st.session_state.pseudonymized_data = pseudonymized_df
                
                # Clear the animation
                pseudo_animation.empty()
                
                # Show success message
                st.success("✅ Daten erfolgreich pseudonymisiert!")
                
            except Exception as e:
                # Clear the animation
                pseudo_animation.empty()
                
                # Show error message
                st.error(f"Fehler bei der Pseudonymisierung: {str(e)}")
        
    else:
        st.info("Bitte wählen Sie mindestens eine Spalte für die Pseudonymisierung aus.")
    
    # 3. Result display and download (only if data has been pseudonymized)
    if st.session_state.pseudonymized_data is not None:
        st.header("3. Pseudonymisierte Daten")
        
        # Compare original and pseudonymized data
        compare_col1, compare_col2 = st.columns(2)
        
        with compare_col1:
            st.subheader("Original Daten")
            st.dataframe(st.session_state.uploaded_data, height=300)
        
        with compare_col2:
            st.subheader("Pseudonymisierte Daten")
            st.dataframe(st.session_state.pseudonymized_data, height=300)
        
        # Download options
        st.subheader("Daten herunterladen")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # CSV download
            csv_data = export_to_csv(st.session_state.pseudonymized_data)
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            
            st.download_button(
                label="Als CSV herunterladen",
                data=csv_data,
                file_name=f"pseudonymisiert_{timestamp}.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        with col2:
            # Excel download
            try:
                excel_buffer = BytesIO()
                st.session_state.pseudonymized_data.to_excel(excel_buffer, index=False)
                excel_buffer.seek(0)  # Go back to the start of the buffer
                excel_data = excel_buffer.getvalue()
                
                st.download_button(
                    label="Als Excel herunterladen",
                    data=excel_data,
                    file_name=f"pseudonymisiert_{timestamp}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )
            except Exception as e:
                st.error(f"Excel-Export nicht verfügbar: {str(e)}")
                st.info("Bitte verwenden Sie den CSV-Export als Alternative.")
        
        # Add GDPR compliance information
        st.info("""
        **DSGVO-Hinweis**: Die pseudonymisierten Daten erfüllen die Anforderungen der DSGVO, 
        solange sie nicht mit zusätzlichen Datenquellen zusammengeführt werden können, 
        die eine Re-Identifizierung ermöglichen.
        """)
        
        # Option to reset/clear the pseudonymized data
        if st.button("Zurücksetzen", type="secondary"):
            # Create a container for the lock animation
            reset_lock_container = st.empty()
            
            # Show the animated lock
            reset_lock_container.markdown("""
            <div class="lock-container">
                <div class="lock-icon lock-animation">🔄</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Clear pseudonymized data
            st.session_state.pseudonymized_data = None
            
            # Clear the animation
            reset_lock_container.empty()
            
            st.success("🔄 Pseudonymisierungsdaten zurückgesetzt!")
            time.sleep(0.5)
            st.rerun()