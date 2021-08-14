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



class Person: 

def __init__(self, p, w):
	self.p = p
	self.w = w

personOne = Person("Abdullah", 190)

print(personOne.p)
print(personOne.w)

3
y
n
y
y
