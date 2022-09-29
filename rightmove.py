
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import uuid
import urllib
import json

class Scraper:
  def __init__(self, start_url, cookies_alert, next_page=''):
    self.driver = webdriver.Chrome()
    self.start_url = start_url
    self.link_list = []
    self.next_page = next_page
    self.cookies_alert = cookies_alert
    self.scraped_data = {}
  
  def find_and_click(self, xcode, wait=0, br=True):
    try:
      time.sleep(wait)
      target =  self.driver.find_element(By.XPATH, f'{xcode}')
      target.click()
    except:
      if br == True:  
        print(f'Could not find and click {xcode}! 💥💥💥')
      if br == False:
        print(f'Could not find and click {xcode}! 💥💥💥')
        pass

  def gather_links(self):
    link_boxes = self.driver.find_elements(By.XPATH, '//a[@class="propertyCard-link property-card-updates"]')
    for link in link_boxes: 
      self.link_list.append(link.get_attribute('href'))
  
  def store_detail(self, xcode, path):
    self.scraped_data[path] = self.driver.find_element(By.XPATH, f'{xcode}')

  def save_dictionary(self):
    with open("sample.json", "w") as fp:
      json.dump(self.scraped_data, fp, indent=4)

  def log_property_details(self):
    def get_location():
      location_str = self.driver.find_element(By.XPATH, '//*[@class="_1kck3jRw2PGQSOEy3Lihgp"]/img').get_attribute('src') #Gets URL of map displaying the location, which has the coordinates
      coord_str = location_str.split('latitude=')[1].split('&longitude=')
      coord_str[1] = coord_str[1].split('&signature')[0]
      coord_floats = [float(x) for x in coord_str]
      return coord_floats

    def get_images():
      collage = self.driver.find_element(By.XPATH, '//*[@class="yyidGoi1pN3HEaahsw3bi"]/a')
      self.driver.get(collage.get_attribute('href'))
      container = WebDriverWait(self.driver, 5).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@class="_2BEYToQ5mjPuC5vD8izBf0 oimOnSwjvoYo82ZTqOaXp"]/img')))
      img_list = [imgs.get_attribute('src') for imgs in container]
      self.driver.back()
      return img_list
  
    def get_sq_ft():
      try:
        sq_ft = int(self.driver.find_element(By.XPATH, '//*[@class="_1hV1kqpVceE9m-QrX_hWDN  "]').text.replace(' sq. ft.', '').replace(',', ''))
        return sq_ft
      except:
        return None

    def get_price():
      try:
        price = int(self.driver.find_element(By.XPATH, '//*[@class="_1gfnqJ3Vtd1z40MlC0MzXu"]').text.replace('£', '').replace(',', ''))
        return price
      except:
        return None
      
    description = self.driver.find_element(By.XPATH, '//*[contains(@class, "STw8udCxUaBUMfOOZu0iL")]').text
    url = self.driver.current_url
    prop_id = url.split('https://www.rightmove.co.uk/properties/')[1].split('#/')[0] #Chops up the URL to just have the id

    price = get_price()
    img_list = get_images()
    sq_ft = get_sq_ft()
    location = get_location()
    uuid1 = str(uuid.uuid4())

    self.scraped_data[prop_id] = {
      "price" : price,
      "sq_ft" : sq_ft,
      "location" : location,
      "description" : description,
      "img_list" : img_list,
      "uuid" : uuid1
    }

if __name__ == "__main__":
  # start_url='https://www.rightmove.co.uk/commercial-property-for-sale/find.html?locationIdentifier=USERDEFINEDAREA%5E%7B%22polylines%22%3A%22q_nuHkpdHn%7BuEn%7Bim%40a~%7BMurf%40%7D%7BpMcb%60DyltKh%7CpGah%7DLmmbF%60br%40otnN%7C~aGaj~FnpjNitcA%60pfN_%7DvSxoaHh~yC%22%7D&maxPrice=1000000&sortType=2&propertyTypes=land%2Ccommercial-development%2Cindustrial-development%2Cresidential-development%2Cfarm%2Cdistribution-warehouse%2Cfactory%2Cheavy-industrial%2Cindustrial-park%2Clight-industrial%2Cshowroom%2Cstorage%2Ctrade-counter%2Cwarehouse%2Coffice%2Cserviced-office%2Cbusiness-park&mustHave=&dontShow=&furnishTypes=&areaSizeUnit=sqft&keywords='
  cookies_alert='//*[@class="optanon-allow-all accept-cookies-button"]'
  next_page='//*[@data-test="pagination-next"]'
  start_url='https://www.rightmove.co.uk/properties/85704885#/?channel=COM_BUY'
  
  scraper = Scraper(start_url, cookies_alert, next_page)
  scraper.driver.get(scraper.start_url)
  scraper.log_property_details()

  # scraper.find_and_click(scraper.cookies_alert, 1, False)
  
  # scraper.gather_links()

  # for link in scraper.link_list:
  #   scraper.driver.get(link)
  #   time.sleep(0.5)
  #   scraper.log_property_details()

  # scraper.save_dictionary()



 
  # cookies_alert='//*[@class="optanon-allow-all accept-cookies-button"]'
  # scraper = Scraper(start_url, cookies_alert)
  # scraper.driver.get(scraper.start_url)
  # scraper.find_and_click(scraper.cookies_alert, 1, False)
  # scraper.log_property_details()

  # urllib.request.urlretrieve('https://media.rightmove.co.uk/229k/228224/85704885/228224_OtterandWatersideHouseUxbridge_IMG_00_0000.jpeg', 'images/new_file.jpg')

  # Blair questions
  # Should I make loc_details a seperate class or no?