import ifcopenshell
import ifcopenshell.util.element
import pandas as pd

# Öffne die IFC-Datei
file_path = r"C:\Users\pasca\OneDrive - Hochschule Luzern\Programmieren\DT_Projekt_HS24\Decke_Wand.ifc"
model = ifcopenshell.open(file_path)

# Funktion zur Extraktion der BaseQuantities mit get_psets
def extract_base_quantities_with_psets(model):
    wall_data = []
    walls = model.by_type("IfcWall")
    
    for wall in walls:
        # Extrahiere Property Sets der Wand
        psets = ifcopenshell.util.element.get_psets(wall)
        
        # Überprüfe, ob BaseQuantities existieren
        if "BaseQuantities" in psets:
            base_quantities = psets["BaseQuantities"]
            data = {
                "WallGlobalId": wall.GlobalId,
                "Width": base_quantities.get("Width"),  # Zugriff auf Width
                "NetSideArea": base_quantities.get("NetSideArea")  # Zugriff auf NetSideArea
            }
            wall_data.append(data)
    
    return wall_data

# Extrahiere die BaseQuantities
wall_quantities = extract_base_quantities_with_psets(model)

# Ergebnisse in einer Tabelle anzeigen
df = pd.DataFrame(wall_quantities)
print(df)
