# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.
import plotly.express as px
import pandas as pd
import sqlalchemy
import datetime
import dotenv
import os

dotenv.load_dotenv(dotenv_path='localenv-prod.txt')

def load_data(user: str, password: str, host: str, port: int, dbname: str, tablename: str, history_min:int) -> pd.DataFrame:
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

df = load_data(os.getenv('SOLARDB_USER'), os.getenv('SOLARDB_PASS'), 
						os.getenv('SOLARDB_HOST'), os.getenv('SOLARDB_PORT', 3306),
						os.getenv('SOLARDB_NAME'), os.getenv('SOLARDB_TABLE'), 60)
print (df.info())
fig = px.line(df)
fig.show()

