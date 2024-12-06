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
from ifc_Berechnungen.Berechnungen import Berechnung_GE_THG
from ifc_Berechnungen.Totalwerte import add_totals_and_group_by_material
from ifc_Datenvisualisierung.Donut import create_interactive_donut_chart

def main():
    st.title("Rohbau | IFC-Ökobilanzierung")
    st.write("Lade das IFC deines Rohbaumodells hoch, um eine erste Ökobilanzierung deines Projekts zu erhalten.")

    # Datei-Upload
    uploaded_file = st.file_uploader("IFC-Datei hier hochladen", type=["ifc"])

    if uploaded_file is not None:
        # Datei speichern
        file_path = save_uploaded_file(uploaded_file)

        if file_path:
            st.success(f"IFC-Datei erfolgreich hochgeladen: {uploaded_file.name}")

            # "Start"-Button anzeigen
            if st.button("Ökobilanzierung starten"):
                try:
                    # IFC-Modell laden
                    model = ifcopenshell.open(file_path)

                    # Daten analysieren
                    wall_data = extract_wall_base_quantities_with_psets(model)
                    slab_data = extract_slab_base_quantities_with_psets(model)
                    material_data = extract_materials_for_all_entities(model)

                    # Ergebnisse zusammenführen
                    IFC_Auszug_MAT = merge_wall_slab_materials(wall_data, slab_data, material_data)

                    # Temporäre Pfade für die Zwischen- und Ergebnisdateien
                    temp_ifc_path = "IFC_Auszug_MAT.xlsx"
                    enriched_output_path = "IFC_MAT_Config.xlsx"
                    final_output_path = "IFC_MAT_Config_with_GE_THG.xlsx"
                    final_output_path_with_totals = "IFC_TAB_Ökobilanzierung.xlsx"

                    # Tabelle IFC_Auszug_MAT speichern
                    with pd.ExcelWriter(temp_ifc_path, engine="openpyxl") as writer:
                        IFC_Auszug_MAT.to_excel(writer, index=False, sheet_name="Analysis")

                    # Konfigurationsdateien laden
                    config_path = "Material_Config.xlsx"
                    kbob_path = "GE_THG_MAT.xlsx"

                    # Tabelle erweitern mit KBOB-Werten
                    enrich_ifc_data(
                        config_file_path=config_path,
                        kbob_file_path=kbob_path,
                        ifc_file_path=temp_ifc_path,
                        output_file_path=enriched_output_path
                    )

                    # Berechnungen für GE und THG durchführen
                    Berechnung_GE_THG(enriched_output_path, final_output_path)

                    # Ergebnisdatei mit Totals ergänzen
                    add_totals_and_group_by_material(final_output_path, final_output_path_with_totals)

                    # Ergebnisdatei mit Totals laden
                    totals_data = pd.read_excel(final_output_path_with_totals, sheet_name='Totals')
                    st.success("Ökobilanzierung abgeschlossen! Die Tabelle ist bereit.")
                    
                    # Graue Energie Diagramm
                    ge_total = totals_data.loc[totals_data['Material'] == 'All Materials', 'GE Total'].values[0]
                    ge_materials = totals_data[totals_data['Material'] != 'All Materials'][['Material', 'GE Total']]
                    ge_donut = create_interactive_donut_chart(
                        values=ge_materials['GE Total'],
                        labels=ge_materials['Material'],
                        total_value=ge_total,
                        title="Graue Energie (kWh_oil_eq)",
                        unit="kWh_oil_eq"
                    )
                    st.plotly_chart(ge_donut)

                    # Treibhausgasemissionen Diagramm
                    thg_total = totals_data.loc[totals_data['Material'] == 'All Materials', 'THG Total'].values[0]
                    thg_materials = totals_data[totals_data['Material'] != 'All Materials'][['Material', 'THG Total']]
                    thg_donut = create_interactive_donut_chart(
                        values=thg_materials['THG Total'],
                        labels=thg_materials['Material'],
                        total_value=thg_total,
                        title="Treibhausgasemissionen (kg_CO2_eq)",
                        unit="kg_CO2_eq"
                    )
                    st.plotly_chart(thg_donut)

                    # Download-Button für die angereicherte Tabelle
                    with open(final_output_path_with_totals, "rb") as f:
                        st.download_button(
                            label="📥 Excel-Tabelle Ökobilanzierung herunterladen",
                            data=f,
                            file_name="IFC_TAB_Ökobilanzierung.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        )

                except Exception as e:
                    st.error(f"Es ist ein Fehler aufgetreten: {e}")

                finally:
                    # Temporäre Dateien löschen
                    for temp_file in [temp_ifc_path, enriched_output_path, final_output_path, final_output_path_with_totals]:
                        if os.path.exists(temp_file):
                            os.remove(temp_file)

                # Datei löschen
                delete_file(file_path)
        else:
            st.error("Fehler beim Speichern der Datei.")

if __name__ == "__main__":
    main()



