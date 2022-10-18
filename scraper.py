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

  def __init__(self, start_url=None, cookies_alert_xpath =None, next_page_xpath=None,link_element_xpath=None, headless=True):
    '''
    See help(Scraper) for accurate signature
    '''
    options = Options()
    options.headless = headless
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
    with open(f'data/{name}', "w") as fp:
      json.dump(dict, fp, indent=4)

class RightmoveScraper(Scraper):
  '''
  A child class of the Scraper class, adding methods specific to scraping data from the Rightmove commercial property advertisment pages

  Attributes:
    See help(Scraper) for attributes
  # '''
  def scrape_links_from_n_pages(self, pages_to_scrape):
    '''
    A function which scrapes the links to individual property pages from n pages

    Args:
      pages_to_scrape (int): the number of pages that links will be scraped from
    '''
    for pages in range(pages_to_scrape):
      time.sleep(0.3)
      self.get_and_store_links_from_list(self.link_element_xpath, self.link_list)
      self.find_and_click(self.next_page_xpath, 0.5)
      print(f'Links scraped: {len(self.link_list)}')

  def scrape_data_from_link_list(self):
    '''
    A function which loops through the links which have been collected, calling the get_property_details function on each page, and when appends the data to the scraped_data attribute
    '''
    for link in self.link_list:
      self.driver.get(link)
      time.sleep(0.3)
      prop_data = self.get_property_details()
      self.scraped_data.append(prop_data)

  def get_property_details(self):
    '''
    A function which gets details from a Rightmove commercial property advertisment

    Returns:
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