import pandas as pd

def merge_basequantities_materials(wall_data, slab_data, column_data, beam_data, material_data):
    """
    Merged die Daten von Wänden, Decken, Stützen, Trägern und Materialien basierend auf ihren GlobalIds.

    Args:
        wall_data (list of dict): BaseQuantities der Wände (von extract_wall_base_quantities_with_psets).
        slab_data (list of dict): BaseQuantities der Decken (von extract_slab_base_quantities_with_psets).
        column_data (list of dict): BaseQuantities der Stützen (von extract_column_base_quantities_with_psets).
        beam_data (list of dict): BaseQuantities der Trägern (von extract_beam_base_quantities_with_psets).
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

    df_columns = pd.DataFrame(column_data)
    df_columns.rename(columns={"ColumnGlobalId": "GlobaldId"}, inplace=True)

    df_beams = pd.DataFrame(beam_data)
    df_beams.rename(columns={"BeamGlobalId": "GlobaldId"}, inplace=True)

    # Materialien zu DataFrame konvertieren
    df_materials = pd.DataFrame(material_data)
    df_materials.rename(columns={"EntityGlobalId": "GlobalId"}, inplace=True)

    # Wände und Materialien kombinieren
    merged_walls = pd.merge(df_walls, df_materials, on="GlobalId", how="left")

    # Decken und Materialien kombinieren
    merged_slabs = pd.merge(df_slabs, df_materials, on="GlobalId", how="left")

    merged_columns = pd.merge(df_columns, df_materials, on="GlobalId", how="left")

    merged_beams = pd.merge(df_beams, df_materials, on="GlobalId", how="left")

    # Alle Tabellen zusammenfügen
    final_df = pd.concat([merged_walls, merged_slabs, merged_columns, merged_beams], ignore_index=True)

    # Neue Spalte für Bauteilfläche erstellen
    final_df["Bauteilfläche"] = final_df["NetArea"].combine_first(final_df["NetSideArea"])

    # Entferne die alten Spalten, wenn sie nicht mehr benötigt werden
    final_df.drop(columns=["NetArea", "NetSideArea"], inplace=True)

    # Spaltenreihenfolge ändern: Width als letzte Spalte
    columns = [col for col in final_df.columns if col != "Width"] + ["Width"]
    final_df = final_df[columns]

    return final_df
