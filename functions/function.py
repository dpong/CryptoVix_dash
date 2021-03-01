import dash, json
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table
from dash.dependencies import Input, Output, State
from datetime import datetime, timedelta
import pandas as pd
from apis.Mongo import Mongo
from bson import ObjectId

mongo = Mongo()


def get_FCAS_score():
    db = mongo.client['crypto_information']
    collect = db['FCAS_score']
    cursor = collect.find({})
    data = list(cursor)
    df = pd.DataFrame(data)
    df = df[['asset_name', 'symbol', 'metric_slug', 'value', 'grade']]
    df = df.sort_values(by=['value'], ascending=False)
    return df

