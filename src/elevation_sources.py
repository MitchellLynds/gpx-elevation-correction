from abc import ABC, abstractmethod
import requests
import rasterio
from rasterio.io import MemoryFile
import numpy as np

class ElevationSource(ABC):
    """Abstract base class for elevation data sources"""

    @abstractmethod
    def get_elevation(self, latitude, longitude):
        """Get elevation at given coordinates, Returns elevation in meters"""
        pass

    @abstractmethod
    def get_name(self):
        """Return the name of this elevation source"""
        pass

class SRTMSource(ElevationSource):
    def __init__(self):
        import srtm 
        self.elevation_data = srtm.get_data()

    def get_elevation(self, latitude, longitude):
        return self.elevation_data.get_elevation(latitude, longitude)
    
    def get_name(self):
        return "SRTM"
    
class USGSPointQuerySource(ElevationSource):
    def __init__(self):
        self.base_url = "https://epqs.nationalmap.gov/v1/json"
        self.cache = {}
    
    def get_elevation(self, latitude, longitude):
        cache_key = f"{latitude:.6f},{longitude:.6f}"
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        params = {
            'x': longitude,
            'y': latitude,
            'units': 'Meters',
            'wkid': 4326,
            'includeDate': 'false'
        }
        
        try:
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # API returns elevation in "value" field
            if 'value' in data:
                elevation = float(data['value'])
                # Check for invalid values
                if elevation == -1000000 or elevation < -500 or elevation > 9000:
                    return None
                self.cache[cache_key] = elevation
                return elevation
            return None
            
        except Exception as e:
            print(f"Error: {e}")
            return None
    
    def get_name(self):
        return "USGS Point Query Service"