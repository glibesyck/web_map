'''
Module for building a map and some practical functions!
'''
from math import radians, cos, sin, asin, sqrt
import csv
import folium

def haversine_distance(lng1, lat1, lng2, lat2) -> float:
    '''
    Return the distance between two point on Earth with given longitudes and
    latitudes.
    >>> haversine_distance(24.05, 48.08, 24.06, 48.09)
    1.3372365823409342
    >>> haversine_distance(48.08, 24.05, 48.09, 24.06)
    1.5057991000504831
    '''
    lng1, lat1, lng2, lat2 = map(radians, [lng1, lat1, lng2, lat2]) #convert to radians
    dlng = lng2-lng1
    dlat = lat2-lat1
    value = 2*asin(sqrt(sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlng/2)**2))
    #haversine formula
    return value*6371 #6371 is a radius of Earth in km

def distance_films(year:int, lat:float, lng:float, file:str) -> list:
    '''
    Return list of tuples (each is (film, distance_in_km)) of films which were
    released in the given year, distance_in_km is distance from given point.
    '''
    list_of_films = []
    with open (file, 'r') as csv_file :
        csv_reader = csv.reader(csv_file, delimiter=',')
        for line in csv_reader :
            if int(line[1]) == year :
                distance = haversine_distance(float(line[3]), float(line[2]), lng, lat)
                list_of_films.append((line[0], distance, line[2], line[3]))
    return list_of_films

def ten_nearest(list_of_films:list) -> list:
    '''
    Return ten (or less) most close to films to given point.
    '''
    nearest_films = []
    for bottom in range (len(list_of_films) - 1) :
        idx = bottom
        for itr in range (bottom+1, len(list_of_films)) :
            if list_of_films[itr][1] < list_of_films[idx][1] :
                idx = itr
        list_of_films[bottom], list_of_films[idx] = list_of_films[idx],\
             list_of_films[bottom] #sorting by distance
    idx = 10
    if len(list_of_films) < 10 :
        idx = len(list_of_films)
    for itr in range(idx) :
        nearest_films.append((list_of_films[itr][0], list_of_films[itr][2],\
             list_of_films[itr][3]))
    return nearest_films

def generating_map(list_of_films:list, lat:float, lng:float, year:int) :
    '''
    Generates map with given properties.
    '''
    map = folium.Map(location=[lat, lng], zoom_start=1000)
    fg_films = folium.FeatureGroup(name='Films')
    for film in list_of_films :
        fg_films.add_child(folium.Marker(location=[film[1], film[2]],
        popup=film[0], icon=folium.Icon()))
    map.add_child(fg_films)
    fg_pp = folium.FeatureGroup(name="Population")
    fg_pp.add_child(folium.GeoJson(data=open('world.json', 'r',
    encoding='utf-8-sig').read(),
    style_function=lambda x: {'fillColor':'green'
    if x['properties']['POP2005'] < 10000000
    else 'orange' if 10000000 <= x['properties']['POP2005'] < 20000000
    else 'red'}))
    map.add_child(fg_pp)
    map.save('{}_map_films.html'.format(year))
    return '{}_map_films.html'.format(year)
