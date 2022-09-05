import urllib
import json
import logging

from custom_code.s3 import S3
from custom_code.data_parsers import CarvagoDataParser
from custom_code.mysql_db import CarsTable, PriceHistoryTable, FeaturesTable, PhotosTable

logger = logging.getLogger()
logger.setLevel(logging.INFO)

client = S3.get_client()

def lambda_handler(event, context):
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    file_name = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    
    try:
        logger.info(f'Getting car data from {bucket_name}/{file_name}...')
        car_data = S3.get_file_from_bucket(
            bucket_name = bucket_name, 
            file_name = file_name, 
            as_json = True, 
            client = client)
        
        car = CarvagoDataParser(car_data)
        car_id = car.car_details['id']
        logger.info(f'Parsing car ({car_id}) data...')
        
        df_car_details = car.get_details()
        df_car_price = car.get_current_price()
        df_car_features = car.get_features()
        df_car_photos = car.get_photos()
        
        logger.info(f'Removing car ({car_id}) from database tables...')
        CarsTable.delete_by_id(car_id)
        FeaturesTable.delete_by_id(car_id)
        PhotosTable.delete_by_id(car_id)
        
        logger.info(f'Inserting car ({car_id}) from database tables...')
        CarsTable.insert_many(df_car_details)
        PriceHistoryTable.insert_many(df_car_price)
        FeaturesTable.insert_many(df_car_features)
        PhotosTable.insert_many(df_car_photos)
    
    except Exception as e:
        logger.info('Exception occured!!')
    
    logger.info(f'Car ({car_id}) processed succesfully!!')
    
    return {
        'statusCode': 200,
        'body': car_data
    }
