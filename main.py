import streamlit as st
from ifc_analyzer.file_handler import save_uploaded_file, delete_file
from ifc_analyzer.ifc_basequantities import extract_slab_base_quantities_with_psets, extract_wall_base_quantities_with_psets
from ifc_analyzer.ifc_material import extract_materials_for_all_entities
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Streamlit-UI
def start_func():
    st.title("IFC-Datei Hochladen und Auswerten")
    st.write("Lade eine IFC-Datei hoch, um die Anzahl der Wände auszulesen.")

    # Datei-Upload
    uploaded_file = st.file_uploader("Wähle eine IFC-Datei aus", type=["ifc"])

    if uploaded_file is not None:
        # Datei speichern
        file_path = save_uploaded_file(uploaded_file)

        if file_path:
            st.success(f"Datei erfolgreich hochgeladen: {uploaded_file.name}")

            # "Start"-Button anzeigen
            if st.button("Analyse starten"):
                # Anzahl der Wände analysieren
                wall_count = (file_path)

                if wall_count is not None:
                    st.write(f"Anzahl der Wände in der IFC-Datei: {wall_count}")

                # Datei löschen
                delete_file(file_path)
                st.info("Die hochgeladene Datei wurde nach der Analyse gelöscht.")
        else:
            st.error("Fehler beim Speichern der Datei.")

if __name__ == "__main__":
    start_func()
