import streamlit as st
import os

# Titel des Userinterfaces
st.title("Datei-Upload und Skript-Ausführung")

# Schritt 1: Datei hochladen
uploaded_file = st.file_uploader("Laden Sie eine Datei hoch", type=["ifc"])

if uploaded_file is not None:
    # Speichern der hochgeladenen Datei
    file_path = os.path.join("uploaded_files", uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success(f"Datei wurde erfolgreich hochgeladen: {file_path}")
    
    # Schritt 2: Datei ausführen
    if st.button("Skript ausführen"):
        st.info("Skript wird ausgeführt...")
        result = os.system(f"python {file_path}")  # Skript ausführen
        if result == 0:
            st.success("Skript wurde erfolgreich ausgeführt!")
        else:
            st.error("Es gab ein Problem beim Ausführen des Skripts.")
