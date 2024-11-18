import ifcopenshell
import ifcopenshell.util
import ifcopenshell.util.element

# Öffne die IFC-Datei
model = ifcopenshell.open(r"C:\Users\pasca\OneDrive - Hochschule Luzern\Programmieren\DT_Projekt_HS24\Decke_Wand.ifc")

wall_test = model.by_type('IfcWall')[0]
print(wall_test.is_a()) # Returns 'IfcWall'


print(ifcopenshell.util.element.get_psets(wall_test))


walls = model.by_type("IfcWall")
results = []

for wall in walls:
    for definition in wall.IsDefinedBy:
        if definition.is_a("IfcRelDefinesByProperties"):
            prop_or_quant = definition.RelatingPropertyDefinition

            # Prüfen, ob es sich um Mengenangaben (Quantities) handelt
            if prop_or_quant.is_a("IfcElementQuantity"):
                print(f"Quantities for {wall.GlobalId}:")
                for quantity in prop_or_quant.Quantities:
                    # Zugriff auf den Wert der Menge
                    if hasattr(quantity, "QuantityValue"):
                        print(f"  {quantity.Name}: {quantity.QuantityValue}")
            elif prop_or_quant.is_a("IfcPropertySet"):
                # Falls es ein Property Set ist, wie gewohnt fortfahren
                print(f"Properties for {wall.GlobalId}:")
                for prop in prop_or_quant.HasProperties:
                    if hasattr(prop, "NominalValue"):
                        print(f"  {prop.Name}: {prop.NominalValue}")




