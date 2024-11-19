import pandas as pd

def merge_entity_and_quantities(entities_df, quantities_df, entity_id_col="EntityGlobalId", quantity_id_col="SlabGlobalId"):
    """
    Kombiniert zwei DataFrames basierend auf der gemeinsamen GlobalId-Spalte.
    
    Args:
        entities_df (pd.DataFrame): DataFrame mit Entity-Daten (Material, Typ, etc.).
        quantities_df (pd.DataFrame): DataFrame mit BaseQuantities-Daten.
        entity_id_col (str): Name der ID-Spalte im Entity-DataFrame (Standard: "EntityGlobalId").
        quantity_id_col (str): Name der ID-Spalte im Quantity-DataFrame (Standard: "SlabGlobalId").
        
    Returns:
        pd.DataFrame: Ein DataFrame mit kombinierten Informationen.
    """
    # Spaltennamen der Quantities-Tabelle anpassen
    quantities_df = quantities_df.rename(columns={quantity_id_col: entity_id_col})

    # Merge der beiden Tabellen basierend auf EntityGlobalId
    merged_df = pd.merge(entities_df, quantities_df, on=entity_id_col, how="inner")

    return merged_df
