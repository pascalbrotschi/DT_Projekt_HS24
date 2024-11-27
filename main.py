import os
import streamlit as st
import ifcopenshell
import pandas as pd
from io import BytesIO
from ifc_analyzer.file_handler import save_uploaded_file, delete_file
from ifc_analyzer.ifc_basequantities import extract_slab_base_quantities_with_psets, extract_wall_base_quantities_with_psets
from ifc_analyzer.ifc_material import extract_materials_for_all_entities
from ifc_analyzer.ifc_merge import merge_wall_slab_materials
from ifc_Config.Config import enrich_ifc_data

# Streamlit-UI
def main():
    st.title("IFC-Datei Hochladen und Auswerten")
    st.write("Lade eine IFC-Datei hoch, um die Daten zu analysieren und mit KBOB-Werten zu erweitern.")

    # Datei-Upload
    uploaded_file = st.file_uploader("Wähle eine IFC-Datei aus", type=["ifc"])

    if uploaded_file is not None:
        # Datei speichern
        file_path = save_uploaded_file(uploaded_file)

        if file_path:
            st.success(f"Datei erfolgreich hochgeladen: {uploaded_file.name}")

            # "Start"-Button anzeigen
            if st.button("Analyse starten"):
                try:
                    # IFC-Modell laden
                    model = ifcopenshell.open(file_path)
                    st.info("IFC-Datei erfolgreich geladen.")

                    # Daten analysieren
                    st.info("Analysiere Wände, Decken und Materialien...")
                    wall_data = extract_wall_base_quantities_with_psets(model)
                    slab_data = extract_slab_base_quantities_with_psets(model)
                    material_data = extract_materials_for_all_entities(model)

                    # Ergebnisse zusammenführen
                    IFC_Auszug_MAT = merge_wall_slab_materials(wall_data, slab_data, material_data)

                    # Temporäre Pfade für die Zwischen- und Ergebnisdateien
                    temp_ifc_path = "IFC_Auszug_MAT.xlsx"
                    enriched_output_path = "IFC_MAT_Config.xlsx"

                    # Tabelle IFC_Auszug_MAT speichern
                    with pd.ExcelWriter(temp_ifc_path, engine="openpyxl") as writer:
                        IFC_Auszug_MAT.to_excel(writer, index=False, sheet_name="Analysis")

                    # Konfigurationsdateien laden
                    config_path = "Material_Config.xlsx"
                    kbob_path = "GE_THG_MAT.xlsx"

                    # Tabelle erweitern mit KBOB-Werten
                    st.info("Erweitere die Tabelle mit KBOB-Werten...")
                    enrich_ifc_data(
                        config_file_path=config_path,
                        kbob_file_path=kbob_path,
                        ifc_file_path=temp_ifc_path,
                        output_file_path=enriched_output_path
                    )

                    # Ergebnisdatei laden und anzeigen
                    enriched_data = pd.read_excel(enriched_output_path)
                    st.success("Konfiguration abgeschlossen! Die Tabelle ist bereit.")
                    st.dataframe(enriched_data)

                    # Download-Button für die angereicherte Tabelle
                    with open(enriched_output_path, "rb") as f:
                        st.download_button(
                            label="📥 Konfigurierte Tabelle herunterladen",
                            data=f,
                            file_name="IFC_MAT_Config.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        )

                except Exception as e:
                    st.error(f"Fehler bei der Analyse: {e}")

                finally:
                    # Temporäre Dateien löschen
                    for temp_file in [temp_ifc_path, enriched_output_path]:
                        if os.path.exists(temp_file):
                            os.remove(temp_file)
                
                # Datei löschen
                delete_file(file_path)
                st.info("Die hochgeladene Datei wurde nach der Analyse gelöscht.")
        else:
            st.error("Fehler beim Speichern der Datei.")

if __name__ == "__main__":
    main()

