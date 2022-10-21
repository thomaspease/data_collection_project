from sqlalchemy import create_engine
import pandas as pd
import boto3
import json
import requests

class RDSUpserter():
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
    df = pd.read_sql(f"select prop_id from {db}", self.engine)
    print(df)

  def search_for_id(self, prop_id):
    thing = self.engine.execute(f'''SELECT * FROM all_data WHERE prop_id={prop_id}''').fetchall()
    return thing

  def upsert(self, raw_list):
    jsonified_list = json.dumps(raw_list)
    df = pd.read_json(jsonified_list)
    try:
      df.to_sql('all_data', self.engine, if_exists='append')
      print('Data upserted')
    except:
      print('Data not upserted')

class S3Upserter():
  def __init__(self):
    self.s3 = boto3.resource('s3')
    self.client = boto3.client('s3')
  
  def upsert_json_from_data_folder(self, name):  
    try:
      self.s3.meta.client.upload_file(f'data/data_{name}.json', 'rightmove-scraper', f'data_{name}.json')
      print('Raw data pushed to S3')
    except:
      print('Raw data not pushed to S3')
  
  def get_image_and_upsert(self, url, name):
    res = requests.get(url, stream = True)

    if res.status_code == 200:
      self.s3.meta.client.upload_fileobj(res.raw, 'rightmove-scraper', name)
    else:
      print('Image couldn\'t be uploaded')

  def dl_image(self):
    self.s3.meta.client.download_file('rightmove-scraper', 'testphoto1.jpeg', 'data/hello1.jpeg')
