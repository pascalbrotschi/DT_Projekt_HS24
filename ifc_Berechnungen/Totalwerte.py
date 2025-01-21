import pandas as pd

def add_totals_and_group_by(input_path, output_path, sheet_name='Sheet1'):
    """
    Fügt die Gesamtsummen der Spalten 'GE Total' und 'THG Total' hinzu und speichert diese
    in separaten Sheets der Excel-Datei.

    Args:
        input_path (str): Pfad zur Eingabe-Excel-Datei.
        output_path (str): Pfad zur Ausgabe-Excel-Datei mit drei Sheets.
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
    totals_row_material = {
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
    material_totals['GlobalId'] = 'Material Total'

    # Totals DataFrame für Material erstellen
    totals_df_material = pd.concat([material_totals, pd.DataFrame([totals_row_material])], ignore_index=True)

    # Summen pro EntityType berechnen
    entity_totals = (
        ifc_table.groupby('EntityType')[['GE Total', 'THG Total']]
        .sum()
        .reset_index()
    )
    entity_totals['GlobalId'] = 'Entity Total'

    # Gesamtsummen aller EntityTypes als neue Zeile
    totals_row_entity = {
        'GlobalId': 'Total',
        'EntityType': 'All Entities',
        'GE Total': total_ge,
        'THG Total': total_thg
    }

    totals_df_entity = pd.concat([entity_totals, pd.DataFrame([totals_row_entity])], ignore_index=True)

    # Schreibe beide DataFrames in separate Sheets
    with pd.ExcelWriter(output_path) as writer:
        ifc_table.to_excel(writer, sheet_name=sheet_name, index=False)  # Ursprüngliches Sheet
        totals_df_material.to_excel(writer, sheet_name='Totals_Material', index=False)  # Neues Sheet mit Material-Summen
        totals_df_entity.to_excel(writer, sheet_name='Totals_Entity', index=False)    # Neues Sheet mit Entity-Summen

