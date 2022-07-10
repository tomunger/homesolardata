'''

Simple test to display an updating graph of solar produciton.

'''

from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import sqlalchemy
import datetime
import dotenv
import os
import graphsolar

#
# Load test configuration.
#
dotenv.load_dotenv(dotenv_path='../localenv-prod.txt')



def load_data(user: str, password: str, host: str, port: int, dbname: str, tablename: str, history_min:int) -> pd.DataFrame:
	'''Load recent data in to a data frame.'''
	connectionstr = f"mysql+pymysql://{user}:{password}@{host}:{port}/{dbname}?charset=utf8mb4"
	engine = sqlalchemy.create_engine(connectionstr)
	engine.connect()

	data_to = datetime.datetime.now()
	data_from = data_to - datetime.timedelta(minutes=history_min)
	data_from_str = data_from.strftime("%Y-%m-%d %H:%M:%S")
	data_to_str = data_to.strftime("%Y-%m-%d %H:%M:%S")

	sql =  f'''
	SELECT datetime, consumption, production FROM {tablename}
		WHERE datetime >= '{data_from_str}' and datetime < '{data_to_str}'
		ORDER by datetime asc
	'''
	solardf = pd.read_sql(sql, engine, index_col='datetime')
	return solardf



#
# Set up the application.
#
app = Dash(__name__)


app.layout = html.Div([
    dcc.Graph(
        id='solar',
    ),
	dcc.Interval(
		id='interval-component',
		interval=30*1000, # in milliseconds
		n_intervals=0
	)

])




@app.callback(Output('solar', 'figure'),
              Input('interval-component', 'n_intervals'))
def update_metrics(n):
	'''Called at intervals to draw a new graph.
	'''
	#
	# Load recent data in to a data frame.
	#
	grapher = graphsolar.create_grapher('1d')
	connectionstr = f"mysql+pymysql://{os.getenv('SOLARDB_USER')}:{os.getenv('SOLARDB_PASS')}@{os.getenv('SOLARDB_HOST')}:{os.getenv('SOLARDB_PORT', 3306)}/{os.getenv('SOLARDB_NAME')}?charset=utf8mb4"
	engine = sqlalchemy.create_engine(connectionstr)
	with engine.connect() as conn:
		fig = grapher.graph(conn)

	return fig



if __name__ == '__main__':
    app.run_server(debug=True)
