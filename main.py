import os
import streamlit as st
import ifcopenshell
import pandas as pd
from io import BytesIO
from ifc_analyzer.file_handler import save_uploaded_file, delete_file
from ifc_analyzer.ifc_basequantities import extract_slab_base_quantities_with_psets, extract_wall_base_quantities_with_psets, extract_column_base_quantities_with_psets, extract_beam_base_quantities_with_psets
from ifc_analyzer.ifc_material import extract_materials_for_all_entities
from ifc_analyzer.ifc_merge import merge_basequantities_materials
from ifc_Config.Config import enrich_ifc_data
from ifc_Berechnungen.Berechnungen import Berechnung_GE_THG
from ifc_Berechnungen.Totalwerte import add_totals_and_group_by
from ifc_Datenvisualisierung.Donut import create_interactive_donut_chart

def provide_file_for_download(file_bytes, download_filename):
    """
    Stellt eine Datei für den Download bereit.

    Args:
        file_bytes (BytesIO): Die Datei als Bytes-Objekt.
        download_filename (str): Der Name, unter dem die Datei heruntergeladen werden soll.
    """
    st.download_button(
        label="📥 Excel-Tabelle Ökobilanzierung herunterladen",
        data=file_bytes,
        file_name=download_filename,
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

def main():
    st.title("Rohbau | IFC-Ökobilanzierung")
    st.write("Lade das IFC deines Rohbaumodells hoch, um eine erste Ökobilanzierung deines Projekts zu erhalten.")

    # Datei-Upload
    uploaded_file = st.file_uploader("IFC-Datei hier hochladen", type=["ifc"])

    # Button-Zustand initialisieren
    if "analysis_started" not in st.session_state:
        st.session_state["analysis_started"] = False

    if uploaded_file is not None:
        # Datei speichern
        file_path = save_uploaded_file(uploaded_file)

        if file_path:
            st.success(f"IFC-Datei erfolgreich hochgeladen: {uploaded_file.name}")

            # "Start"-Button anzeigen
            if st.button("Ökobilanzierung starten") or st.session_state["analysis_started"]:
                st.session_state["analysis_started"] = True
                
                # Temporäre Pfade für die Zwischen- und Ergebnisdateien
                temp_ifc_path = "IFC_Auszug_MAT.xlsx"
                enriched_output_path = "IFC_MAT_Config.xlsx"
                final_output_path = "IFC_MAT_Config_with_GE_THG.xlsx"
                final_output_path_with_totals = "IFC_TAB_Ökobilanzierung.xlsx"
                
                try:
                    if not st.session_state.get("results_loaded", False):
                        # IFC-Modell laden
                        model = ifcopenshell.open(file_path)

                        # Daten analysieren
                        wall_data = extract_wall_base_quantities_with_psets(model)
                        slab_data = extract_slab_base_quantities_with_psets(model)
                        column_data = extract_column_base_quantities_with_psets(model)
                        beam_data = extract_beam_base_quantities_with_psets(model)
                        material_data = extract_materials_for_all_entities(model)

                        # Ergebnisse zusammenführen
                        IFC_Auszug_MAT = merge_basequantities_materials(wall_data, slab_data, column_data, beam_data, material_data)

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
                        add_totals_and_group_by(final_output_path, final_output_path_with_totals)

                        # Datei in BytesIO laden und im Session-State speichern
                        with open(final_output_path_with_totals, "rb") as f:
                            st.session_state["final_file"] = BytesIO(f.read())

                        # Ergebnisdateien mit Totals laden und im Session-State speichern
                        st.session_state["totals_material_data"] = pd.read_excel(final_output_path_with_totals, sheet_name='Totals_Material')
                        st.session_state["totals_entity_data"] = pd.read_excel(final_output_path_with_totals, sheet_name='Totals_Entity')
                        st.session_state["results_loaded"] = True

                        # Temporäre Dateien löschen
                        os.remove(temp_ifc_path)
                        os.remove(enriched_output_path)
                        os.remove(final_output_path)
                        os.remove(final_output_path_with_totals)

                    # Daten aus dem Session-State abrufen
                    totals_material_data = st.session_state["totals_material_data"]
                    totals_entity_data = st.session_state["totals_entity_data"]

                    st.success("Ökobilanzierung abgeschlossen! Die Tabellen sind bereit.")

                    # Dropdown zur Auswahl des Diagramms
                    diagram_option = st.selectbox(
                        "Wählen Sie die Ansicht für das Diagramm:",
                        [
                            "Graue Energie pro Material",
                            "Treibhausgasemissionen pro Material",
                            "Graue Energie pro EntityType",
                            "Treibhausgasemissionen pro EntityType"
                        ]
                    )

                    if diagram_option == "Graue Energie pro Material":
                        ge_total_material = totals_material_data.loc[totals_material_data['Material'] == 'All Materials', 'GE Total'].values[0]
                        ge_materials = totals_material_data[totals_material_data['Material'] != 'All Materials'][['Material', 'GE Total']]
                        ge_donut_material = create_interactive_donut_chart(
                            values=ge_materials['GE Total'],
                            labels=ge_materials['Material'],
                            total_value=ge_total_material,
                            title="Graue Energie pro Material (kWh_oil_eq)",
                            unit="kWh_oil_eq"
                        )
                        st.plotly_chart(ge_donut_material)

                    elif diagram_option == "Treibhausgasemissionen pro Material":
                        thg_total_material = totals_material_data.loc[totals_material_data['Material'] == 'All Materials', 'THG Total'].values[0]
                        thg_materials = totals_material_data[totals_material_data['Material'] != 'All Materials'][['Material', 'THG Total']]
                        thg_donut_material = create_interactive_donut_chart(
                            values=thg_materials['THG Total'],
                            labels=thg_materials['Material'],
                            total_value=thg_total_material,
                            title="Treibhausgasemissionen pro Material (kg_CO2_eq)",
                            unit="kg_CO2_eq"
                        )
                        st.plotly_chart(thg_donut_material)

                    elif diagram_option == "Graue Energie pro EntityType":
                        ge_total_entity = totals_entity_data.loc[totals_entity_data['EntityType'] == 'All Entities', 'GE Total'].values[0]
                        ge_entities = totals_entity_data[totals_entity_data['EntityType'] != 'All Entities'][['EntityType', 'GE Total']]
                        ge_donut_entity = create_interactive_donut_chart(
                            values=ge_entities['GE Total'],
                            labels=ge_entities['EntityType'],
                            total_value=ge_total_entity,
                            title="Graue Energie pro EntityType (kWh_oil_eq)",
                            unit="kWh_oil_eq"
                        )
                        st.plotly_chart(ge_donut_entity)

                    elif diagram_option == "Treibhausgasemissionen pro EntityType":
                        thg_total_entity = totals_entity_data.loc[totals_entity_data['EntityType'] == 'All Entities', 'THG Total'].values[0]
                        thg_entities = totals_entity_data[totals_entity_data['EntityType'] != 'All Entities'][['EntityType', 'THG Total']]
                        thg_donut_entity = create_interactive_donut_chart(
                            values=thg_entities['THG Total'],
                            labels=thg_entities['EntityType'],
                            total_value=thg_total_entity,
                            title="Treibhausgasemissionen pro EntityType (kg_CO2_eq)",
                            unit="kg_CO2_eq"
                        )
                        st.plotly_chart(thg_donut_entity)

                    # Download-Button für die angereicherte Tabelle
                    if "final_file" in st.session_state:
                        provide_file_for_download(st.session_state["final_file"], "IFC_TAB_Ökobilanzierung.xlsx")

                except Exception as e:
                    st.error(f"Es ist ein Fehler aufgetreten: {e}")
                finally:
                    delete_file(file_path)
        else:
            st.error("Fehler beim Speichern der Datei.")

if __name__ == "__main__":
    main()



