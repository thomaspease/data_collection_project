import sys
import pytest
sys.path.append('/Users/tompease/documents/coding/aicore/data_collection_pipeline')
from scraper import RightmoveScraper
import time


def return_value(list, desired_key):
  for item in list:
    if item[desired_key]:
      return item[desired_key]
    else:
      pass

@pytest.fixture
def scraper():
  start_url = 'https://www.rightmove.co.uk/commercial-property-for-sale/find.html?locationIdentifier=REGION%5E87490&maxPrice=800000&propertyTypes=&includeSSTC=false&mustHave=&dontShow=&furnishTypes=&areaSizeUnit=sqft&keywords='
  link_element_xpath = '//a[@class="propertyCard-link property-card-updates"]'

  #Set up scraper and get list of advert links from the first page
  scraper = RightmoveScraper()
  scraper.driver.get(start_url)
  scraper.get_and_store_links_from_list(link_element_xpath, scraper.link_list)
  return scraper

@pytest.fixture
def prop_detail_scraper(scraper):
  for property in range(7):
    scraper.driver.get(scraper.link_list[property])
    time.sleep(0.3)
    prop_data = scraper.get_property_details()
    scraper.scraped_data.append(prop_data)

  return scraper

def test_find_and_click_next(scraper):
  next_page='//*[@data-test="pagination-next"]'
  scraper.find_and_click(next_page)
  assert 'index=24' in scraper.driver.current_url

def test_store_links_from_list(scraper):
  assert 'www.rightmove.co.uk/properties/' in scraper.link_list[5]

def test_get_property_details(prop_detail_scraper):
  assert isinstance(prop_detail_scraper.scraped_data, list)
  assert len(prop_detail_scraper.scraped_data) == 7

def test_get_location(prop_detail_scraper):
  location = return_value(prop_detail_scraper.scraped_data, 'location')
  assert location[0] <= 90
  assert location[1] <= 180
  assert len(location) == 2

def test_get_images(prop_detail_scraper):
  img_list = return_value(prop_detail_scraper.scraped_data, 'img_list')
  print(img_list)
  jpeg = img_list[0][-4:]
  assert jpeg == 'jpeg'

def test_get_sq_ft(prop_detail_scraper):
  sq_ft = return_value(prop_detail_scraper.scraped_data, 'sq_ft')
  assert isinstance(sq_ft, int)

def test_get_price(prop_detail_scraper):
  price = return_value(prop_detail_scraper.scraped_data, 'price')
  assert isinstance(price, int)

def test_get_description(prop_detail_scraper):
  description = return_value(prop_detail_scraper.scraped_data, 'description')
  assert isinstance(description, str)

def test_get_prop_id(prop_detail_scraper):
  prop_id = prop_detail_scraper.scraped_data[0]['prop_id']
  assert isinstance(prop_id, int)
  assert len(prop_id) >= 8