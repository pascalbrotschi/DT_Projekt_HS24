import plotly.graph_objects as go

def create_interactive_donut_chart(values, labels, total_value, title):
    """
    Erstellt ein interaktives Donut-Diagramm mit Plotly.

    Args:
        values (list): Werte für die Diagrammsegmente.
        labels (list): Beschriftungen der Segmente.
        total_value (float): Gesamtwert in der Mitte des Donuts.
        title (str): Titel des Diagramms.

    Returns:
        Plotly Figure: Das Donut-Diagramm.
    """
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.7,  # Donut-Effekt
        textinfo='percent+label',
        hoverinfo='label+value+percent'
    )])

    # Zentralen Text hinzufügen
    fig.add_annotation(
        x=0.5, y=0.5,  # Position (Mitte des Donuts)
        text=f"{total_value:.2f}",
        showarrow=False,
        font=dict(size=40, color="black"),
        xref="paper", yref="paper"
    )

    # Layout anpassen
    fig.update_layout(
        title=dict(text=title, x=0.5, xanchor='center'),
        showlegend=True,
        margin=dict(t=50, b=50, l=50, r=50)
    )

    return fig





