import plotly.graph_objects as go

def create_interactive_donut_chart(values, labels, total_value, title, unit):
    """
    Erstellt ein interaktives Donut-Diagramm mit Plotly.

    Args:
        values (list): Werte für die Diagrammsegmente.
        labels (list): Beschriftungen der Segmente.
        total_value (float): Gesamtwert in der Mitte des Donuts.
        title (str): Titel des Diagramms.
        unit (str): Maßeinheit, die unter dem Totalwert angezeigt wird.

    Returns:
        Plotly Figure: Das Donut-Diagramm.
    """
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.7,  # Donut-Effekt
        textinfo='label+percent',  # Prozent und Label anzeigen
        hoverinfo='label+value+percent',
        hovertemplate='%{label}<br>%{value:.2f} ' + unit + '<br>%{percent}'
    )])

    # Zentralen Text (Wert und Einheit) hinzufügen
    fig.add_annotation(
        x=0.5, y=0.5,  # Position (Mitte des Donuts)
        text=f"<b>{total_value:.2f}</b><br><span style='font-size:14px;'>{unit}</span>",
        showarrow=False,
        font=dict(size=30, color="white"),
        align="center",
        xref="paper", yref="paper"
    )

    # Layout anpassen
    fig.update_layout(
        title=dict(text=title, x=0.425, y=0.95, xanchor='center', font=dict(size=20, color="white")),
        showlegend=True,
        margin=dict(t=50, b=50, l=50, r=50),
    )

    return fig







