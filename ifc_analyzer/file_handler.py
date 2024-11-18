import os
import tempfile

def save_uploaded_file(uploaded_file):
    """Speichert eine hochgeladene Datei temporär und gibt den Dateipfad zurück."""
    try:
        temp_dir = tempfile.gettempdir()
        file_path = os.path.join(temp_dir, uploaded_file.name)

        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        return file_path
    except Exception as e:
        print(f"Fehler beim Speichern der Datei: {e}")
        return None

def delete_file(file_path):
    """Löscht die angegebene Datei."""
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"Datei gelöscht: {file_path}")
        else:
            print("Datei existiert nicht.")
    except Exception as e:
        print(f"Fehler beim Löschen der Datei: {e}")
