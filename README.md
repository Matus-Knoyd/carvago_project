# Carvago project
This project contains three folders

1. scraping - This folder contains code responsible for scraping cars from carvago.com and storing them to S3.
2. lambda - This folder contains AWS lambda function together with custom layer. This code parses data stored in S3 and inserts them into multiple tables inside MySQL whenever new cars are inserted into S3.
3. dashboard - This folder contains the Dash application responsible for visualizing scraped cars' data.

To start these applications read the README file in each folder.
