

import pandas as pd
import folium
import json
from folium.plugins import TimestampedGeoJson
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np

# CSV-Datei einlesen
data = pd.read_csv("scripts/data/processed_data.csv")

# Transformiere 'date' Spalte in datetime-Format
data['date'] = pd.to_datetime(data['date'])

# Extrahiere den Angriffstyp aus der 'associations'-Spalte
data['attack_type'] = data['associations'].str.split('Weapon System=').str[-1]

# Lade die GeoJSON-Daten der Ukraine
with open('scripts/data/geoBoundaries-UKR-ADM1_simplified.geojson') as f:
    ukraine_geojson = json.load(f)

# Erstelle eine Karte
m = folium.Map(location=[48.3794, 31.1656], zoom_start=5)

# Erstelle eine Liste aller einzigartigen Angriffstypen
attack_types = data['attack_type'].unique().tolist()

# Erstelle eine Farbpalette mit so vielen Farben wie es Angriffstypen gibt
colors = plt.cm.viridis(np.linspace(0, 1, len(attack_types)))

# Erstelle ein Wörterbuch, das jedem Angriffstyp eine Farbe zuordnet
color_dict = {attack_type: mcolors.rgb2hex(color) for attack_type, color in zip(attack_types, colors)}


# Erstelle eine Markierung für jeden Punkt in jedem Angriffstyp
for attack_type in attack_types:
    data_attack_type = data[data['attack_type'] == attack_type]
    
    # Erstelle eine neue Schicht für diesen Angriffstyp
    feature_group = folium.FeatureGroup(name=attack_type)
    
    for _, row in data_attack_type.iterrows():
        folium.CircleMarker(
            location=[row['latitude'], row['longitude']],
            radius=5,
            popup=row['description'],
            fill=True,
            color=color_dict[row['attack_type']],
            fill_color=color_dict[row['attack_type']],
            fill_opacity=0.6
        ).add_to(feature_group)
    
    feature_group.add_to(m)

# Füge GeoJson der Ukraine hinzu
folium.GeoJson(ukraine_geojson, name='ukraine').add_to(m)

# Füge eine Schichtkontrolle hinzu, damit Benutzer zwischen den Schichten wechseln können
folium.LayerControl().add_to(m)

m

# Speichern Sie die Karte in einer HTML-Datei
m.save('scripts/html/heatmap_points.html')
