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
app.layout = html.Div(
    html.Div([
        html.H4('Home solar production'),
        html.Div(id='live-update-text'),
        # dcc.Graph(id='live-update-graph'),
        dcc.Interval(
            id='interval-component',
            interval=5*1000, # in milliseconds
            n_intervals=0
        )
    ])
)


@app.callback(Output('live-update-text', 'children'),
              Input('interval-component', 'n_intervals'))
def update_metrics(n):
    (prod, cons) = envoy_system.get_power()
    style = {'padding': '5px', 'fontSize': '16px'}
    return [
		html.Span([
			'Production:  ',
			html.Code('{0:6.2f}'.format(prod), style={'fontSize': '18px'}),
		]),
		html.Br(),
		html.Span([
			'Consumption:  ',
			html.Code('{0:6.2f}'.format(cons), style={'fontSize': '18px'}),
		]),
    ]



if __name__ == '__main__':
    app.run_server(debug=True)