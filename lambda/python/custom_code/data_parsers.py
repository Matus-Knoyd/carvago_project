import datetime as dt
import pandas as pd

class CarvagoDataParser:
    def __init__(self, car_details):
        self.car_details = car_details
        
    def get_details(self, as_dataframe=True):
        data = {
            'id': self.car_details['id'],
            'url': self.car_details['url'],
            'make': self.car_details['make'],
            'model': self.car_details['model'],
            'color': self.car_details['body_color'],
            'interior_colour': self.car_details['interior_colour'],
            'body': self.car_details['body'],
            'power': self.car_details['power'].replace('kW','').strip(),
            'drive_type': self.car_details['drive_type'],
            'transmission': self.car_details['transmission'],
            'mileage': self.car_details['kms_driven'].replace('km', '').replace(' ', ''),
            'registration': dt.datetime.strptime(self.car_details.get('first_registration','01/2017'), '%m/%Y')
        }
        
        if as_dataframe:
            df = pd.DataFrame([data])
            df['registration'] = pd.to_datetime(df['registration'])
            return df
        
        return data
           
    def get_current_price(self, as_dataframe=True):
        data = {
            'id': self.car_details['id'],
            'datetime': self.car_details['datetime'],
            'price': self.car_details['price']
        }
        
        if as_dataframe:
            df = pd.DataFrame([data])
            df['datetime'] = pd.to_datetime(df['datetime'])
            return df
        
        return data
    
    def get_features(self, as_dataframe=True):
        features = self.car_details['features']
        id_ = self.car_details['id']
        
        if as_dataframe:
            df = pd.DataFrame(features, columns=['feature'])
            df['id'] = id_
            return df
        
        return list(zip(features,[id_]*len(features)))
    
    def get_photos(self, as_dataframe=True):
        photos = self.car_details['photos']
        id_ = self.car_details['id']
        
        if as_dataframe:
            df = pd.DataFrame(photos, columns=['url'])
            df['id'] = id_
            return df
        
        return list(zip(photos,[id_]*len(photos)))