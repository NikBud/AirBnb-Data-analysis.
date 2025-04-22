[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/0DvX22Lj)
[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-2e0aaae1b6195c2367325f4f02e2d04e9abb55f0b24a779b69b11b9e10269abc.svg)](https://classroom.github.com/online_ide?assignment_repo_id=19275421&assignment_repo_type=AssignmentRepo)
# Python pour le Machine Learning

## TD3 : utilisation de Pandas

### Leo Donati - 2025
### ⏳ Durée : 2 heures
### 🛠️ Pré-requis 

- Python 3.x installé sur votre machine
- Bibliothèque NumPy installée (`pip install numpy`)
- Bibliothèque Matplotlib installée (`pip install matplotlib`)
- Bibliothèque Pandas installée (`pip install pandas`)

### 🚀 Instructions:

On va utiliser les données publiques disponibles sur le site de AirBnb pour faire des analyses de données. AIrBnB publie régulièrement des données sur les locations de logements dans différentes villes du monde sur le site [Inside AirBnb](http://insideairbnb.com). 

- Dans l'onglet ``Explore the data`` on a une interface web qui permet de visualiser les données sur une carte. Voir par exemple [AirBnb Paris](https://insideairbnb.com/fr/paris/).
- Dans l'onglet ``Get the data`` les données sont disponibles sous forme de fichiers CSV et contiennent des informations sur les logements, les prix, les évaluations, etc. Les données pour Paris sont disponibles 
    - [listings](https://data.insideairbnb.com/france/ile-de-france/paris/2024-12-06/data/listings.csv.gz) contient des informations sur les logements, y compris le prix, le nombre de chambres, la capacité d'accueil, etc.
    - [calendar](https://data.insideairbnb.com/france/ile-de-france/paris/2024-12-06/data/calendar.csv.gz) contient des informations sur la disponibilité des logements, y compris les dates de disponibilité et les prix.
    - [reviews](https://data.insideairbnb.com/france/ile-de-france/paris/2024-12-06/data/reviews.csv.gz) contient des informations sur les évaluations des logements, y compris les commentaires et les notes.

Téléchargez les trois fichiers CSV compressés et placez-les dans un répertoire ``data`` de votre projet. 

Pour lire les fichiers CSV, nous allons utiliser la bibliothèque Pandas. Voici comment lire un fichier CSV avec Pandas :

```python
import pandas as pd
# Lire le fichier CSV
df = pd.read_csv('data/listings.csv.gz', compression='gzip')
# Afficher les premières lignes du DataFrame
print(df.head())
```

### 1. Exploration du dataset listings

 1. Affichez les 5 premières lignes du DataFrame.
 2. Affichez les informations sur le DataFrame (nombre de lignes, nombre de colonnes, types de données, etc.).
 3. Affichez les noms des colonnes du DataFrame.
 4. Affichez les statistiques descriptives du DataFrame (moyenne, écart-type, minimum, maximum, etc.).

### 2. Nettoyage du dataset ``listings``

 1. Trouvez les lignes qui contiennent des doublons. Enlevez les doublons du DataFrame.
 2. Affichez le nombre de valeurs manquantes dans chaque colonne du DataFrame. Identifier la colonne qui ne contient aucune valeur et la supprimer. Supprimer aussi les colonnes qui ont plus de 1000 cellules vides.
 3. Remplacez les valeurs manquantes de la colonne `price` par la moyenne du quartier.
 4. Remplacez les valeurs manquantes de la colonne `host_name` par "unkown"
 5. Vérifiez que le dataframe ne contient plus de valeurs manquantes.
 6. Y a-t-il des valeurs aberrantes dans la colonne `price` ? Si oui, supprimez-les. Faites de même pour toutes les colonnes numériques.

### 3. Analyse des données

1. Quel est le prix moyen des logements dans chaque quartier ? Affichez les résultats sous forme de tableau.
2. Quel est le nombre de logements disponibles dans chaque quartier ? Affichez les résultats sous forme de tableau. Puis sous forme de graphique (barplot).
3. Quelle est la répartition des logements par type de propriété ? Affichez les résultats sous forme de tableau. Puis sous forme de graphique (graphique circulaire).
4. A l'aide du plot scatter, visualisez la relation entre le prix et le nombre de chambres. Utilisez une couleur par quartier.
5. A l'aide du plot scatter, dessinez dans un nuage de points la latitude et la longitude des logements.

### 4. Exploration du dataset calendar

Nous allons maintenant explorer le dataset `calendar.csv.gz` qui contient des informations sur la disponibilité des logements. Pour chacun des 365 jours allant du 7 décembre 2024 au 16 décembre 2025 et pour chaque logement il y a une ligne qui contient la statut et le prix du logement si le logement est loué.

1. Lisez le fichier `calendar.csv.gz` et affichez les 5 premières lignes du DataFrame.
2. Affichez les informations sur le DataFrame (nombre de lignes, nombre de colonnes, types de données, etc.).
3. Affichez les noms des colonnes du DataFrame.
4. Combien y a-t-il de logements disponibles dans le calendrier pour le 14 juillet 2025 ? 
5. Quel est le prix moyen des logements disponibles pour le 14 juillet 2025 ? 


### 5. Exemple de fusion de données

Nous allons maintenant fusionner les données de deux fichiers CSV : `calendar.csv.gz` et `listings.csv.gz`. 

1. Fusionnez les deux DataFrames sur la colonne `listing_id`.
2. Affichez les 5 premières lignes du DataFrame fusionné.
3. Affichez les informations sur le DataFrame fusionné (nombre de lignes, nombre de colonnes, types de données, etc.).
4. Écrire une fonction qui prend en entrée un nom de logement et qui retourne le prix moyen de ce logement pour les 30 prochains jours.
5. Écrire une fonction qui prend en entrée une date et un quartier et qui retourne la liste des logements disponibles dans ce quartier pour cette date.
6. Grâce à une fusion entre listings et reviews, écrire une fonction qui prend en entrée un `nom` de logement et qui retourne la liste des commentaires pour ce logement, triée par date.

### 6. Visualisation des données sur une carte

Nous allons maintenant visualiser les données sur une carte OpenStreetMap avec la bibliothèque Cartopy. Plus d'informations sur la bibliothèque Cartopy sont disponibles [ici](https://scitools.org.uk/cartopy/docs/latest/).

```python
import cartopy.crs as ccrs
from cartopy.io.img_tiles import OSM ## OSM = OpenStreetMap
import matplotlib.pyplot as plt

tiles = OSM()
plt.figure(figsize=(10, 10))
ax = plt.axes(projection=tiles.crs)
ax.set_extent([2.2, 2.5, 48.8, 48.91], ccrs.PlateCarree())
ax.add_image(tiles, 12)

# On suppose que new_listing est le DataFrame nettoyé.
ax.scatter("longitude", "latitude", data=new_listing, s=1, transform=ccrs.PlateCarree(), alpha=0.1)
```

![AirBnb Paris avec OpenStreetMap](../../cours/images/paris.png)

On peut faire la même chose avec une carte google maps : au lieu de `OSM` on utilise `GoogleTiles`.

![AirBnb Paris avec GoogleMaps](../../cours/images/paris_gmap.png)

