import csv
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from geopy.exc import GeocoderUnavailable

geolocator = Nominatim(user_agent='smth')
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

def reading_data(file:str) -> list:
    '''
    Return list of tuples (film, year, location) from file location.list.
    '''
    idx = 0
    list_of_films = []
    with open (file, 'r', encoding='utf-8', errors='ignore') as file_locations :
        for line in file_locations :
            idx += 1
            if idx > 14 : #cut first lines of file
                line = line.strip().split('\t')
                line = list(filter(lambda a: a != '', line))
                if len(line) > 1 :
                    location = line[1]
                    film = line[0].split('(')[0].strip()
                    year = line[0].split('(')[1][:4]
                    if year.isdigit():
                        list_of_films.append((film, int(year), location))
    return list(set(list_of_films))

def writing_csv_file (locations:list) :
    '''
    Writes given information in CSV file (film, year, location, latitude, longitude).
    '''
    start_idx = 10000 #there are a lot of data so I will go only with these films
    end_idx = 15000
    idx = 0
    with open('locations1.csv', 'w') as locations_file :
        locations_writer = csv.writer(locations_file, delimiter=',')
        for line in locations :
            idx += 1
            if start_idx < idx and idx < end_idx :
                try :
                    location = geolocator.geocode(line[2])
                    if location :
                        locations_writer.writerow([line[0], line[1],\
                        location.latitude, location.longitude])
                except GeocoderUnavailable :
                    pass



