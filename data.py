import csv
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
    return list_of_films

def writing_csv_file (locations:list) :
    '''
    Writes given information in CSV file (film, year, location).
    '''
    with open('locations.csv', 'w') as locations_file :
        locations_writer = csv.writer(locations_file, delimiter=',')
        for line in locations :
            locations_writer.writerow([line[0], line[1], line[2]])



