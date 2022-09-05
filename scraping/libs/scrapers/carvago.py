import re
import time
import logging

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

from libs.scrapers.base import BaseScraper

logger = logging.getLogger(__name__)


class CarvagoScraper(BaseScraper):
    def __init__(self, path_to_chromedriver: str = '', headless: bool = True, sleep_time: float = 1):
        """
        Parameters
        ----------
        path_to_chromedriver: str 
            Path to executable of chromedriver
        headless: bool
            Browser headles
        sleep_time: float
            Sleep time in seconds between requests
        """
        
        self.PATH_TO_CHROMEDRIVER = path_to_chromedriver
        self.HEADLESS = headless
        self.SLEEP_TIME = sleep_time
    
    @staticmethod   
    def _parse_price(text: str) -> float:
        """
        Get price from scraped price node
        
        Parameters
        ----------
        text: str
            Scraped text to parse price from
            
        Returns
        -------
        float
            Parsed price
        """
        return re.findall('\d+', text.replace(' ', ''))[0]
    
    @staticmethod
    def get_id_from_car_url(url: str) -> str:
        """
        Get advertisement id from car url

        Parameters
        ----------
        url: str 
            Car url

        Returns
        -------
        str
            Advertisement id
        """
        from_index = url.find('car/') + len('car/')
        to_index = url.rfind('/')

        return url[from_index:to_index]

    @staticmethod
    def _add_page_num_to_url(url: str, page_num: int) -> str:
        """
        Add or replace page number to url

        Parameters
        ----------
        url: str 
            Base url to modify
        page_num: str
            Page number to append or replace

        Returns
        -------
        str
            Modified url containing paga_num
        """
        if re.findall('page=\d+', url):
            new_url = url.replace(re.findall('page=\d+', url)[0], f'page={page_num}')
        else:
            new_url = f'{url}&page={page_num}'

        return new_url
    
    @staticmethod
    def _get_cards_description(browser: webdriver) -> set:
        """
        Get cards description (url, id, price)

        Parameters
        ----------
        browser: webdriver 
            Instance of webdriver

        Returns
        -------
        list
            Description to all cars found on current page
        """
        descriptions = []
        for card in browser.find_elements_by_class_name('gtm-element-visibility-impressions-list'):
            description = {}
            
            try:
                description['id'] = card.get_attribute('data-car-id').strip()
                description['url'] = card.get_attribute('href').strip()
                description['price'] = CarvagoScraper._parse_price(card.find_element_by_class_name('e14v3bw44').text.strip())
            
            except Exception as e:
                logger.warning(e)
            
            descriptions.append(description)

        return descriptions
    
    @staticmethod
    def _get_max_page_num(browser: webdriver) -> int:
        """
        Get total number of pages

        Parameters
        ----------
        browser: webdriver 
            Instance of webdriver

        Returns
        -------
        int
            Count pages
        """
        
        return int(browser.find_elements_by_class_name('Pagination-item')[-1].text.strip())
    
    def _load_url(self, browser: webdriver, url: str, max_retries: int = 1) -> None:
        """
        Load url

        Parameters
        ----------
        browser: webdriver 
            Instance of webdriver
            
        url: str 
            Url to load
            
        max_retries: int
            How many retries is possible
        """
        logging.info(f'Loading: {url}')
        
        sleep_time = self.SLEEP_TIME
        retries = 1
        while True:
            try:
                browser.get(url)
                break
            except:
                if retry == max_retries:
                    raise
                else:
                    sleep_time *= 2
                    retries += 1
                    time.sleep(sleep_time)
                    
                    
        time.sleep(self.SLEEP_TIME)
        browser.maximize_window()
    
    def _init_browser(self) -> webdriver:
        """
        Initialize browser

        Returns
        -------
        set
            Urls to all cars found on current page
        """
        chrome_options = Options()
        chrome_options.add_argument("--disable-popup-blocking")
        chrome_options.add_argument("--incognito")
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
        
        if self.HEADLESS:
            chrome_options.add_argument("--headless")
        
        if self.PATH_TO_CHROMEDRIVER == '':
            return webdriver.Chrome(options=chrome_options)
  
        return webdriver.Chrome(self.PATH_TO_CHROMEDRIVER, options=chrome_options)

    def get_advertised_cars(self, url: str, page_limit: int = 1000) -> list:
        """
        Get advertised cars description (url, id, price)
        
        Parameters
        ----------
        url: str
            Search url (first page of search)
            
        page_limit: int
            Maximum number of pages to search on

        Returns
        -------
        list
            All available cars cards description
        """
        descriptions = []
        with self._init_browser() as browser:
            # load main page
            self._load_url(browser, url, 5)
            
            # get total number of pages
            max_page_num = CarvagoScraper._get_max_page_num(browser)
            logger.info(f'Found {max_page_num} pages!')
            
            for page_num in range(1, min(max_page_num, page_limit) + 1):
                logger.info(f'Scraping page {page_num}/{max_page_num}...')
                # consider page num in url
                page_url = CarvagoScraper._add_page_num_to_url(browser.current_url, page_num)
                
                # load page
                try:
                    self._load_url(browser, page_url, 5)
                except Exception as e:
                    logger.warning(e)
                    continue
                
                # load cards descriptions from current page
                new_descriptions = CarvagoScraper._get_cards_description(browser)
                
                descriptions += new_descriptions
        
        return descriptions
    
    def _get_photos_urls(self, browser: webdriver) -> list:
        """
        Get urls to all photos from car page

        Parameters
        ----------
        browser: webdriver 
            Instance of webdriver

        Returns
        -------
        list
            All available links to car photos
        """
        photos_urls = []

        try:
            # click on first image
            browser.find_element_by_class_name('image-gallery-image').click()
            time.sleep(self.SLEEP_TIME)

            # load all photos urls
            photos_urls = [
                elem.find_element_by_tag_name('img').get_attribute('src') 
                for elem in browser.find_elements_by_class_name('e1sb5aaj0')
            ]
        except Exception as e:
            logger.warning(e)

        return photos_urls
    
    def get_car_details(self, url: str, browser: webdriver = None, with_photos: bool = False) -> dict:
        """
        Get all available informations about advertised car
        
        Parameters
        ----------
        url: str
            Car url 
            
        browser: webdriver 
            Instance of webdriver

        Returns
        -------
        dict
            Informations about advertised car
        """
        called_without_browser = False
        try:
            # init browser if not passed as argumennt
            if browser is None:
                called_without_browser = True
                browser = self._init_browser()

            self._load_url(browser, url, 5)

            car_details = {}
            car_details['photos'] = []
            car_details['url'] = url
            car_details['price'] = CarvagoScraper._parse_price(browser.find_element_by_class_name('e1hgzarh2').text.strip())

            # load brand, mileage, color,...
            for name_elem, value_elem in zip(
                browser.find_elements_by_class_name('e18uvu5d2'), 
                browser.find_elements_by_class_name('e18uvu5d4')
            ):
                name = '_'.join(name_elem.text.strip().lower().split(' '))
                value = value_elem.text.strip()
                car_details[name] = value

            # load additional features
            car_details['features'] = [elem.text.strip() for elem in browser.find_elements_by_class_name('eoxqr1g1')]

            # load photos
            if with_photos:
                car_details['photos'] = self._get_photos_urls(browser)

            # if function is not called in loop => quit browser
            if browser and called_without_browser:
                browser.quit()
        
        except Exception as e:
            logger.warning(e)
            return None
        
        return car_details
    
    def get_multiple_cars_details(self, urls: list, with_photos: bool = False) -> list:
        """
        Get all available informations about multiple cars at once
        
        Parameters
        ----------
        urls: list
            Urls to advertised cars

        Returns
        -------
        list
            Informations about all cars from list
        """
        cars_details = []
        len_urls = len(urls)
        
        with self._init_browser() as browser:
            for i, url in enumerate(urls):
                logger.info(f'Scraping {i+1}/{len_urls}')
                car_details = self.get_car_details(url, browser, with_photos)
                if car_details:
                    cars_details.append(car_details)
                    
        return cars_details