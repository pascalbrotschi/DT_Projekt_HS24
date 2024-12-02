import matplotlib.pyplot as plt
import mplcursors

# Daten für das Kuchendiagramm
labels = ['Apples', 'Bananas', 'Cherries', 'Dates']
sizes = [15, 30, 45, 10]
colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue']

# Kuchendiagramm erstellen
fig, ax = plt.subplots()
wedges, texts, autotexts = ax.pie(
    sizes,
    labels=labels,
    autopct='%1.1f%%',
    startangle=140,
    colors=colors
)

# Anpassung der Beschriftungen
for text in autotexts:
    text.set_color('white')

# Interaktive Funktion hinzufügen
cursor = mplcursors.cursor(wedges, hover=True)

@cursor.connect("add")
def on_hover(sel):
    # Anzeige der Details des ausgewählten Kuchenstücks
    label = labels[wedges.index(sel.artist)]
    size = sizes[wedges.index(sel.artist)]
    sel.annotation.set(text=f'{label}: {size}')

# Plot anzeigen
plt.title('Interaktives Kuchendiagramm')
plt.show()