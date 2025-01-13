from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
from gauge import create_gauge

__author__ = "Matteo Golin"

GRUVBOX: dict[str, str] = {
    "red_dark" :"#cc241d",
    "red_light":"#fb4934",
    "blue_dark":"#458588",
    "blue_light":"#83a598",
    "aqua_dark":"#689d6a",
    "acqua_light":"#8ec07c",
    "gray_dark":"#928374",
    "gray_light":"#a89984",
    "green_dark" :"#98971a",
    "green_light":"#b8bb26",
    "yellow_dark"  :"#d79921",
    "yellow_light":"#fabd2f",
    "purple_dark":"#b16286",
    "purple_light":"#d3869b",
    "orange_dark":"#d65d0e",
    "orange_light":"#fe8019",
    "bg0":"#282828",
    "bg0_h":"#1d2021",
    "bg0_s":"#32302f",
    "bg1":"#3c3836",
    "bg2":"#504945",
    "bg3":"#665c54",
    "bg4":"#7c6f64",
    "gray":"#928374",
    "fg":"#ebdbb2",
    "fg0":"#fbf1c7",
    "fg1":"#ebdbb2",
    "fg2":"#d5c4a1",
    "fg3":"#bdae93",
    "fg4":"#a89984",
}

COLORS: dict[str, str] = {
    "background": GRUVBOX["bg0"],
    "text": GRUVBOX["fg"],
}

app = Dash("PygmyGS")

app.layout = [
    html.H1(children="PygmyGS", style={"textAlign": "center"}),
    create_gauge("Pressure", "kPa"),
    create_gauge("Temperature", "C"),
]

if __name__ == "__main__":
    app.run(debug=True)
