from selenium.webdriver.common.by import By


class CarScraper():
    def __init__(self, driver):
        self.driver = driver
       
    
    # cars
    def get_cars_names(self, class_name = 'car-name'):
        return [car.text for car in self.driver.find_elements(By.CLASS_NAME, class_name)]
    
    # cities
    def get_car_cities(self, class_name='search-vehicle-info'):
        return [city.text for city in self.driver.find_elements(By.CLASS_NAME, class_name)]
    
    # price
    def get_car_prices(self, class_name= 'price-details'):
        return [price.text for price in self.driver.find_elements(By.CLASS_NAME, class_name)]
    

   # other specfications
    def get_vehicle_specs(self, class_name='search-vehicle-info-2'):
        specs = []

        details = self.driver.find_elements(By.CLASS_NAME, class_name)
        for detail in details:
            parts = detail.text.strip().split()
            if len(parts) >=7:
                specs.append({
                    "year": parts[0],
                    "mileage": parts[1] + " " + parts[2],
                    "fuel": parts[3],
                    "engine": parts[4] + " " + parts[5],
                    "transmission": parts[6]
                })
    
        return specs