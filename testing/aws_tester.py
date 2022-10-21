import sys
import pytest
sys.path.append('/Users/tompease/documents/coding/aicore/data_collection_pipeline')
from utils.upsert import RDSUpserter, S3Upserter

test_data = [
    {
        "url": "https://www.rightmove.co.uk/properties/85427586#/?channel=COM_BUY",
        "prop_id": "85427586000",
        "price": 1200000,
        "sq_ft": 9881,
        "location": [
            53.408624,
            -2.9838
        ],
        "description": "The Ternary is self-contained commercial space available to let or buy, in the centre of Liverpool arranged over basement, ground and first floors. The space benefits from excellent natural light levels, and currently features stylish exposed services; subject to change of use, the space would make an excellent office or gym.\n\nLocation Highlights\n\nThe Ternary is in a convenient city centre location, just minutes from Liverpool Lime Street Station which offers national rail links, and the popular Liverpool One retail destination. Parking options can be found at Queen Square and on Victoria Street, and The Mersey Tunnel is just a short drive away.\n\n\n\nFor specification details, please speak to one of our agents.\n\n\n\nAvailable on request.",
        "img_list": [
            "https://media.rightmove.co.uk/57k/56478/85427586/56478_15095FH_IMG_00_0000.jpeg",
            "https://media.rightmove.co.uk/57k/56478/85427586/56478_15095FH_IMG_01_0000.jpeg",
            "https://media.rightmove.co.uk/57k/56478/85427586/56478_15095FH_IMG_02_0000.jpeg",
            "https://media.rightmove.co.uk/57k/56478/85427586/56478_15095FH_IMG_03_0000.jpeg",
            "https://media.rightmove.co.uk/57k/56478/85427586/56478_15095FH_IMG_04_0000.jpeg"
        ],
        "uuid": "e4da341c-5398-43ce-bcff-562ededf1ab2"}]

@pytest.fixture
def rds():
  rds = RDSUpserter()
  return rds

@pytest.fixture
def s3():
  s3 = S3Upserter()
  return s3

def test_search_for_id(rds):
  result = rds.search_for_id(127024703)
  assert result


def test_upsert_to_rds(rds):
  rds.upsert(test_data)
  result = rds.search_for_id(85427586000)
  assert result
  
  rds.engine.execute('''DELETE FROM all_data WHERE prop_id=85427586000''')
  none_result = rds.search_for_id(85427586000)
  assert none_result == []

def test_upsert_json_from_data_folder(s3):
  s3.upsert_json_from_data_folder('test')
  response = s3.s3.meta.client.get_object(
    Bucket='rightmove-scraper',
    Key='data_test.json',
  )
  assert response

  s3.client.delete_object(
    Bucket='rightmove-scraper',
    Key='data_test.json',
  )
  with pytest.raises(Exception):
    s3.s3.meta.client.get_object(
    Bucket='rightmove-scraper',
    Key='data_test.json',
  )

def test_get_image_and_upsert(s3):
  s3.get_image_and_upsert("https://media.rightmove.co.uk/57k/56478/85427586/56478_15095FH_IMG_00_0000.jpeg", 'test_imgg.jpeg')
  response = s3.s3.meta.client.get_object(
    Bucket='rightmove-scraper',
    Key='test_imgg.jpeg',
  )
  assert response

  s3.client.delete_object(
    Bucket='rightmove-scraper',
    Key='test_imgg.jpeg',
  )
  with pytest.raises(Exception):
    s3.s3.meta.client.get_object(
    Bucket='rightmove-scraper',
    Key='test_imgg.jpeg',
  )