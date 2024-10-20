#!/usr/bin/env python3
from __future__ import annotations
import os
import geopy
import folium
import webbrowser
import json

# Create a geocoder object
geolocator = geopy.Nominatim(user_agent="Job_scraper_2024")

# # Ask the user to input multiple locations separated by commas
# locations = input("Enter multiple locations separated by commas: ").split(',')

home_locations = [
    'Darlingstraat 983  1102MX',
    'Dennenrodepad 15   1102MW'
]


# load json from companies/
# json will look like this:
# {
#     "name": "Vripack Design B.V.",
#     "kvk": "01035286",
#     "website": "https://vripack.com/",
#     "careers_page": null,
#     "address": "Oppenhuizerweg 2, 8606 AS Sneek",
#     "sector": "Architecture"
# }
# empty parts are = null
# generate a map of companies if they have an address that isn't null and add them to the map
# {code}
map = folium.Map(zoom_start=13)
# List to store the coordinates (latitude, longitude) for bounding box
bounds = []

# Loop through all the locations and add them to the map
for location in home_locations:
    location = location.strip()  # Remove extra spaces
    h = geolocator.geocode(location)
    if h:
        # Store the latitude and longitude for each location
        coords = [h.latitude, h.longitude]
        bounds.append(coords)
        
        # Add marker to the map
        folium.Marker(coords, popup=location, icon=folium.Icon(icon='home')).add_to(map)
    else:
        print(f"Location '{location}' not found!")


# Load companies from JSON files in the 'companies' directory
companies_directory = 'companies'
for filename in os.listdir(companies_directory):
    if filename.endswith('.json'):
        with open(os.path.join(companies_directory, filename)) as f:
            company_data = json.load(f)
            address = company_data.get('address')
            if address:
                h = geolocator.geocode(address)
                if h:
                    coords = [h.latitude, h.longitude]
                    bounds.append(coords)
                    
                    # Add marker to the map for the company
                    folium.Marker(coords, popup=f"{company_data['name']} - {company_data.get('website', 'No website')}").add_to(map)

# Fit the map to the bounds of all locations
if bounds:
    map.fit_bounds(bounds)

# Save and display the map
path = './location_map.html'
map.save(path)
webbrowser.open(f'file://{os.path.realpath(path)}')