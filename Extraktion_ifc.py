import ifcopenshell
import pandas as pd

# Pfad zur IFC-Datei
ifc_file_path = input("Gib den Datei Pfad an: ")  # Ersetzen Sie den Dateinamen bei Bedarf


# IFC-Datei laden
ifc_file = ifcopenshell.open(ifc_file_path)

# Konfigurationsliste (Attribute, die extrahiert werden sollen)
config = {
    "Material": True,
    "Thickness": True,  # Wird aus BaseQuantities - Width extrahiert
    "Area": True        # Wird aus BaseQuantities - NetArea extrahiert
}

# Funktion zur Materialextraktion
def get_material(element):
    try:
        for rel in element.HasAssociations:
            if rel.is_a("IfcRelAssociatesMaterial"):
                material = rel.RelatingMaterial
                if material.is_a("IfcMaterial"):
                    return material.Name
                elif material.is_a("IfcMaterialLayerSetUsage"):
                    return material.ForLayerSet.MaterialLayers[0].Material.Name
                elif material.is_a("IfcMaterialLayerSet"):
                    return material.MaterialLayers[0].Material.Name
        return "Unknown"
    except AttributeError:
        return "Unknown"

# Funktion zur Extraktion der BaseQuantities (Dicke und Fläche)
def get_quantity(element, quantity_name):
    try:
        for rel in element.IsDefinedBy:
            if rel.is_a("IfcRelDefinesByProperties") and rel.RelatingPropertyDefinition.is_a("IfcElementQuantity"):
                for quantity in rel.RelatingPropertyDefinition.Quantities:
                    if quantity.Name == quantity_name:
                        return quantity.NominalValue.wrappedValue
        return "N/A"
    except AttributeError:
        return "N/A"

# Daten sammeln
elements_data = []

for element in ifc_file.by_type("IfcElement"):
    # Material extrahieren
    material = get_material(element) if config.get("Material") else "N/A"

    # Dicke extrahieren (BaseQuantities - Width)
    thickness = get_quantity(element, "Width") if config.get("Thickness") else "N/A"

    # Fläche extrahieren (BaseQuantities - NetArea)
    area = get_quantity(element, "NetArea") if config.get("Area") else "N/A"

    # Elementname erfassen
    element_name = element.Name if element.Name else "Unnamed Element"

    # Daten speichern
    elements_data.append({
        "Element Name": element_name,
        "Material": material,
        "Thickness (Width)": thickness,
        "Area (NetArea)": area
    })

# Datenrahmen erstellen
elements_df = pd.DataFrame(elements_data)

# Daten in Excel exportieren
output_path = "ifc_extracted_data.xlsx"
elements_df.to_excel(output_path, index=False)

print(f"Die Daten wurden erfolgreich in '{output_path}' gespeichert.")

