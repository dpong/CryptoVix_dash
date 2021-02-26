import dash
import dash_bootstrap_components as dbc


app = dash.Dash(
    external_stylesheets=[dbc.themes.SLATE],
    )
app.title = 'CryptoVix'


server = app.server

import index
