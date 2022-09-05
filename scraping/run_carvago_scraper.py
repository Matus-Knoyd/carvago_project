# CRON
# 09 17 * * * cd /home/ubuntu/carvago && /home/ubuntu/anaconda3/bin/python run_carvago_scraper.py 

import os
import json
import pandas as pd

from dotenv import load_dotenv
from libs.scrapers.carvago import CarvagoScraper
from libs.help_functions import get_current_time_string
from libs.s3 import S3

from libs.logger import Logger
logger = Logger().get_full_logger('./logs/carvago_scraping.log')

# load env variables
load_dotenv()

PATH_TO_CHROMEDRIVER = os.getenv('PATH_TO_CHROMEDRIVER')
BUCKET_NAME = os.getenv('AWS_BUCKET_NAME')
S3_CREDENTIALS = {
    'aws_access_key_id': os.getenv('AWS_ACCESS_KEY_ID'),
    'aws_secret_access_key': os.getenv('AWS_SECRET_ACCESS_KEY')
}

LINK = 'https://carvago.com/sk/auta?car-style[]=3&cruise-control[]=2&cruise-control-any=true&fuel-type[]=2&interior-material[]=1&price-to=40000&registration-date-from=2017&transmission[]=2&model-family-group[]=1785'

logger.info('Process started!')

def run():
    try:
        scraper = CarvagoScraper(headless=True, sleep_time=2, path_to_chromedriver=PATH_TO_CHROMEDRIVER)
        descriptions = scraper.get_advertised_cars(LINK)
        num_cars = len(descriptions)

        for i,description in enumerate(descriptions):
            logger.info(f'Scraping car details: {i+1}/{num_cars}')

            car_id = description['id']
            car_url = description['url']
            current_time = get_current_time_string()

            car_details = scraper.get_car_details(car_url)

            if car_details:
                car_details['id'] = car_id
                car_details['datetime'] = current_time

                S3.store_file_in_bucket(
                    bucket_name = BUCKET_NAME, 
                    file_name = f'car_details_{car_id}_{current_time}.json', 
                    file = json.dumps(car_details), 
                    credentials = S3_CREDENTIALS
                )
    except Exception as e:
        logger.exception('Exception occured!!')
        
if __name__ == "__main__":
    run()