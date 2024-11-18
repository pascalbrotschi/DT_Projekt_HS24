import ifcopenshell

def analyze_ifc_file(file_path):
    """Analysiert die Anzahl der Wände in einer IFC-Datei."""
    try:
        # IFC-Datei mit ifcopenshell öffnen
        model = ifcopenshell.open(file_path)
        # Alle Wände im Modell extrahieren
        walls = model.by_type("IfcWall")
        return len(walls)
    except Exception as e:
        print(f"Fehler beim Verarbeiten der IFC-Datei: {e}")
        return None
