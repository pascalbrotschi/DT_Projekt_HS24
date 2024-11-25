import pandas as pd

# Lade die erste Tabelle (final_table)
final_table_path = 'final_table.xlsx'
final_table = pd.read_excel(final_table_path, sheet_name='Sheet1')

# Lade die zweite Tabelle (Oekobilanzdaten)
oekobilanz_table_path = 'Oekobilanzdaten_2009-1-2022_v3.0.xlsx'
oekobilanz_table = pd.read_excel(oekobilanz_table_path, sheet_name='Baumaterialien Matériaux')

# Bereinigung und Vereinheitlichung der Materialspalten
final_table['Material'] = final_table['Material'].str.strip().str.lower()
oekobilanz_table['BAUMATERIALIEN'] = oekobilanz_table['BAUMATERIALIEN'].str.strip().str.lower()

# Suche nach Materialien aus der ersten Tabelle in der zweiten Tabelle
matched_rows = []
for material in final_table['Material'].unique():
    matches = oekobilanz_table[oekobilanz_table['BAUMATERIALIEN'].str.contains(material, na=False)]
    if not matches.empty:
        matched_rows.append(matches)

# Alle gefundenen Zeilen zusammenführen
if matched_rows:
    result = pd.concat(matched_rows)
else:
    result = pd.DataFrame(columns=oekobilanz_table.columns)

# Speichere das Ergebnis in einer neuen Excel-Datei
output_path = 'matched_materials.xlsx'
result.to_excel(output_path, index=False)

print(f"Das Ergebnis wurde in '{output_path}' gespeichert.")
