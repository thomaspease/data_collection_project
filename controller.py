from scraper import RightmoveScraper
from utils.upsert import Upserter


if __name__ == "__main__":
  start_url='https://www.rightmove.co.uk/commercial-property-for-sale/find.html?locationIdentifier=USERDEFINEDAREA%5E%7B%22polylines%22%3A%22q_nuHkpdHn%7BuEn%7Bim%40a~%7BMurf%40%7D%7BpMcb%60DyltKh%7CpGah%7DLmmbF%60br%40otnN%7C~aGaj~FnpjNitcA%60pfN_%7DvSxoaHh~yC%22%7D&maxPrice=1500000&sortType=2&propertyTypes=distribution-warehouse%2Cfactory%2Cheavy-industrial%2Cindustrial-park%2Clight-industrial%2Cshowroom%2Cstorage%2Ctrade-counter%2Cwarehouse%2Coffice%2Cserviced-office%2Cbusiness-park&mustHave=&dontShow=&furnishTypes=&areaSizeUnit=sqft&keywords='
  cookies_alert_xpath='//*[@class="optanon-allow-all accept-cookies-button"]'
  next_page_xpath='//*[@data-test="pagination-next"]'
  link_element_xpath = '//a[@class="propertyCard-link property-card-updates"]'
  # start_url='https://www.rightmove.co.uk/properties/127280450#/?channel=COM_BUY' 
  
  # Initialise webdriver, go to property list, accept cookies
  scraper = RightmoveScraper(start_url, cookies_alert_xpath, next_page_xpath, link_element_xpath)
  scraper.driver.get(scraper.start_url)
  scraper.find_and_click(scraper.cookies_alert_xpath, 1, False)

  # Scrape individual property links from as many pages as desired
  scraper.scrape_links_from_n_pages(1)

  # For each property in the list which has just been scraped, go to that page, scrape the data, and add it to a dictionary
  scraper.scrape_data_from_link_list()

  #Save locally
  #Upload json to S3 with an appropriate name
  #Upload images to S3
  scraper.save_dictionary(scraper.scraped_data, 'sample1.json')



  upserter = Upserter()
  upserter.show_all_data('all_data')
  upserter.upsert(scraper.scraped_data)
  upserter.show_all_data('all_data')