import requests

class FeatchApi:
    
    def __init__(self, lat, lng, r):
        self.lat = lat
        self.lng = lng
        self.r = r
    
    def fetch_aed_date(self):
        
        url = f"https://aed.azure-mobile.net/api/AEDSearch?lat={self.lat}&lng={self.lng}&r={self.r}"
        response = requests.get(url)
        
        return response.json()
    

