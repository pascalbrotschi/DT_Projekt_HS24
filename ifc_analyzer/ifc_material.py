import ifcopenshell
import ifcopenshell.util.element
import pandas as pd

# Öffne die IFC-Datei
file_path = r"C:\Users\pasca\OneDrive - Hochschule Luzern\Programmieren\DT_Projekt_HS24\Decke_Wand.ifc"
model = ifcopenshell.open(file_path)

# Funktion zur Extraktion der Materialien für alle IFC-Entitäten
def extract_materials_for_all_entities(model):
    material_data = []
    entities = model.by_type("IfcProduct")  # Alle IFC-Produkt-Entitäten

    for entity in entities:
        # Extrahiere Property Sets der Entität
        psets = ifcopenshell.util.element.get_psets(entity)

        # Prüfe auf spezifische Materialinformationen
        material_info = None
        if "Pset_MaterialCommon" in psets:  # Häufig verwendetes Material-Pset
            material_info = psets["Pset_MaterialCommon"].get("Material")

        # Fallback: Materialien aus RelatingMaterial-Attribut extrahieren
        if material_info is None and hasattr(entity, "HasAssociations"):
            for association in entity.HasAssociations:
                if association.is_a("IfcRelAssociatesMaterial"):
                    material = association.RelatingMaterial
                    if material.is_a("IfcMaterial"):
                        material_info = material.Name
                    elif material.is_a("IfcMaterialLayerSetUsage"):
                        material_info = ", ".join(
                            layer.Material.Name for layer in material.ForLayerSet.MaterialLayers
                        )

        # Füge Entität und Materialinformation der Liste hinzu
        material_data.append({
            "EntityGlobalId": entity.GlobalId,
            "EntityType": entity.is_a(),
            "Material": material_info
        })

    return material_data

# Extrahiere die Materialien für alle Entitäten
materials = extract_materials_for_all_entities(model)

# Ergebnisse in einer Tabelle anzeigen
df = pd.DataFrame(materials)
print(df)
