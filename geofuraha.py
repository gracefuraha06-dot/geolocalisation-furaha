import folium
from folium import CircleMarker, PolyLine
import webbrowser

# ---- Coordonnées des lieux ----
lieux = {
    "Université Révérend Kim": (-4.3400, 15.3200),
    "Jardin Botanique": (-4.3200, 15.3100),
    "Palais du Peuple": (-4.3245, 15.3136)
}

# ---- Centre de la carte ----
avg_lat = sum(lat for lat, lon in lieux.values()) / len(lieux)
avg_lon = sum(lon for lat, lon in lieux.values()) / len(lieux)

# ---- Création de la carte ----
m = folium.Map(location=[avg_lat, avg_lon], zoom_start=14, tiles="OpenStreetMap")

# ---- Couleurs pour les marqueurs ----
couleurs = ["blue", "green", "red"]

# ---- Ajout des marqueurs principaux ----
for (nom, (lat, lon)), couleur in zip(lieux.items(), couleurs):
    CircleMarker(
        location=[lat, lon],
        radius=8,
        color=couleur,
        fill=True,
        fill_color=couleur,
        fill_opacity=0.8,
        popup=f"<b>{nom}</b><br>Latitude: {lat}<br>Longitude: {lon}"
    ).add_to(m)

# ---- Fonction pour créer des points intermédiaires ----
def points_intermediaires(start, end, n=10):
    """Créer n points intermédiaires entre deux coordonnées (lat, lon)"""
    lat1, lon1 = start
    lat2, lon2 = end
    points = []
    for i in range(1, n):
        lat = lat1 + (lat2 - lat1) * i / n
        lon = lon1 + (lon2 - lon1) * i / n
        points.append((lat, lon))
    return points

# ---- Tracer le chemin le plus court approximatif en ligne rouge ----
chemin_lieux = ["Université Révérend Kim", "Jardin Botanique", "Palais du Peuple"]
coords_chemin = []

for i in range(len(chemin_lieux)-1):
    start = lieux[chemin_lieux[i]]
    end = lieux[chemin_lieux[i+1]]
    coords_chemin.append(start)
    coords_chemin.extend(points_intermediaires(start, end, n=10))
coords_chemin.append(lieux[chemin_lieux[-1]])

# Ligne rouge du chemin complet
PolyLine(coords_chemin, color="red", weight=4, opacity=0.9).add_to(m)

# ---- Sauvegarde et ouverture automatique ----
fichier = "carte_kinshasa_universite.html"
m.save(fichier)
print(f"Carte générée : {fichier}")
webbrowser.open(fichier)
