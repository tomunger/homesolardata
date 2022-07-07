import datetime

import dash
from dash import dcc, html
import plotly
from dash.dependencies import Input, Output
import dotenv
import os

import envoy

dotenv.load_dotenv(dotenv_path='localenv-prod.txt')


envoy_system = envoy.EnvoySystem(os.getenv('ENPHASE_HOST', 'envoy.local'), int(os.getenv('ENPHASE_PORT', 80)))

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

app.layout = html.Div(
    html.Div([
        html.H4('Home solar production'),
        html.Div([
            html.Span([
                'Time:  ',
                html.Code("", style={'fontSize': '18px'}, id="time-text"),
            ]),
            html.Br(),
            html.Span([
                'Production:  ',
                html.Code("", style={'fontSize': '18px'}, id="production-text"),
            ]),
            html.Br(),
            html.Span([
                'Consumption:  ',
                html.Code("", style={'fontSize': '18px'}, id="consumption-text"),
            ]),
        ]),
        # dcc.Graph(id='live-update-graph'),
        dcc.Interval(
            id='interval-component',
            interval=5*1000, # in milliseconds
            n_intervals=0
        )
    ])
)


@app.callback(Output('time-text', 'children'),
                Output('production-text', 'children'),
                Output('consumption-text', 'children'),
              Input('interval-component', 'n_intervals'))
def update_metrics(n):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    p = envoy_system.get_power()
    if p is None:
        return [now + "  (error fetching)", dash.no_update, dash.no_update]
        return [ html.Span(f'{now}: Error fetching power')]

    return [now, str(int(p[0])), str(int(p[1])) ]



if __name__ == '__main__':
    app.run_server(debug=False)