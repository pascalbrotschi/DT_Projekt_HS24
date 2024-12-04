import pandas as pd

def add_totals_and_group_by_material(input_path, output_path, sheet_name='Sheet1'):
    """
    Fügt die Gesamtsummen der Spalten 'GE Total' und 'THG Total' hinzu und speichert diese
    in einem separaten Sheet der Excel-Datei.

    Args:
        input_path (str): Pfad zur Eingabe-Excel-Datei.
        output_path (str): Pfad zur Ausgabe-Excel-Datei mit zwei Sheets.
        sheet_name (str): Name des Sheets, das verarbeitet werden soll (Standard: 'Sheet1').

    Returns:
        None
    """
    # Excel-Datei laden
    ifc_table = pd.read_excel(input_path, sheet_name=sheet_name)

    # Gesamtsummen für "GE Total" und "THG Total" berechnen
    total_ge = ifc_table['GE Total'].sum()
    total_thg = ifc_table['THG Total'].sum()

    # Gesamtsummen aller Materialien als neue Zeile
    totals_row = {
        'GlobalId': 'Total',
        'Material': 'All Materials',
        'GE Total': total_ge,
        'THG Total': total_thg
    }

    # Summen pro Material berechnen
    material_totals = (
        ifc_table.groupby('Material')[['GE Total', 'THG Total']]
        .sum()
        .reset_index()
    )

    # Füge eine konstante Spalte "GlobalId" hinzu, um die Tabelle vollständig zu halten
    material_totals['GlobalId'] = 'Material Total'

    # Erstelle eine DataFrame für die Totals
    totals_df = pd.concat([material_totals, pd.DataFrame([totals_row])], ignore_index=True)

    # Schreibe beide DataFrames in zwei separate Sheets
    with pd.ExcelWriter(output_path) as writer:
        ifc_table.to_excel(writer, sheet_name=sheet_name, index=False)  # Ursprüngliches Sheet
        totals_df.to_excel(writer, sheet_name='Totals', index=False)   # Neues Sheet mit Summen

