import typing as t
import json
import pandas as pd
import sqlalchemy
import yaml


DB_CONFIG = dict[str,str]

def load_config(filename: str) -> tuple[list[DB_CONFIG], DB_CONFIG]:

    with open(filename, "r") as f:
        config = json.load(f)
    return config['source'], config['target']

def load_yaml_config(filename: str) -> tuple[list[DB_CONFIG], DB_CONFIG]:

    with open(filename, "r") as f:
        config = yaml.safe_load(f) 
    return config['source'], config['target']




def load_database(config: DB_CONFIG) -> pd.DataFrame:
    connectionstr = f"mysql+pymysql://{config['solardb_user']}:{config['solardb_pass']}@{config['solardb_host']}/{config['solardb_name']}?charset=utf8mb4"
    engine = sqlalchemy.create_engine(connectionstr)
    engine.connect()

    #solardf = pd.read_sql_table('production', engine)
    sql =  '''
    SELECT datetime, consumption, production FROM production 
        ORDER by datetime asc
    '''
    solardf = pd.read_sql(sql, engine) #, index_col='datetime')    
    return solardf


def save_database(config: DB_CONFIG, data: pd.DataFrame) -> None:
    connectionstr = f"mysql+pymysql://{config['solardb_user']}:{config['solardb_pass']}@{config['solardb_host']}/{config['solardb_name']}?charset=utf8mb4"
    engine = sqlalchemy.create_engine(connectionstr)
    engine.connect()
    data.to_sql(config['solardb_table'], engine, index=True, if_exists='replace')


