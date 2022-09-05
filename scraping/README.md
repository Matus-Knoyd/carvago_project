# Carvago scraping
This folder contains code that is responsible for scraping cars from carvago.com and inserting them to AWS S3


1. Create empty python environment. Python version: 3.7.6
2. Install requirements: `pip install -r requirements.txt`
3. Start the app: `python run_carvago_scraper.py`


It is important to have following environmental variables specified (you can also set them in .env file):

- PATH_TO_CHROMEDRIVER: path to chromedriver executable
- AWS_ACCESS_KEY_ID: AWS boto credentials
- AWS_SECRET_ACCESS_KEY: AWS boto credentials
- AWS_BUCKET_NAME: S3 bucket name where cars will be stored

