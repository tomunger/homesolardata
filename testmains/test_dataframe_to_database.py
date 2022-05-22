
#
# A brief snipit that shows how to add data from a dataframe to a database table.
#
import sqlalchemy
import pandas as pd
import json

with open("../localconfig.json", "r") as f:
	config = json.load(f)


#
# The database and table we write to.  This is not taken from the confuguration file for flexibility.
to_db_name = "enphasesolar"
to_db_table = "production"


solardf = pd.read_csv("solardata.csv")


connectionstr = f"mysql+pymysql://{config['solardb_user']}:{config['solardb_pass']}@{config['solardb_host']}/{to_db_name}?charset=utf8mb4"
engine = sqlalchemy.create_engine(connectionstr)
engine.connect()

solardf.to_sql(to_db_table, engine, index=True, index_label='timestamp', if_exists='append')

