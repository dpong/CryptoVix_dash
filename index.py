import dash, re, json
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from app import app
from functions.function import *



app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

def index_layout():
    return html.Div([
    dbc.Row([
        dbc.Col([],width=1, xs=1, lg=3),
        dbc.Col([
            dbc.Row([
                dbc.Col([
                dbc.InputGroup(
                [
                    dbc.Select(id='main_drop', options=[{'label': 'Ranking', 'value': 'Ranking'}], value='Ranking'),
                ],
                className="mb-3"),
            ],width=6),
            ], justify="center"),
            dbc.Row([
                dash_table.DataTable(
                    id='main_table',
                    style_cell={'textAlign': 'center', 'height': 'auto', 'minWidth': '120px', 'width': '120px', 'maxWidth': '120px','whiteSpace': 'normal', 'backgroundColor': 'rgba(0, 0, 0, 0)', 'color':'rgb(211,211,211)'},
                    style_header={
                            'backgroundColor': 'rgb(105,105,105)',
                            'fontWeight': 'bold',
                            'color':'white'
                        },
                ),
                ], justify="center", style={'margin-top':'5px'}),
        ], width=10, xs=10, lg=6),
        dbc.Col([], width=1, xs=1, lg=3),
    ]),
    ])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    return index_layout()
        

@app.callback(
    [Output('main_table', 'columns'),
    Output('main_table', 'data')],
    [Input('main_drop', 'value')])
def update_share_data(option):
    limited = 1000
    df = pd.DataFrame()
    if option == "Ranking":
        fcas = get_FCAS_score(limited)
        fcas.drop_duplicates('symbol', 'first', inplace=True)
    col = [{"name": str(i), "id": str(i)} for i in df.columns]
    return col, df.to_dict('records')


if __name__ == '__main__':
    app.run_server(debug=False, host='0.0.0.0',port=9527)