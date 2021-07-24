"""app.coordinates.py"""

class Coordinates:  
def __init__(self, lat_long):  
self.lat_long = lat_long  

if __name__ == "__main__":  
us_lat, us_long = 45, 60  
us = Point(us_lat, us_long) 
us_coord = Coorinates(us) 



class Point:  

def __init__(self, x, y):  
self.x = x  
self.y = y  
