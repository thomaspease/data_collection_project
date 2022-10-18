from sqlalchemy import create_engine
import pandas as pd
import json

class Upserter():
  def __init__(self):
    DATABASE_TYPE = 'postgresql'
    DBAPI = 'psycopg2'
    HOST = 'rightmove-scraper-rds.cha5mybmehvu.eu-west-2.rds.amazonaws.com'
    USER = 'tom'
    PASSWORD = 'rightmove'
    DATABASE = 'postgres'
    PORT = 5432
    self.engine = create_engine(f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}")
    self.engine.connect()


  def show_all_data(self, db):
    df = pd.read_sql(f"select * from {db}", self.engine)
    print(df)

  def upsert(self, raw_list):
    jsonified_list = json.dumps(raw_list)
    df = pd.read_json(jsonified_list)
    try:
      df.to_sql('all_data', self.engine, if_exists='append')
      print('Data upserted')
    except:
      print('Data not upserted')