import plotly.express as px

# Daten für das Kuchendiagramm
data = {
    "Labels": ["Apples", "Bananas", "Cherries", "Dates"],
    "Values": [15, 30, 45, 10]
}

# Diagramm erstellen
fig = px.pie(data, names="Labels", values="Values", title="Interaktives Kuchendiagramm")

# Speichern als HTML-Datei
fig.write_html("interactive_piechart.html")

print("Diagramm wurde als 'interactive_piechart.html' gespeichert. Öffne es manuell im Browser.")
