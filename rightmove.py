from os import link
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

class Scraper:
  def __init__(self):
    self.driver = webdriver.Chrome()
    self.start_url = ''
    self.link_list = []


  def build_start_url(self, location_code):
      self.start_url = f'https://www.rightmove.co.uk/property-for-sale/find.html?searchType=SALE&locationIdentifier={location_code}&insId=1&radius=0.0&sortType=6'
      # Tottenham is REGION%5E87532

  def accept_cookies(self):
    try: 
        accept_cookies_button = self.driver.find_element(by=By.XPATH, value='//*[@class="optanon-allow-all accept-cookies-button"]')
        time.sleep(1)
        accept_cookies_button.click()
    except:
        pass # If there is no cookies button, we won't find it, so we can pass

  def next_page(self):
    next_button = self.driver.find_element(by=By.XPATH, value='//*[@data-test="pagination-next"]')
    next_button.click()

  def gather_links(self):
    link_boxes = self.driver.find_elements(by=By.XPATH, value='//a[@class="propertyCard-link property-card-updates"]')
    for i in link_boxes: 
      self.link_list.append(i.get_attribute('href'))


    

scraper = Scraper()
scraper.build_start_url('REGION%5E87532')
scraper.driver.get(scraper.start_url)
scraper.accept_cookies()
scraper.gather_links()
# time.sleep(3)
# scraper.next_page()