import plotly.express as px
from plotly.graph_objects import Figure
import pandas as pd
import sqlalchemy
import datetime
import math


COLOR_PRODUCTION = '#00FA9A'
COLOR_CONSUMPTION = '#FF7F50'
COLOR_NET_CONSUMPTION = '#808080'

class Grapher(object):
	def graph(self, connection: sqlalchemy.engine.base.Connection) -> Figure:
		raise NotImplementedError()



class GraphMomentary(Grapher):
	def __init__(self, end_time: datetime.datetime, history_min: int, update_interval_sec: int,
					resample: str, smoothing: int):
		self._end_time = end_time
		self._history_min = history_min
		self._update_interval = datetime.timedelta(seconds=update_interval_sec)
		self._resample = resample
		self._smoothing = smoothing


	def _load_data(self, engine: sqlalchemy.engine.Engine) -> pd.DataFrame:

		data_to = self._end_time if self._end_time is not None else datetime.datetime.now()
		data_from = data_to - datetime.timedelta(minutes=self._history_min)
		data_from_str = data_from.strftime("%Y-%m-%d %H:%M:%S")
		data_to_str = data_to.strftime("%Y-%m-%d %H:%M:%S")

		sql =  f'''
		SELECT datetime, consumption, production FROM production
			WHERE datetime >= '{data_from_str}' and datetime < '{data_to_str}'
			ORDER by datetime asc
		'''
		solardf = pd.read_sql(sql, engine, index_col='datetime')

		# Resample and interpolate to fill gaps in data with reasonable value.
		if self._resample:
			df = solardf.resample(self._resample).mean().interpolate(method='linear', axis=0)

		# Smooth data with rolling average and convert to kiloWatts.
		if self._smoothing:
			smoothed_consumption = df['consumption'].rolling(self._smoothing).mean().dropna()
			smoothed_production = df['production'].rolling(self._smoothing).mean().dropna()
			solardf = pd.DataFrame(data={'production': smoothed_production, 'consumption': smoothed_consumption}, index=df.index)

		# Convert to kW, make consumption negative, and calculate a net.
		solardf['production'] = solardf['production']
		solardf['consumption'] = -solardf['consumption']
		solardf['net'] = solardf['production']  + solardf['consumption']

		return solardf


	@property
	def update_interval(self) -> datetime.timedelta:
		return self._update_interval



	def graph(self, connection: sqlalchemy.engine.Connection) -> Figure:
		df = self._load_data(connection)

		max_power = max(df['production'].max(), -(df['consumption'].min()))
		max_power = math.ceil(max_power)

		title = f"Solar production: {df.index[0].strftime('%H:%M')} to {df.index[-1].strftime('%H:%M')}"

		fig = px.line(df, y=['production', 'consumption', 'net'],
				title = title,
				range_y=[-max_power, max_power],
				height=700,
				template="simple_white")

		fig.update_layout(title_xanchor="center")
		#fig.update_layout("title_yanchor", "top")
		fig.update_layout(title_x=0.5)
		# fig.update_layout("title_y", 0.9)
		# fig.update_layout("title_font", dict(size=24))
		# fig.update_layout("title_x", 0.5)
		# fig.update_layout("title_y", 0.9)
		# fig.update_layout("title_font", dict(size=24))
		fig.update_layout(xaxis_title="Time")
		fig.update_layout(yaxis_title="Watts")
		fig.update_layout(xaxis_showgrid=True)
		fig.update_layout(yaxis_showgrid=True)
		# fig.update_layout("xaxis_zeroline", False)
		# fig.update_layout("yaxis_zeroline", False)
		# fig.update_layout("xaxis_showline", False)
		# fig.update_layout("yaxis_showline", False)
		# fig.update_layout("xaxis_showticklabels", False)
		# fig.update_layout("yaxis_showticklabels", False)
		# fig.update_layout("xaxis_autorange", True)
		# fig.update_layout("yaxis_autorange", True)
		# fig.update_layout("xaxis_range", [df.index[0], df.index[-1]])
		# fig.update_layout("yaxis_range", [-max, max])
		# fig.update_layout("xaxis_tickformat", "%H:%M")
		# fig.update_layout("yaxis_tickformat", "decimal")
		# fig.update_layout("xaxis_tickangle", 0)
		# fig.update_layout("yaxis_tickangle", 0)
		# fig.update_layout("xaxis_tickfont", dict(size=12))
		# fig.update_layout("yaxis_tickfont", dict(size=12))
		# fig.update_layout("xaxis_tickvals", df.index)

		fig.data[0].line.color = COLOR_PRODUCTION
		fig.data[1].line.color = COLOR_CONSUMPTION
		fig.data[2].line.color = COLOR_NET_CONSUMPTION

		return fig


def create_grapher(graph_range: str) -> Grapher:
	if graph_range == '7d':
		return GraphMomentary(None, 7 * 24 * 60,  60*60,  '1T', 20)
	if graph_range == '3d':
		return GraphMomentary(None, 3 * 24 * 60,  60*60, '1T', 20)
	if graph_range == '1d':
		return GraphMomentary(None, 24 * 60,      30*60, '1T', 20)
	elif graph_range == '12h':
		return GraphMomentary(None, 12 * 60,      10*60, '1T', 20)
	elif graph_range == '6h':
		return GraphMomentary(None, 6 * 60,       5*60,  '1T', 10)
	elif graph_range == '3h':
		return GraphMomentary(None, 3 * 60,       5*60,  '1T', 5)
	elif graph_range == '1h':
		return GraphMomentary(None, 60,           1*60,  '30S', 5)
	else:    # '30m'
		return GraphMomentary(None, 30,           30,   '', 0)
