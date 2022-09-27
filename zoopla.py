from selenium import webdriver
from selenium.webdriver.common.by import By
import time


driver = webdriver.Chrome()
URL = "https://www.zoopla.co.uk/new-homes/property/london/?q=London&results_sort=newest_listings&search_source=new-homes&page_size=25&pn=1&view_type=list"
driver.get(URL)

time.sleep(1) # Wait a couple of seconds, so the website doesn't suspect you are a bot
def accept_cookies(driver):
  try: 
      driver.switch_to.frame('gdpr-consent-notice') # This is the id of the frame
      accept_cookies_button = driver.find_element(by=By.XPATH, value='//*[@id="save"]')
      accept_cookies_button.click()

  except:
      pass # If there is no cookies button, we won't find it, so we can pass


accept_cookies(driver)
property_container = driver.find_element(by=By.XPATH, value='//*[@data-testid="regular-listings"]') # Change this xpath with the xpath the current page has in their properties
properties = property_container.find_elements(by=By.XPATH, value='./div')
link_list = []

for house_property in properties:
    a_tag = house_property.find_element(by=By.TAG_NAME, value='a')
    link = a_tag.get_attribute('href')
    link_list.append(link)


print(f'There are {len(link_list)} properties in this page')
print(link_list)

next_button = driver.find_element(by=By.XPATH, value='//*@li[text()="Next"]')
next_button.click()

