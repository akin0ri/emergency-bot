import requests
import pandas as pd

def fetch_aed_data(lat, lng, r):
        
        url = f"https://aed.azure-mobile.net/api/AEDSearch?lat={lat}&lng={lng}&r={r}"
        response = requests.get(url)
        
        return response.json()
    
def aed_data_to_pandas(aed_data):
        select_data = [{'DIST':data['DIST'], 'LocationName':data['LocationName'], 'ADRESS':data['Perfecture'] + data['City'] + data['AddressArea'] + " " + data['FacilityName'], 'FacilityPlace':data['FacilityPlace'], 'Lat':data['Latitude'], 'Lng':data['Longitude']} for data in aed_data]
        
        return pd.DataFrame(select_data)