import ifcopenshell
import ifcopenshell.util.element
import pandas as pd
from .ifc_basequantities import extract_slab_base_quantities_with_psets, extract_wall_base_quantities_with_psets
from .ifc_material import extract_materials_for_all_entities

def merge_wall_slab_materials(wall_data, slab_data, material_data):
    """
    Merged die Daten von Wänden, Decken und Materialien basierend auf ihren GlobalIds.

    Args:
        wall_data (list of dict): BaseQuantities der Wände (von extract_wall_base_quantities_with_psets).
        slab_data (list of dict): BaseQuantities der Decken (von extract_slab_base_quantities_with_psets).
        material_data (list of dict): Materialien aller Entitäten (von extract_materials_for_all_entities).

    Returns:
        pd.DataFrame: Eine kombinierte Tabelle mit allen Informationen.
    """
    # Wände zu DataFrame konvertieren
    df_walls = pd.DataFrame(wall_data)
    df_walls.rename(columns={"WallGlobalId": "GlobalId"}, inplace=True)

    # Decken zu DataFrame konvertieren
    df_slabs = pd.DataFrame(slab_data)
    df_slabs.rename(columns={"SlabGlobalId": "GlobalId"}, inplace=True)

    # Materialien zu DataFrame konvertieren
    df_materials = pd.DataFrame(material_data)
    df_materials.rename(columns={"EntityGlobalId": "GlobalId"}, inplace=True)

    # Wände und Materialien kombinieren
    merged_walls = pd.merge(df_walls, df_materials, on="GlobalId", how="left")

    # Decken und Materialien kombinieren
    merged_slabs = pd.merge(df_slabs, df_materials, on="GlobalId", how="left")

    # Beide Tabellen zusammenfügen
    final_df = pd.concat([merged_walls, merged_slabs], ignore_index=True)

    # Neue Spalte für Bauteilfläche erstellen
    final_df["Bauteilfläche"] = final_df["NetArea"].combine_first(final_df["NetSideArea"])

    # Entferne die alten Spalten, wenn sie nicht mehr benötigt werden
    final_df.drop(columns=["NetArea", "NetSideArea"], inplace=True)

    # Spaltenreihenfolge ändern: Width als letzte Spalte
    columns = [col for col in final_df.columns if col != "Width"] + ["Width"]
    final_df = final_df[columns]

    return final_df

# Beispiel
file_path = r"C:\Users\pasca\OneDrive - Hochschule Luzern\Programmieren\DT_Projekt_HS24\Decke_Wand.ifc"
model = ifcopenshell.open(file_path)

# Extrahiere Daten
wall_data = extract_wall_base_quantities_with_psets(model)
slab_data = extract_slab_base_quantities_with_psets(model)
material_data = extract_materials_for_all_entities(model)

# Merge durchführen
final_table = merge_wall_slab_materials(wall_data, slab_data, material_data)

# Speichere die Tabelle als Excel-Datei mit Pandas
output_file = r"C:\Users\pasca\OneDrive - Hochschule Luzern\Programmieren\DT_Projekt_HS24\final_table.xlsx"
final_table.to_excel(output_file, index=False)

print(f"Die Tabelle wurde erfolgreich als Excel-Datei gespeichert: {output_file}")
