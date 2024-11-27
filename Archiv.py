import streamlit as st
import ifcopenshell
import pandas as pd
from io import BytesIO
from ifc_analyzer.file_handler import save_uploaded_file, delete_file
from ifc_analyzer.ifc_basequantities import extract_slab_base_quantities_with_psets, extract_wall_base_quantities_with_psets
from ifc_analyzer.ifc_material import extract_materials_for_all_entities
from ifc_analyzer.ifc_merge import merge_wall_slab_materials

# Streamlit-UI
def main():
    st.title("IFC-Datei Hochladen und Auswerten")
    st.write("Lade eine IFC-Datei hoch, um die Daten zu analysieren.")

    # Datei-Upload
    uploaded_file = st.file_uploader("Wähle eine IFC-Datei aus", type=["ifc"])

    if uploaded_file is not None:
        # Datei speichern
        file_path = save_uploaded_file(uploaded_file)

        if file_path:
            st.success(f"Datei erfolgreich hochgeladen: {uploaded_file.name}")

            # "Start"-Button anzeigen
            if st.button("Analyse starten"):
                # IFC-Modell laden
                try:
                    model = ifcopenshell.open(file_path)
                except Exception as e:
                    st.error(f"Fehler beim Öffnen der IFC-Datei: {e}")
                    return

                # Daten analysieren
                try:
                    st.info("Analysiere Wände, Decken und Materialien...")
                    wall_data = extract_wall_base_quantities_with_psets(model)
                    slab_data = extract_slab_base_quantities_with_psets(model)
                    material_data = extract_materials_for_all_entities(model)

                    # Ergebnisse zusammenführen
                    IFC_Auszug_MAT = merge_wall_slab_materials(wall_data, slab_data, material_data)

                    # Tabelle als Excel speichern in BytesIO
                    output_buffer = BytesIO()
                    with pd.ExcelWriter(output_buffer, engine="openpyxl") as writer:
                        IFC_Auszug_MAT.to_excel(writer, index=False, sheet_name="Analysis")
                    output_buffer.seek(0)

                    # Ergebnisse anzeigen
                    st.success("Analyse abgeschlossen! Du kannst die Excel-Datei herunterladen.")
                    st.dataframe(IFC_Auszug_MAT)

                    # Download-Button für die Excel-Datei
                    st.download_button(
                        label="📥 Excel-Datei herunterladen",
                        data=output_buffer,
                        file_name="IFC_Auszug_MAT.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    )

                except Exception as e:
                    st.error(f"Fehler bei der Analyse: {e}")
                
                # Datei löschen
                delete_file(file_path)
                st.info("Die hochgeladene Datei wurde nach der Analyse gelöscht.")
        else:
            st.error("Fehler beim Speichern der Datei.")

if __name__ == "__main__":
    main()
