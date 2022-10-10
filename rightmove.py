
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from utils.errorhandling import handle_nosuch_and_value_error
import time
import uuid
import urllib
import json

class Scraper:
  '''
  A class used to scrape data from a suitable website

  Attributes:
    driver (webdriver): an instance of a selenium webdriver.
    start_url (str): the url that the driver will start on if it is scraping  product links from a series of pages.
    link_element_xpath (str): xpath to the elements where the hrefs to individual product pages can be found.
    link_list (list): the hrefs to individual product pages will be stored here.
    next_page_xpath (str): xpath to next page button.
    cookies_alert_xpath (str): xpath to cookies alert button.
    scraped_data (dict): dictionary to which scraped data is appended.
  '''

  def __init__(self, start_url=None, cookies_alert_xpath =None, next_page_xpath=None,link_element_xpath=None):
    '''
    See help(Scraper) for accurate signature
    '''
    options = Options()
    options.headless = True
    self.driver = webdriver.Chrome(options = options)
    self.start_url = start_url
    self.link_element_xpath = link_element_xpath
    self.link_list = []
    self.next_page_xpath = next_page_xpath
    self.cookies_alert_xpath = cookies_alert_xpath
    self.scraped_data = []
  
  def find_and_click(self, xpath, wait=0, br=True):
    '''
    A function to find an element by xpath and click it

    Args:
      xpath (str): the xpath to the element being clicked
      wait (int/float): the time to wait before finding and clicking, defaults to 0.
      br (bool): if set to true, the code will raise an exception if element not found, if set to false, the exception is passed. Defaults to true.
    '''
    try:
      time.sleep(wait)
      target =  self.driver.find_element(By.XPATH, xpath)
      target.click()
    except:
      if br == True:  
        print(f'Could not find and click {xpath}! 💥💥💥')
      if br == False:
        print(f'Could not find and click {xpath}! 💥💥💥')
        pass

  def get_and_store_links_from_list(self, xpath, link_list):
    '''
    A function that gets and stores links (e.g. of product pages) in a list

    Args:
      xpath (str): xpath of the elements which contain the hrefs that we want
      link_list (list - class attribute): the list which the links will be stored in, should be a class attribute. 
    '''
    link_boxes = self.driver.find_elements(By.XPATH, xpath)
    for link in link_boxes: 
      link_list.append(link.get_attribute('href'))

  def add_data_to_dict(self, dict, id, data):
    '''
    Appends data to a dictionary

    Args:
      dict (dict): a dictionary, must be a class attribute
      id (str): the key of the dictionary entry, likely to be a product id
      data (dict/*): the data of the product, or could be a simple value if the dictionary is not a product catalogue
    '''
    dict[data]

  def save_dictionary(self, dict, name):
    '''
    Saves the contents of a dictionary to a json file

    Args:
      dict (dict): the dictionary being jsonified
      name (str): the name that the file will be saved as
    '''
    with open(name, "w") as fp:
      json.dump(dict, fp, indent=4)

class RightmoveScraper(Scraper):
  '''
  A child class of the Scraper class, adding methods specific to scraping data from the Rightmove commercial property advertisment pages

  Attributes:
    See help(Scraper) for attributes
  # '''
  # def __init__(self, start_url=None, cookies_alert_xpath =None, next_page_xpath=None,link_element_xpath=None):
  #   super.__init__(self, start_url, cookies_alert_xpath, next_page_xpath,link_element_xpath)

  def get_property_details(self):
    '''
    A function which gets details from a Rightmove commercial property advertisment

    Returns
      prop_data (dict): the data which has been scraped, including:
        location (list): the coordinates of the property
        images (list): the urls of the property images
        sq_ft (int): the sq ft of the property, if listed
        price (int): the price, in £, of the property
        description (str): the property's description
        uuid (str): a stringified UUID4 identifier

      prop_id (str): the unique id of the property, taken from Rightmove's own id for the property in question
    '''
    @handle_nosuch_and_value_error
    def get_location():
      # Gets URL of map displaying the location, which has the coordinates
      location_str = self.driver.find_element(By.XPATH, '//*[@class="_1kck3jRw2PGQSOEy3Lihgp"]/img').get_attribute('src') 
      # Chops up the URL to leave just the values for longitude and latitude
      coord_str = location_str.split('latitude=')[1].split('&longitude=')
      coord_str[1] = coord_str[1].split('&signature')[0]
      # Converts the L&L from str to float
      coord_floats = [float(x) for x in coord_str]
      return coord_floats

    @handle_nosuch_and_value_error
    def get_images():
      # Gets URL for property image gallery 
      try:
        gallery = self.driver.find_element(By.XPATH, '//*[@class="yyidGoi1pN3HEaahsw3bi"]/a')
        self.driver.get(gallery.get_attribute('href'))
      except:
        gallery = self.driver.find_element(By.XPATH, '//*[@class="_30hgiLFzNTpFG4iV-9f6oK"]/a')
        self.driver.get(gallery.get_attribute('href'))
      # Goes to image gallery and waits for img elements (containing url filepaths) to load
      container = WebDriverWait(self.driver, 5).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@class="_2BEYToQ5mjPuC5vD8izBf0 oimOnSwjvoYo82ZTqOaXp"]/img')))
      # Compiles the urls into a list, and then returns to property page
      img_list = [imgs.get_attribute('src') for imgs in container]
      self.driver.back()
      return img_list

  
    # Wrapped by error handler as sq ft often not listed
    @handle_nosuch_and_value_error
    def get_sq_ft():
      sq_ft = int(self.driver.find_element(By.XPATH, '//*[@class="_1hV1kqpVceE9m-QrX_hWDN  "]').text.replace(' sq. ft.', '').replace(',', ''))
      return sq_ft

    # Wrapped by error handler as price sometimes not listed (e.g. 'POA')
    @handle_nosuch_and_value_error
    def get_price():
      try:
        price = int(self.driver.find_element(By.XPATH, '//*[@class="_1gfnqJ3Vtd1z40MlC0MzXu"]').text.replace('£', '').replace(',', ''))
        return price
      except:
        return None
      
    @handle_nosuch_and_value_error
    def get_description():
      description = self.driver.find_element(By.XPATH, '//*[contains(@class, "STw8udCxUaBUMfOOZu0iL")]').text
      return description

    url = self.driver.current_url
    prop_id = url.split('https://www.rightmove.co.uk/properties/')[1].split('#/')[0] #Chops up the URL to just have the id

    price = get_price()
    img_list = get_images()
    sq_ft = get_sq_ft()
    location = get_location()
    description = get_description()
    uuid1 = str(uuid.uuid4())

    prop_data = {
      "url": url,
      "prop_id": prop_id,
      "price" : price,
      "sq_ft" : sq_ft,
      "location" : location,
      "description" : description,
      "img_list" : img_list,
      "uuid" : uuid1
    }

    return prop_data

if __name__ == "__main__":
  start_url='https://www.rightmove.co.uk/commercial-property-for-sale/find.html?locationIdentifier=USERDEFINEDAREA%5E%7B%22polylines%22%3A%22q_nuHkpdHn%7BuEn%7Bim%40a~%7BMurf%40%7D%7BpMcb%60DyltKh%7CpGah%7DLmmbF%60br%40otnN%7C~aGaj~FnpjNitcA%60pfN_%7DvSxoaHh~yC%22%7D&maxPrice=1500000&sortType=2&propertyTypes=distribution-warehouse%2Cfactory%2Cheavy-industrial%2Cindustrial-park%2Clight-industrial%2Cshowroom%2Cstorage%2Ctrade-counter%2Cwarehouse%2Coffice%2Cserviced-office%2Cbusiness-park&mustHave=&dontShow=&furnishTypes=&areaSizeUnit=sqft&keywords='
  cookies_alert_xpath='//*[@class="optanon-allow-all accept-cookies-button"]'
  next_page_xpath='//*[@data-test="pagination-next"]'
  link_element_xpath = '//a[@class="propertyCard-link property-card-updates"]'
  # start_url='https://www.rightmove.co.uk/properties/127280450#/?channel=COM_BUY' 
  
  # Initialise webdriver, go to property list, accept cookies
  scraper = RightMoveScraper(start_url, cookies_alert_xpath, next_page_xpath, link_element_xpath)
  scraper.driver.get(scraper.start_url)
  scraper.find_and_click(scraper.cookies_alert_xpath, 1, False)

  # Scrape individual property links from as many pages as desired
  pages_to_scrape = 100
  for pages in range(pages_to_scrape):
    time.sleep(0.5)
    scraper.get_and_store_links_from_list(scraper.link_element_xpath, scraper.link_list)
    scraper.find_and_click(scraper.next_page_xpath, 0.5)
    print(len(scraper.link_list))

  # For each property in the list which has just been scraped, go to that page, scrape the data, and add it to a dictionary
  for link in scraper.link_list:
    scraper.driver.get(link)
    time.sleep(0.3)
    prop_data = scraper.get_property_details()
    scraper.scraped_data.append(prop_data)

  scraper.save_dictionary(scraper.scraped_data, 'sample1.json')