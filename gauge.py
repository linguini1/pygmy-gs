from dash import dcc
import plotly.graph_objects as go

def create_gauge(title: str, unit: str) -> dcc.Graph:
    return dcc.Graph(
        id=title.lower(),
        figure=go.Figure(go.Indicator(
            mode="gauge+number",
            value=0,
            domain={"x": [0, 1], "y": [0, 1]},
            title={"text": title},
        ))
    )
