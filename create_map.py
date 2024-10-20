#!/usr/bin/env python3

from __future__ import annotations

import geopy 
object=geopy.Nominatim(user_agent="Nikki")
location = input("Enter the location ")
h=object.geocode(ation)
import folium 
map = folium.Map(location=[h.latitude,h.longitude], zoom_start=13)
folium.Marker([h.latitude,h.longitude], popup='My Home').add_to(map)
map
