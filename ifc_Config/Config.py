# Import necessary libraries
import pandas as pd

def enrich_ifc_data(config_file_path, kbob_file_path, ifc_file_path, output_file_path):
    """
    Diese Funktion ordnet gemäß der Konfigurationstabelle die KBOB-Materialien den IFC-Elementen zu
    und hängt die entsprechenden Werte aus der KBOB-Tabelle an.

    Parameter:
    - config_file_path: Pfad zur Konfigurationsdatei (Excel-Datei)
    - kbob_file_path: Pfad zur KBOB-Datenbank (Excel-Datei)
    - ifc_file_path: Pfad zur IFC-Datentabelle (Excel-Datei)
    - output_file_path: Pfad zur Ausgabe-Excel-Datei, in der die angereicherten Daten gespeichert werden
    """

    import pandas as pd

    # Laden der Tabellen
    config_table = pd.read_excel(config_file_path, sheet_name='Objektkatalog')
    kbob_table = pd.read_excel(kbob_file_path, sheet_name='Baumaterialien Matériaux')

     # Debugging: Verfügbare Arbeitsblätter anzeigen
    sheet_names = pd.ExcelFile(ifc_file_path).sheet_names
    print("Verfügbare Arbeitsblätter in IFC-Datei:", sheet_names)

    # Dynamisches Laden des Arbeitsblatts
    try:
        ifc_table = pd.read_excel(ifc_file_path, sheet_name='Analysis')  # Ersetzen Sie 'Analysis' falls notwendig
    except ValueError:
        ifc_table = pd.read_excel(ifc_file_path, sheet_name=sheet_names[0])  # Fallback zum ersten Blatt

    # Umbenennen der Spalten für Konsistenz
    config_table.columns = ['Material_Archicad', 'Material_KBOB']
    kbob_table.columns = [
        'ID-Nummer', 'BAUMATERIALIEN', 'Rohdichte_Flächenmasse',
        'Graue_Energie_Total_kWh_oil_eq', 'CO2_Emissionen_Total_kg_CO2_eq'
    ]
    ifc_table.columns = ['GlobalId', 'EntityType', 'Material', 'Bauteilfläche', 'Width']

    # Zusammenführen der Konfigurationstabelle mit den IFC-Materialien
    ifc_with_kbob = pd.merge(
        ifc_table, config_table,
        left_on='Material', right_on='Material_Archicad',
        how='left'
    )

    # Anhängen der KBOB-Eigenschaften an die IFC-Daten
    final_ifc_data = pd.merge(
        ifc_with_kbob, kbob_table,
        left_on='Material_KBOB', right_on='BAUMATERIALIEN',
        how='left'
    )

    # Entfernen unnötiger Spalten
    final_ifc_data = final_ifc_data.drop(columns=['Material_Archicad', 'Material_KBOB'])

    # Speichern der angereicherten Daten in einer neuen Excel-Datei
    final_ifc_data.to_excel(output_file_path, index=False)

