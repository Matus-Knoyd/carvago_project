from abc import ABC, abstractmethod

class BaseScraper(ABC):
    @abstractmethod
    def get_advertised_cars(self):
        pass
    
    @abstractmethod
    def get_car_details(self):
        pass
    
    @abstractmethod
    def get_multiple_cars_details(self):
        pass