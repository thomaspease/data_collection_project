import sys
import unittest
sys.path.append('/Users/tompease/documents/coding/aicore/data_collection_pipeline')
from controller import RightmoveScraper
import time

class ScraperTestCase(unittest.TestCase):
    def setUp(self):
      url = 'https://www.rightmove.co.uk/commercial-property-for-sale/find.html?locationIdentifier=REGION%5E87490&maxPrice=800000&propertyTypes=&includeSSTC=false&mustHave=&dontShow=&furnishTypes=&areaSizeUnit=sqft&keywords='
      link_element_xpath = '//a[@class="propertyCard-link property-card-updates"]'

      #Set up scraper and get list of advert links from the first page
      self.scraper = RightmoveScraper(url, link_element_xpath)
      self.scraper.driver.get(self.scraper.start_url)
      self.scraper.get_and_store_links_from_list(self.link_element_xpath, self.scraper.link_list)

      #Collect info from the first 7 listings
      for i in range(7):
        self.driver.get(self.link_list[i])
        time.sleep(0.3)
        prop_data = self.get_property_details()
        self.scraped_data.append(prop_data)

    
    def test_find_and_click_next(self):
      next_page='//*[@data-test="pagination-next"]'
      self.scraper.driver.get(self.scraper.start_url)
      self.scraper.find_and_click(next_page)

      expected_value = 'index=24'
      actual_value = self.scraper.driver.current_url
      self.assertIn(expected_value, actual_value)

    def test_store_links_from_list(self):
      expected_value = 'www.rightmove.co.uk/properties/'
      self.assertIn(expected_value, self.scraper.link_list[5])

    def test_get_location(self):
      self.assertLessEqual(self.prop_data['location'][0], 90)
      self.assertLessEqual(self.prop_data['location'][1], 180)
      self.assertEqual(len(self.prop_data['location']), 2)

    def test_get_images(self):
        jpeg = self.prop_data['img_list'][0][-4:]
        self.assertEquals(jpeg, 'jpeg')


    
    








unittest.main(argv=[''], verbosity=3, exit=False)