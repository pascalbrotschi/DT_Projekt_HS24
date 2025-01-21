import ifcopenshell
import ifcopenshell.util.element
import pandas as pd

# Öffne die IFC-Datei
file_path = r"C:\Users\pasca\OneDrive - Hochschule Luzern\Programmieren\DT_Projekt_HS24\ARC_Box_MEP.ifc"
model = ifcopenshell.open(file_path)

# Funktion zur Extraktion der BaseQuantities mit get_psets
def extract_wall_base_quantities_with_psets(model):
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
wall_quantities = extract_wall_base_quantities_with_psets(model)

# Ergebnisse in einer Tabelle anzeigen
walldf = pd.DataFrame(wall_quantities)
print(walldf)


def extract_slab_base_quantities_with_psets(model):
    slab_data = []
    slabs = model.by_type("IfcSlab")

    for slab in slabs:
        psets = ifcopenshell.util.element.get_psets(slab)

        if "BaseQuantities" in psets:
            base_quantities = psets["BaseQuantities"]
            data = {
                "SlabGlobalId": slab.GlobalId,
                "Width": base_quantities.get("Width"),
                "NetArea": base_quantities.get("NetArea")
            }
            slab_data.append(data)
        
    return slab_data

slab_quantities = extract_slab_base_quantities_with_psets(model)

slabdf = pd.DataFrame(slab_quantities)
print(slabdf)


def extract_column_base_quantities_with_psets(model):
    column_data = []
    columns = model.by_type("IfcColumn")

    for column in columns:
        psets = ifcopenshell.util.element.get_psets(column)

        if "BaseQuantities" in psets:
            base_quantities = psets["BaseQuantities"]
            depth = base_quantities.get("Depth")
            width = base_quantities.get("Width")
            length = base_quantities.get("Length")

            # Berechnung der NetArea mit Depth und Length
            net_area = None
            if depth is not None and length is not None:
                net_area = depth * length

            data = {
                "ColumnGlobalId": column.GlobalId,
                "Width": width,
                "NetArea": net_area
            }
            column_data.append(data)
        
    return column_data

column_quantities = extract_column_base_quantities_with_psets(model)

columndf = pd.DataFrame(column_quantities)
print(columndf)


def extract_beam_base_quantities_with_psets(model):
    beam_data = []
    beams = model.by_type("IfcBeam")

    for beam in beams:
        psets = ifcopenshell.util.element.get_psets(beam)

        if "BaseQuantities" in psets:
            base_quantities = psets["BaseQuantities"]
            depth = base_quantities.get("Depth")
            width = base_quantities.get("Width")
            length = base_quantities.get("Length")

            # Berechnung der NetArea mit Depth und Length
            net_area = None
            if depth is not None and length is not None:
                net_area = depth * length

            data = {
                "BeamGlobalId": beam.GlobalId,
                "Width": width,
                "NetArea": net_area
            }
            beam_data.append(data)
        
    return beam_data


beam_quantities = extract_beam_base_quantities_with_psets(model)

beamdf = pd.DataFrame(beam_quantities)
print(beamdf)
