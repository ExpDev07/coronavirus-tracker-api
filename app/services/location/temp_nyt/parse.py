import csv
import json


with open('nyt_timeseries.csv', 'r') as file:
    text = file.read()

data = list(csv.DictReader(text.splitlines()))


temp_loc_dict = {}

for row in data:
    county_state = (row['county'], row['state'])
    date = row['date']
    confirmed = row['cases']
    deaths = row['deaths']

    # initialize if not existing
    if county_state not in temp_loc_dict:
        temp_loc_dict[county_state] = {
            'confirmed': [],
            'deaths': []
        }

    # append confirmed object to county_state
    temp_loc_dict[county_state]['confirmed'].append({
        'date': date,
        'number': confirmed
    })
    #append deaths object to county_state
    temp_loc_dict[county_state]['deaths'].append({
        'date': date,
        'number': deaths
    })


print(len(temp_loc_dict.keys()))


print(json.dumps(temp_loc_dict[('Washtenaw', 'Michigan')]))
