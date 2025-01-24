# Rohbau-IFC | Ökobilanzierung

Dieses Programm dient dazu, eine Ökobilanzierung für IFC-Dateien (Building Information Modeling) durchzuführen. Die Berechnungen basieren auf der **SIA 2032** und verwenden Daten aus der KBOB-Tabelle "Ökobilanzdaten im Baubereich". Ziel ist es, die graue Energie (GE) sowie die Treibhausgasemissionen (THG) für Materialien und Bauwerkelemente zu analysieren und darzustellen.

## Funktionen
- **Upload von IFC-Dateien**: Benutzer können ihre Rohbaumodelle als IFC-Dateien hochladen.
- **Analyse von Basisdaten**: Extraktion von Basisdaten zu Wänden, Decken, Säulen und Trägern sowie der zugehörigen Materialien.
- **Erweiterung der Daten**: Verknüpfung mit Materialkonfigurations- und KBOB-Daten.
- **Berechnung von Ökobilanzdaten**:
  - Graue Energie (kWh Öl-Äquivalent)
  - Treibhausgasemissionen (kg CO₂-Äquivalent)
- **Visualisierung**: Interaktive Donut-Diagramme zur Darstellung der Ergebnisse.
- **Download**: Excel-Tabelle mit den Ergebnissen zur weiteren Nutzung.

## Voraussetzungen
### Software
- **Python 3.8+**
- **Streamlit**
- Weitere notwendige Bibliotheken (siehe `requirements.txt`):
  - `ifcopenshell`
  - `pandas`
  - `plotly`

### Dateien
Die folgenden Konfigurationsdateien müssen im selben Verzeichnis wie das Programm vorhanden sein:
- `Material_Config.xlsx`: Materialkonfigurationen.
- `GE_THG_MAT.xlsx`: Daten zur grauen Energie und Treibhausgasemissionen (basierend auf KBOB).

## Installation
1. Klone das Repository oder lade den Quellcode herunter.
2. Stelle sicher, dass Python installiert ist.
3. Installiere die notwendigen Bibliotheken mit:
   ```bash
   pip install -r requirements.txt
   ```
4. Starte die Anwendung mit:
   ```bash
   streamlit run <name_der_datei>.py
   ```

## Nutzung
1. **Starte die Anwendung**: Führe das Programm in einem Browser aus.
2. **Lade eine IFC-Datei hoch**:
   - Ziehe die Datei in das Upload-Feld oder wähle sie über den Datei-Explorer aus.
3. **Starte die Ökobilanzierung**: Klicke auf den Button "Ökobilanzierung starten".
4. **Ergebnisse ansehen**:
   - Interaktive Donut-Diagramme für graue Energie und Treibhausgasemissionen.
   - Ergebnisse werden nach Material und Entity-Typ gruppiert.
5. **Excel-Tabelle herunterladen**: Lade die Ergebnisse als Excel-Datei herunter, indem du auf den Button "Excel-Tabelle Ökobilanzierung herunterladen" klickst.

## Dateien
- **Hochgeladene Datei**: Die hochgeladene IFC-Datei wird temporär gespeichert und nach der Analyse gelöscht.
- **Zwischenergebnisse**:
  - `IFC_Auszug_MAT.xlsx`: Analyse der Basisdaten.
  - `IFC_MAT_Config.xlsx`: Erweiterte Tabelle mit KBOB-Daten.
  - `IFC_MAT_Config_with_GE_THG.xlsx`: Tabelle mit berechneten Werten.
  - `IFC_TAB_Ökobilanzierung.xlsx`: Finales Ergebnis mit Totals.

## Visualisierung
Das Programm bietet folgende Diagramme zur Auswahl:
- **Graue Energie pro Material**
- **Treibhausgasemissionen pro Material**
- **Graue Energie pro EntityType**
- **Treibhausgasemissionen pro EntityType**

Die Diagramme sind interaktiv und bieten eine Übersicht über die Verteilung der grauen Energie und Treibhausgasemissionen.

## Fehlerbehebung
Falls ein Fehler auftritt:
- Prüfe, ob alle notwendigen Dateien vorhanden sind.
- Stelle sicher, dass die hochgeladene Datei eine valide IFC-Datei ist.
- Konsultiere die Fehlermeldungen, die in der Streamlit-Anwendung angezeigt werden.

## Lizenz
Dieses Programm ist ein Open-Source-Programm.

## Autoren
Dieses Projekt wurde von [Pascal Brotschi] erstellt.

