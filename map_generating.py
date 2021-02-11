from geopy.geocoders import Nominatim
from math import radians, cos, sin, asin, sqrt
import csv
import time

geolocator = Nominatim(user_agent='smth')

def haversine_distance(lng1, lat1, lng2, lat2) -> float:
    '''
    Return the distance between two point on Earth with given longitudes and 
    latitudes.
    '''
    lng1, lat1, lng2, lat2 = map(radians, [lng1, lat1, lng2, lat2]) #convert to radians
    dlng = lng2-lng1
    dlat = lat2-lat1
    value = 2*asin(sqrt(sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlng/2)**2))
    #haversine formula
    return value*6371 #6371 is a radius of Earth in km

def distance_films(year:int, lng:float, lat:float, file:str) -> list:
    '''
    Return list of tuples (each is (film, distance_in_km)) of films which were
    released in the given year, distance_in_km is distance from given point.
    '''
    list_of_films = []
    with open (file, 'r') as csv_file :
        csv_reader = csv.reader(csv_file, delimiter=',')
        for line in csv_reader :
            if int(line[1]) == year :
                location = geolocator.geocode(line[2])
                distance = haversine_distance(location.longitude,\
                     location.latitude, lng, lat)
                list_of_films.append((line[0], distance))
    return list_of_films
print(distance_films(2002, 24.02324, 49.83826, 'locations.csv'))


