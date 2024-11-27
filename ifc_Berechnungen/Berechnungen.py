import pandas as pd

def Berechnung_GE_THG(input_file_path, output_file_path):
    """
    Berechnet Masse/Bauteilfläche, GE/Bauteilfläche, GE Total, 
    THG/Bauteilfläche und THG Total für jedes Element in der Tabelle.

    Parameter:
    - input_file_path: Pfad zur Eingabe-Excel-Datei.
    - output_file_path: Pfad zur Ausgabe-Excel-Datei mit den berechneten Werten.

    Rückgabe:
    - Die Tabelle mit den berechneten Werten als Pandas DataFrame.
    """
    # Eingabedatei laden
    ifc_table = pd.read_excel(input_file_path)

    # Berechnungen für Graue Energie (GE)
    ifc_table['Masse/Bauteilfläche'] = ifc_table['Width'] * ifc_table['Rohdichte_Flächenmasse']
    ifc_table['GE/Bauteilfläche'] = ifc_table['Masse/Bauteilfläche'] * ifc_table['Graue_Energie_Total_kWh_oil_eq']
    ifc_table['GE Total'] = ifc_table['GE/Bauteilfläche'] * ifc_table['Bauteilfläche']

    # Berechnungen für Treibhausgasemissionen (THG)
    ifc_table['THG/Bauteilfläche'] = ifc_table['Masse/Bauteilfläche'] * ifc_table['CO2_Emissionen_Total_kg_CO2_eq']
    ifc_table['THG Total'] = ifc_table['THG/Bauteilfläche'] * ifc_table['Bauteilfläche']

    # Tabelle speichern
    ifc_table.to_excel(output_file_path, index=False)

    return ifc_table


