
#
# A brief snipit that shows how to add data from a dataframe to a database table.
#
import sqlalchemy
import pandas as pd

solardf = pd.read_csv("solardata.csv")


connectionstr = f"mysql+pymysql://{config['dbuser']}:{config['dbpass']}@lita.local/enphasesolar?charset=utf8mb4"
engine = sqlalchemy.create_engine(connectionstr)
engine.connect()

solardf.to_sql('production', engine, index=True, index_label='timestamp', if_exists='append')

