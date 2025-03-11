# -*- coding: utf-8 -*-
"""
Created on Thu Jun 20 02:11:19 2024

@author: varunsharma
"""

# from geopy.distance import geodesic
import math
from collections import defaultdict
from datetime import datetime
import pandas as pd
from geopy.distance import geodesic

#%%
# Haversine formula
def haversine(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))
    r = 6371  # Radius of Earth in kilometers
    return c * r

# Vincenty's formula using geopy
def vincenty(lat1, lon1, lat2, lon2):
    coords_1 = (lat1, lon1)
    coords_2 = (lat2, lon2)
    return geodesic(coords_1, coords_2).kilometers

def filter_data_by_date(data, date):
    return data[data['created_at'].dt.date == date]

def calculate_distance(data, method):
    total_distance = 0.0
    if len(data) < 2:
        return total_distance
    for i in range(1, len(data)):
        coords_1 = (data.iloc[i-1]['latitude'], data.iloc[i-1]['longitude'])
        coords_2 = (data.iloc[i]['latitude'], data.iloc[i]['longitude'])
        total_distance += method(*coords_1, *coords_2)
    return total_distance
#%%
def main(date):
    # Convert the date from string to datetime object
    date = datetime.strptime(date, '%Y-%m-%d').date()

    # Read the CSV file containing the latt-long tracked data from an andrid app
    # lattlong were captured for all user at every 15 minutes for working hours
    data = pd.read_csv(r'C:\Users\varun\androidapp_location_data\fr_route2.csv') 

    # Convert the 'created_at' column to datetime
    data['created_at'] = pd.to_datetime(data['created_at'])

    # Filter the data based on the given date
    filtered_data = filter_data_by_date(data, date)

    distances_by_user_haversine = defaultdict(float)
    distances_by_user_vincenty = defaultdict(float)
    data_by_user = defaultdict(list)

    for _, record in filtered_data.iterrows():
        data_by_user[record['user_id']].append(record)

    for user_id, records in data_by_user.items():
        distances_by_user_haversine[user_id] = calculate_distance(pd.DataFrame(records), haversine)
        distances_by_user_vincenty[user_id] = calculate_distance(pd.DataFrame(records), vincenty)

    # Prepare the result in tabular form
    result = {
        'user_id': [],
        'distance_haversine_km': [],
        'distance_vincenty_km': []
    }

    for user_id in distances_by_user_haversine.keys():
        result['user_id'].append(user_id)
        result['distance_haversine_km'].append(distances_by_user_haversine[user_id])
        result['distance_vincenty_km'].append(distances_by_user_vincenty[user_id])

    result_df = pd.DataFrame(result)
    return result_df


#%%
# Example usage
date = '2024-06-20' #give the date for which route distance has to be calculated
result_df = main(date)
print(result_df)
