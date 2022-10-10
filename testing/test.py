import sys
import unittest
sys.path.append('/Users/tompease/documents/coding/aicore/data_collection_pipeline')
from rightmove import RightMoveScraper

class ScraperTestCase(unittest.TestCase):
    def setUp(self):
      url = 'https://www.rightmove.co.uk/commercial-property-for-sale/find.html?locationIdentifier=REGION%5E87490&maxPrice=800000&propertyTypes=&includeSSTC=false&mustHave=&dontShow=&furnishTypes=&areaSizeUnit=sqft&keywords='
      self.scraper = RightMoveScraper(url)
      self.scraper.driver.get('https://www.rightmove.co.uk/properties/111775718#/?channel=COM_BUY')
      self.prop_id, self.prop_data = self.scraper.get_property_details()
    
    def test_find_and_click_next(self):
      next_page='//*[@data-test="pagination-next"]'
      self.scraper.driver.get(self.scraper.start_url)
      self.scraper.find_and_click(next_page)

      expected_value = 'index=24'
      actual_value = self.scraper.driver.current_url
      self.assertIn(expected_value, actual_value)

    def test_store_links_from_list(self):
      link_container = '//a[@class="propertyCard-link property-card-updates"]'
      self.scraper.driver.get(self.scraper.start_url)
      self.scraper.get_and_store_links_from_list(link_container, self.scraper.link_list)
      expected_value = 'www.rightmove.co.uk/properties/'
      self.assertIn(expected_value, self.scraper.link_list[7])

    def test_get_location(self):
      self.assertLessEqual(self.prop_data['location'][0], 90)
      self.assertLessEqual(self.prop_data['location'][1], 180)
      self.assertEqual(len(self.prop_data['location']), 2)








unittest.main(argv=[''], verbosity=3, exit=False)