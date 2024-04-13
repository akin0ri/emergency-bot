import featch_api
import pandas as pd

class StoreData:
    
    def __init__(self, featch_data):
        self.featch_data = featch_data
    
    def aed_data_to_pandas(self):
        aed_data = self.featch_data
        select_data = [{'DIST':data['DIST'], 'LocationName':data['LocationName'], 'ADRESS':data['Perfecture'] + data['City'] + data['AddressArea'] + " " + data['FacilityName'], 'FacilityPlace':data['FacilityPlace'], 'Lat':data['Latitude'], 'Lng':data['Longitude']} for data in aed_data]
        
        return pd.DataFrame(select_data)