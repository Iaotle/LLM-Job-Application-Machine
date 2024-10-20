#!/usr/bin/env python3
from __future__ import annotations
import os
import geopy
import folium
import webbrowser

# Create a geocoder object
geolocator = geopy.Nominatim(user_agent="Job_scraper_2024")

# # Ask the user to input multiple locations separated by commas
# locations = input("Enter multiple locations separated by commas: ").split(',')

locations = [
    'Darlingstraat 983  1102MX',
    'Dennenrodepad 15   1102MW'
]
    
map = folium.Map(zoom_start=13)
# List to store the coordinates (latitude, longitude) for bounding box
bounds = []

# Loop through all the locations and add them to the map
for location in locations:
    location = location.strip()  # Remove extra spaces
    h = geolocator.geocode(location)
    if h:
        # Store the latitude and longitude for each location
        coords = [h.latitude, h.longitude]
        bounds.append(coords)
        
        # Add marker to the map
        folium.Marker(coords, popup=location).add_to(map)
    else:
        print(f"Location '{location}' not found!")

# Fit the map to the bounds of all locations
if bounds:
    map.fit_bounds(bounds)

# Save and display the map
path = './location_map.html'
map.save(path)
webbrowser.open(f'file://{os.path.realpath(path)}')