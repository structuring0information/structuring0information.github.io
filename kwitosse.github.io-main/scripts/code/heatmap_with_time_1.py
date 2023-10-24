import folium
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from folium.plugins import TimestampedGeoJson
import numpy as np

# Daten laden
df = pd.read_csv('scripts/data/ukr-civharm-2023-05-25.csv')

# Extrahiere den Angriffstyp aus der 'associations'-Spalte
df['attack_type'] = df['associations'].str.split(',').str[-1].str.split('=').str[-1]

# Erstelle eine Liste aller einzigartigen Angriffstypen
attack_types = df['attack_type'].unique().tolist()

# Erstelle eine Farbpalette mit so vielen Farben wie es Angriffstypen gibt
colors = plt.cm.viridis(np.linspace(0, 1, len(attack_types)))

# Erstelle ein Wörterbuch, das jedem Angriffstyp eine Farbe zuordnet
color_dict = {attack_type: mcolors.rgb2hex(color) for attack_type, color in zip(attack_types, colors)}

# Konvertiere DataFrame zu GeoJSON
features = df.apply(
    lambda row: {
        'type': 'Feature',
        'geometry': {
            'type':'Point', 
            'coordinates':[row['longitude'],row['latitude']]
        },
        'properties': {
            'time': row['date'].__str__(),
            'style': {'color' : color_dict[row['attack_type']]},
            'icon': 'circle',
            'iconstyle':{
                'fillColor': color_dict[row['attack_type']],
                'fillOpacity': 0.6,
                'stroke': 'true',
                'radius': 5
            }
        }
    },
    axis=1).tolist()

# Wir legen den "type" auf "FeatureCollection" und fügen "features" hinzu
geojson = {'type':'FeatureCollection', 'features':features}

# Erstelle eine Basiskarte
m = folium.Map(location=[48.3794, 31.1656], zoom_start=5)

# Füge GeoJson der Ukraine hinzu
folium.GeoJson('scripts/data/geoBoundaries-UKR-ADM0_simplified.geojson', name='ukraine').add_to(m)

# Füge die zeitgestempelte GeoJSON-Schicht hinzu
TimestampedGeoJson(geojson, period='P1D', add_last_point=True).add_to(m)

m

m.save('scripts/html/heatmap_with_time_1.html')
