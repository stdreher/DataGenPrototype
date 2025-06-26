import streamlit as st
import pandas as pd
import datetime
import json
from sqlalchemy import select, insert, update, delete
from database_utils import Session, community_showcases, saved_datasets

# Set page config
st.set_page_config(
    page_title="Community Showcase | Testdaten Generator",
    page_icon="🎲",
    layout="wide",
)

# Title and introduction
st.title("🌟 Community Showcase")
st.write("Entdecken und teilen Sie interessante Datenszenarien aus der Community")

# Function to load all showcases with fallback examples
def get_all_showcases():
    try:
        session = Session()
        try:
            stmt = select(
                community_showcases.c.id,
                community_showcases.c.title,
                community_showcases.c.description,
                community_showcases.c.author,
                community_showcases.c.category,
                community_showcases.c.tags,
                community_showcases.c.dataset_id,
                community_showcases.c.upvotes,
                community_showcases.c.created_at,
                community_showcases.c.is_featured
            )
            result = session.execute(stmt).fetchall()
            
            showcases = []
            for row in result:
                showcase = {
                    "id": row.id,
                    "title": row.title,
                    "description": row.description,
                    "author": row.author,
                    "category": row.category,
                    "tags": json.loads(row.tags) if row.tags else [],
                    "dataset_id": row.dataset_id,
                    "upvotes": row.upvotes,
                    "created_at": row.created_at,
                    "is_featured": row.is_featured
                }
                showcases.append(showcase)
            
            return pd.DataFrame(showcases) if showcases else get_sample_showcases_df()
        except Exception as e:
            st.warning(f"Datenbankverbindung nicht verfügbar. Zeige Beispiel-Showcases an.")
            return get_sample_showcases_df()
        finally:
            session.close()
    except Exception as e:
        st.warning("Datenbankverbindung nicht verfügbar. Zeige Beispiel-Showcases an.")
        return get_sample_showcases_df()

# Function to provide sample showcases when database is unavailable
def get_sample_showcases_df():
    sample_showcases = [
        {
            "id": 1,
            "title": "E-Commerce Kundendatenbank mit realistischen Kaufmustern",
            "description": "Diese E-Commerce-Datenkonfiguration erzeugt realistische Kundendaten für einen Online-Shop, komplett mit Adressen, Kontaktinformationen und Kaufmustern.",
            "author": "Markus Weber",
            "category": "E-Commerce",
            "tags": ["user-profiles", "payments", "e-commerce"],
            "dataset_id": None,
            "upvotes": 15,
            "created_at": "2025-05-21",
            "is_featured": 1
        },
        {
            "id": 2,
            "title": "Gesundheitsdaten mit DSGVO-konformer Pseudonymisierung",
            "description": "Diese Konfiguration erzeugt pseudonymisierte Patientendaten, die für Tests von Gesundheits-IT-Systemen verwendet werden können, während gleichzeitig die DSGVO-Anforderungen eingehalten werden.",
            "author": "Dr. Julia Fischer",
            "category": "Gesundheitswesen",
            "tags": ["health-data", "DSGVO", "pseudonymization"],
            "dataset_id": None,
            "upvotes": 23,
            "created_at": "2025-05-21",
            "is_featured": 1
        },
        {
            "id": 3,
            "title": "Multi-Locale Testdaten für internationale Websites",
            "description": "Diese Datenkonfiguration erzeugt Testdaten für internationale Websites und Anwendungen mit Unterstützung für mehrere Locales.",
            "author": "Sandra Müller",
            "category": "Web-Anwendungen",
            "tags": ["multi-language", "i18n", "l10n"],
            "dataset_id": None,
            "upvotes": 12,
            "created_at": "2025-05-21",
            "is_featured": 0
        }
    ]
    return pd.DataFrame(sample_showcases)

# Function to get a showcase by ID
def get_showcase_by_id(showcase_id):
    try:
        # For sample showcases, return the appropriate one
        sample_showcases_df = get_sample_showcases_df()
        if showcase_id in sample_showcases_df['id'].values:
            sample_showcase = sample_showcases_df[sample_showcases_df['id'] == showcase_id].iloc[0].to_dict()
            return sample_showcase
            
        # Otherwise try to fetch from database
        session = Session()
        try:
            stmt = select(
                community_showcases.c.id,
                community_showcases.c.title,
                community_showcases.c.description,
                community_showcases.c.author,
                community_showcases.c.category,
                community_showcases.c.tags,
                community_showcases.c.dataset_id,
                community_showcases.c.upvotes,
                community_showcases.c.created_at,
                community_showcases.c.is_featured
            ).where(community_showcases.c.id == showcase_id)
            
            result = session.execute(stmt).fetchone()
            
            if not result:
                return None
            
            showcase = {
                "id": result.id,
                "title": result.title,
                "description": result.description,
                "author": result.author,
                "category": result.category,
                "tags": json.loads(result.tags) if result.tags else [],
                "dataset_id": result.dataset_id,
                "upvotes": result.upvotes,
                "created_at": result.created_at,
                "is_featured": result.is_featured
            }
            
            return showcase
        except Exception as e:
            st.warning("Datenbankverbindung nicht verfügbar.")
            # Check if we're looking for a sample showcase
            if showcase_id <= 3:  # Our sample showcases have IDs 1-3
                sample_showcases = get_sample_showcases_df()
                sample_showcase = sample_showcases[sample_showcases['id'] == showcase_id]
                if not sample_showcase.empty:
                    return sample_showcase.iloc[0].to_dict()
            return None
        finally:
            session.close()
    except Exception as e:
        st.warning("Fehler beim Zugriff auf die Datenbank.")
        return None

# Function to save a new showcase
def save_showcase(title, description, author, category, tags, dataset_id=None):
    session = Session()
    try:
        tags_json = json.dumps(tags)
        created_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        stmt = insert(community_showcases).values(
            title=title,
            description=description,
            author=author,
            category=category,
            tags=tags_json,
            dataset_id=dataset_id,
            upvotes=0,
            created_at=created_at,
            is_featured=0
        )
        
        result = session.execute(stmt)
        session.commit()
        
        # The ID of the newly inserted showcase is stored in result.inserted_primary_key
        if result.inserted_primary_key and len(result.inserted_primary_key) > 0:
            return result.inserted_primary_key[0]
        return None
    except Exception as e:
        session.rollback()
        st.error(f"Fehler beim Speichern des Showcase: {str(e)}")
        return None
    finally:
        session.close()

# Function to upvote a showcase
def upvote_showcase(showcase_id):
    # For sample showcases, simulate upvote in session state
    sample_showcases_df = get_sample_showcases_df()
    if showcase_id in sample_showcases_df['id'].values:
        # Store upvotes for sample showcases in session state
        if 'sample_showcase_upvotes' not in st.session_state:
            st.session_state.sample_showcase_upvotes = {}
        
        # Initialize if not already tracked
        if showcase_id not in st.session_state.sample_showcase_upvotes:
            upvotes_rows = sample_showcases_df[sample_showcases_df['id'] == showcase_id]
            if not upvotes_rows.empty:
                st.session_state.sample_showcase_upvotes[showcase_id] = upvotes_rows['upvotes'].values[0]
            else:
                st.session_state.sample_showcase_upvotes[showcase_id] = 0
        
        # Increment upvote count
        st.session_state.sample_showcase_upvotes[showcase_id] += 1
        return True
    
    # Try using the database
    try:
        session = Session()
        try:
            # First get the current showcase to get its upvote count
            stmt = select(
                community_showcases.c.id,
                community_showcases.c.upvotes
            ).where(community_showcases.c.id == showcase_id)
            
            showcase = session.execute(stmt).fetchone()
            
            if not showcase:
                return False
            
            # Increment upvotes
            update_stmt = update(community_showcases).where(
                community_showcases.c.id == showcase_id
            ).values(
                upvotes=showcase.upvotes + 1
            )
            
            session.execute(update_stmt)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            st.warning("Datenbankverbindung nicht verfügbar. Upvote konnte nicht gespeichert werden.")
            return False
        finally:
            session.close()
    except Exception as e:
        st.warning("Datenbankverbindung nicht verfügbar.")
        return False

# Function to get a dataset by ID
def get_dataset_by_id(dataset_id):
    session = Session()
    try:
        stmt = select(
            saved_datasets.c.id,
            saved_datasets.c.name,
            saved_datasets.c.description,
            saved_datasets.c.num_records,
            saved_datasets.c.locale,
            saved_datasets.c.fields,
            saved_datasets.c.field_config,
            saved_datasets.c.created_at
        ).where(saved_datasets.c.id == dataset_id)
        
        result = session.execute(stmt).fetchone()
        
        if not result:
            return None
        
        dataset = {
            "id": result.id,
            "name": result.name,
            "description": result.description,
            "num_records": result.num_records,
            "locale": result.locale,
            "fields": json.loads(result.fields) if result.fields else [],
            "field_config": json.loads(result.field_config) if result.field_config else {},
            "created_at": result.created_at
        }
        
        return dataset
    except Exception as e:
        st.error(f"Fehler beim Laden des Datensatzes: {str(e)}")
        return None
    finally:
        session.close()

# Function to get all datasets (for selection)
def get_all_datasets():
    session = Session()
    try:
        stmt = select(
            saved_datasets.c.id,
            saved_datasets.c.name,
            saved_datasets.c.description,
            saved_datasets.c.num_records,
            saved_datasets.c.locale,
            saved_datasets.c.created_at
        )
        result = session.execute(stmt).fetchall()
        
        datasets = []
        for row in result:
            dataset = {
                "id": row.id,
                "name": row.name,
                "description": row.description,
                "num_records": row.num_records,
                "locale": row.locale,
                "created_at": row.created_at
            }
            datasets.append(dataset)
        
        return pd.DataFrame(datasets) if datasets else pd.DataFrame()
    except Exception as e:
        st.error(f"Fehler beim Laden der Datensätze: {str(e)}")
        return pd.DataFrame()
    finally:
        session.close()

# Sidebar for navigation
with st.sidebar:
    page = st.radio("Navigation", ["Showcases durchsuchen", "Neues Showcase hinzufügen"])

# Main content
if page == "Showcases durchsuchen":
    # Check if a showcase ID is in the session state for viewing details
    if "view_showcase_id" in st.session_state:
        showcase_id = int(st.session_state.view_showcase_id)  # Convert to Python int
        showcase = get_showcase_by_id(showcase_id)
        
        if showcase:
            # Show detailed view of the selected showcase
            st.header(showcase["title"])
            
            # Show featured badge if applicable
            if showcase["is_featured"] == 1:  # Check for value 1 (featured)
                st.markdown('<span style="background-color: gold; color: black; padding: 5px 10px; border-radius: 5px;">⭐ Featured</span>', unsafe_allow_html=True)
            
            # Showcase details
            st.subheader("Beschreibung")
            st.write(showcase["description"])
            
            # Author and metadata
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"👤 Autor: {showcase['author']}")
                st.write(f"📂 Kategorie: {showcase['category']}")
            
            with col2:
                st.write(f"⭐ Upvotes: {showcase['upvotes']}")
                st.write(f"📅 Erstellt am: {showcase['created_at']}")
            
            # Tags display
            if showcase["tags"]:
                st.subheader("Tags")
                tags_html = ' '.join([f'<span style="background-color: #f0f2f6; border-radius: 10px; padding: 5px 10px; margin-right: 8px;">{tag}</span>' for tag in showcase["tags"]])
                st.markdown(tags_html, unsafe_allow_html=True)
            
            # Show associated dataset if available
            if showcase["dataset_id"]:
                st.subheader("Verknüpfter Datensatz")
                dataset = get_dataset_by_id(showcase["dataset_id"])
                
                if dataset:
                    st.write(f"Name: {dataset['name']}")
                    st.write(f"Beschreibung: {dataset['description']}")
                    st.write(f"Anzahl der Datensätze: {dataset['num_records']}")
                    st.write(f"Locale: {dataset['locale']}")
                    
                    # Show fields
                    if dataset["fields"]:
                        st.write("Felder:")
                        fields_list = ", ".join(dataset["fields"])
                        st.write(fields_list)
                    
                    # Button to load this dataset in the generator
                    if st.button("Diese Konfiguration im Generator laden"):
                        st.session_state.load_dataset_id = dataset["id"]
                        st.switch_page("pages/1_Testdaten_Generator.py")
                else:
                    st.write("Der verknüpfte Datensatz ist nicht mehr verfügbar.")
            
            # Upvote button
            if st.button("👍 Upvote"):
                if upvote_showcase(int(showcase_id)):
                    st.success("Upvote erfolgreich!")
                    st.rerun()
            
            # Back button
            if st.button("Zurück zur Übersicht"):
                del st.session_state.view_showcase_id
                st.rerun()
        else:
            st.error("Showcase nicht gefunden.")
            # Back button if showcase doesn't exist
            if st.button("Zurück zur Übersicht"):
                del st.session_state.view_showcase_id
                st.rerun()
    else:
        # List all showcases
        st.subheader("Vorhandene Showcases")
        
        showcases_df = get_all_showcases()
        
        if not showcases_df.empty:
            # Display showcases in a nice grid
            for i in range(0, len(showcases_df), 2):
                cols = st.columns(2)
                for j in range(2):
                    if i + j < len(showcases_df):
                        with cols[j]:
                            showcase = showcases_df.iloc[i + j]
                            with st.container(border=True):
                                st.subheader(showcase["title"])
                                st.write(f"👤 {showcase['author']} | 📂 {showcase['category']}")
                                
                                # Show a preview of the description
                                description = showcase["description"]
                                if len(description) > 100:
                                    st.write(description[:100] + "...")
                                else:
                                    st.write(description)
                                
                                # Show tags
                                if len(showcase["tags"]) > 0:
                                    tags_html = ' '.join([f'<span style="background-color: #f0f2f6; border-radius: 10px; padding: 2px 8px; margin-right: 5px;">{tag}</span>' for tag in showcase["tags"]])
                                    st.markdown(tags_html, unsafe_allow_html=True)
                                
                                # Stats and actions
                                col1, col2 = st.columns([1, 1])
                                with col1:
                                    st.write(f"⭐ {showcase['upvotes']} Upvotes")
                                
                                with col2:
                                    # Button to view details
                                    if st.button("Details", key=f"view_{showcase['id']}"):
                                        st.session_state.view_showcase_id = int(showcase["id"])
                                        st.rerun()
        else:
            st.info("Noch keine Showcases vorhanden. Fügen Sie das erste Showcase hinzu!")

elif page == "Neues Showcase hinzufügen":
    st.header("Neues Showcase hinzufügen")
    
    with st.form("showcase_form"):
        # Basic info
        title = st.text_input("Titel", max_chars=100)
        description = st.text_area("Beschreibung", height=150, max_chars=2000)
        author = st.text_input("Ihr Name/Pseudonym", max_chars=50)
        
        # Category
        categories = [
            "Web-Anwendungen",
            "E-Commerce",
            "CRM",
            "Finanzen",
            "Gesundheitswesen",
            "Bildung",
            "IoT",
            "Sonstige"
        ]
        category = st.selectbox("Kategorie", categories)
        
        # Tags
        common_tags = [
            "address", "user-profiles", "payments", "e-commerce", 
            "health-data", "financial", "DSGVO", "education", 
            "performance-test", "large-dataset", "multi-language"
        ]
        selected_tags = st.multiselect("Tags", common_tags)
        custom_tags = st.text_input("Eigene Tags (durch Kommas getrennt)")
        
        # Dataset linking
        st.subheader("Datensatz verknüpfen (optional)")
        
        # Get all datasets
        datasets_df = get_all_datasets()
        
        dataset_id = None
        if not datasets_df.empty:
            # Create a list of options for the selectbox
            dataset_options = ["Kein Datensatz"] + [f"{row['id']}: {row['name']}" for _, row in datasets_df.iterrows()]
            selected_dataset = st.selectbox("Datensatz", dataset_options)
            
            # Extract the ID if a dataset was selected
            if selected_dataset != "Kein Datensatz":
                dataset_id = int(selected_dataset.split(":")[0])
        else:
            st.info("Keine Datensätze vorhanden. Erstellen Sie zuerst einen Datensatz im Generator.")
        
        # Submit button
        submitted = st.form_submit_button("Showcase speichern")
        
        # Form handling
        if submitted:
            if not title:
                st.error("Bitte geben Sie einen Titel ein.")
            elif not description:
                st.error("Bitte geben Sie eine Beschreibung ein.")
            elif not author:
                st.error("Bitte geben Sie einen Autor ein.")
            else:
                # Process tags
                all_tags = selected_tags.copy()
                if custom_tags:
                    all_tags.extend([tag.strip() for tag in custom_tags.split(",") if tag.strip()])
                
                # Save the showcase
                new_id = save_showcase(
                    title=title,
                    description=description,
                    author=author,
                    category=category,
                    tags=all_tags,
                    dataset_id=dataset_id
                )
                
                if new_id:
                    st.session_state.new_showcase_id = new_id
                    st.success(f"Showcase erfolgreich gespeichert mit ID: {new_id}")
                else:
                    st.error("Fehler beim Speichern des Showcase.")

# Display button to view the newly created showcase outside of the form
if "new_showcase_id" in st.session_state:
    new_id = st.session_state.new_showcase_id
    if st.button("Zum neuen Showcase anzeigen"):
        st.session_state.view_showcase_id = new_id
        del st.session_state.new_showcase_id
        st.session_state.page = "Showcases durchsuchen"
        st.rerun()

# Footer info
st.divider()
st.info("""
**Community Guidelines**:
- Teilen Sie interessante und nützliche Datenszenarien.
- Respektieren Sie die Privatsphäre - keine echten personenbezogenen Daten.
- Geben Sie hilfreiche Beschreibungen, damit andere von Ihren Szenarien lernen können.
- Upvoten Sie die Showcases, die Sie hilfreich finden.
""")