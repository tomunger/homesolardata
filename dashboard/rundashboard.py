import datetime

import dash
from dash import dcc, html
import plotly
from dash.dependencies import Input, Output, State
import dotenv
import os
import sqlalchemy

import sys
print (sys.path)

import envoy
import graphsolar


#
# Load development environment setting.
#
dotenv.load_dotenv(dotenv_path='localenv-prod.txt')


#
# Object to read from the envoy system.
#
envoy_system = envoy.EnvoySystem(os.getenv('ENPHASE_HOST', 'envoy.local'), int(os.getenv('ENPHASE_PORT', 80)))


#
# Create the Dash application.
external_stylesheets = ['https://cdn.jsdelivr.net/npm/bootstrap@5.2.0-beta1/dist/css/bootstrap.min.css', ]
app = dash.Dash(__name__, 
		external_stylesheets=external_stylesheets,
		external_scripts=['https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.min.js'])

#
# Server object is run by gunicorn.
#
server = app.server


#
# Layout the page.
# 
# Outputs:
#   date-text - Date of the last sample.
#	time-text - Time of the last sample.
#	production-text - solar prodtion.
#	consumption-text - home consumption.
#	net-consumption-text - Home net consumption.
#	history-graph - Graph of production history.
#
# Controls:
#	time-range - Dropdown defining graph type.
#	Future:  navigate back in time.
#
# Stored in the session:
#	next-graph-update-time - Time the graph will be updated.
#
p_label_class = 'text-muted text-end'
p_value_class = 'font-monospace fs-6 text-end'
app.layout = html.Div(
	[
 
	html.Div(className='container-md', children=
		[
		html.Div(className='row text-center', children= 
			[
				html.Div(className='col', children=[
					html.H3('Home solar production'),
				]),
			]),
		html.Div(className='row', children=
			[
			html.Div(className='container', children=
				[
				html.Div(className='row', children=
				   [
					html.Div(className='col-4', children=
						[
						html.P('Time', className=p_label_class),
						#html.Br(),
						html.P(className=p_value_class, children=
							[
							html.Span('', id='date-text'),
							" ",
							html.Span('', id='time-text'), 
							]),
						]),
					html.Div(className='col', children=
						[
						html.P('Production', className=p_label_class),
						html.P('', id='production-text', className=p_value_class),
						]),
					html.Div(className='col', children=
						[
						html.P('Consumption', className=p_label_class),
						html.P('', id='consumption-text', className=p_value_class),
						]),
					html.Div(className='col', children=
						[
						html.P('Net', className=p_label_class),
						html.P('', id='net-consumption-text', className=p_value_class),
						]),
					]),
				]),
			]),

		html.Div(className='row mt-3', children=
			[
			html.Div(className='col-12', children=
				[
				html.Div(className='input-group', children=
					[
					html.Span('Time range', className='input-group-text'),
					dcc.Dropdown(id="time-range", className='form-control', options=[
							{'label': '30 minutes', 'value': '30m'},
							{'label': '1 hour', 'value': '1h'},
							{'label': '3 hours', 'value': '3h'},
							{'label': '6 hours', 'value': '6h'},
							{'label': '12 hours', 'value': '12h'},
							{'label': '1 day', 'value': '1d'},
							{'label': '3 days', 'value': '3d'},
							#{'label': '7 days', 'value': '7d'},
							#{'label': '', 'value': '1h'},
						],
						value='30m'),
					]),
				]),
			]),
		html.Div(className='row', children=
			[
			dcc.Graph(id='live-update-graph'),
			]),
		]),
	dcc.Interval(
		id='interval-component',
		interval=5*1000, # in milliseconds
		n_intervals=0),
	dcc.Store(id='graph-update-time', storage_type='session'),
	dcc.Store(id='last-time-range', storage_type='session'),
	])


@app.callback(
		Output('date-text', 'children'),
		Output('time-text', 'children'),
		Output('production-text', 'children'),
		Output('consumption-text', 'children'),
		Output('net-consumption-text', 'children'),
		Output('live-update-graph', 'figure'),
		Output('graph-update-time', 'data'),
		Output('last-time-range', 'data'),
		Input('interval-component', 'n_intervals'),
		Input('time-range', 'value'),
		State('graph-update-time', 'data'),
		State('last-time-range', 'data'))
def update_metrics(n, time_range, graph_update_time_in, last_time_range):
	if time_range is None:
		raise dash.PreventUpdate

	#
	# Claculate the date and time texts.
	#
	now = datetime.datetime.now()
	date_text = now.strftime("%Y-%m-%d")
	time_text = now.strftime("%H:%M:%S")

	#
	# Get current solar production numbers and calculate those outputs.
	#
	production_text = dash.no_update
	consumption_text = dash.no_update
	net_consumption_text = dash.no_update
	sditem = envoy_system.get_power()
	if sditem is not None:
		production_text = f"{sditem.production:,.0f}"
		consumption_text = f"{sditem.consumption:,.0f}"
		net_consumption_text = f"{sditem.production - sditem.consumption:,.0f}"


	#
	# defaults for graph output.
	#
	graph_figure = dash.no_update
	graph_update_time_out = dash.no_update
 
	# Decide if it is time to update the graph.
	is_update_graph = False
	if time_range != last_time_range:
		is_update_graph = True
	elif graph_update_time_in is None:
		# No update time set, so we update now.
		is_update_graph = True
	else:
		try:
			update_time = datetime.datetime.strptime(graph_update_time_in, "%Y-%m-%d %H:%M:%S")
			# Valid update time is set so we check if we are past that time.
			is_update_graph = now > update_time
		except:
			# Could not parse the update time so we update now.
			is_update_graph = True

	#
	# Update the graph
	if is_update_graph:
		grapher = graphsolar.create_grapher(time_range)
		connectionstr = f"mysql+pymysql://{os.getenv('SOLARDB_USER')}:{os.getenv('SOLARDB_PASS')}@{os.getenv('SOLARDB_HOST')}:{os.getenv('SOLARDB_PORT', 3306)}/{os.getenv('SOLARDB_NAME')}?charset=utf8mb4"
		engine = sqlalchemy.create_engine(connectionstr)
		with engine.connect() as conn:
			graph_figure = grapher.graph(conn)
		# Calculate the next update time.
		graph_update_time_out = (now + grapher.update_interval).strftime("%Y-%m-%d %H:%M:%S")
		last_time_range = time_range
		print (f"Update graph {time_range}")

	return [
		date_text,
		time_text,
		production_text,
		consumption_text,
		net_consumption_text,
		graph_figure,
		graph_update_time_out,
		last_time_range,
	]


if __name__ == '__main__':
	app.run_server(debug=True)