from map_generating import generating_map, ten_nearest, distance_films

if __name__ == '__main__' :
    year = int(input('Please enter a year you would like to have a map for: '))
    lat, lng = input('Please enter your location (format: lat,lng): ').split(',')
    lat = float(lat)
    lng = float(lng)
    print('Map is finished. Please look at: ',
    generating_map(ten_nearest(distance_films(year, lat, lng, 'locations.csv')),
    lat, lng, year))