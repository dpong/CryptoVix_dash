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
                    page_current=0,
                    page_size=100,
                    page_action='custom',
                    sort_action='custom',
                    sort_mode='single',
                    sort_by=[],
                    style_cell={'textAlign': 'center', 'height': 'auto', 'minWidth': '120px', 'width': '120px', 'maxWidth': '120px','whiteSpace': 'normal', 'backgroundColor': 'rgba(0, 0, 0, 0)', 'color':'rgb(211,211,211)'},
                    style_header={
                            'backgroundColor': 'rgb(105,105,105)',
                            'fontWeight': 'bold',
                            'color':'white'
                        },
                ),
                ], justify="center", style={'margin-top':'5px'}),
                html.Div(id='storage1_all', style={'display': 'none'}),
        ], width=10, xs=10, lg=6),
        dbc.Col([], width=1, xs=1, lg=3),
    ]),
    ])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    return index_layout()
        

@app.callback(
    Output('main_table', 'data'),
    [Input('main_table', "page_current"),
     Input('main_table', "page_size"),
     Input('main_table', 'sort_by'),
     Input('storage1_all', 'children')])
def update_table(page_current, page_size, sort_by, data1):
    df = pd.read_json(data1, orient='split')
    if len(sort_by):
        dff = df.sort_values(
            sort_by[0]['column_id'],
            ascending=sort_by[0]['direction'] == 'asc',
            inplace=False
        )
    else:
        # No sort is applied
        dff = df
    return dff.iloc[page_current*page_size:(page_current+ 1)*page_size].to_dict('records')


@app.callback(
    [Output('main_table', 'columns'),
    Output('storage1_all', 'children')],
    [Input('main_drop', 'value')])
def update_share_data(option):
    limited = 1000
    df = pd.DataFrame()
    if option == "Ranking":
        fcas = get_FCAS_score(limited)
        simetri = get_Simetri_score(limited)
        insight = get_token_insight_score(limited)
        fcas.drop_duplicates('symbol', 'first', inplace=True)
        df['symbol'] = fcas['symbol']
        df['name'] = fcas['asset_name']
        fcas = fcas.merge(simetri, left_on='asset_name', right_on='Coin Name')
        fcas = fcas.merge(insight, left_on='symbol', right_on='symbol')
        print(fcas.tail(10))
        df['FCAS'] = fcas['grade']
        df['Simetri'] = fcas['Current']
        df['Token Insight'] = fcas['ratinga']
        df = df[['symbol', 'name', 'FCAS', 'Simetri', 'Token Insight']]
    col = [{"name": str(i), "id": str(i)} for i in df.columns]
    return col, df.to_json(date_format='iso', orient='split')


if __name__ == '__main__':
    app.run_server(debug=False, host='0.0.0.0',port=9527)