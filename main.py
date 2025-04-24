import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import cartopy.crs as ccrs
from cartopy.io.img_tiles import GoogleTiles


listings_df = pd.read_csv('data/listings.csv.gz', compression='gzip')
calendar_df = pd.read_csv('data/calendar.csv.gz', compression='gzip', nrows=5000)
reviews_df = pd.read_csv('data/reviews.csv.gz', compression='gzip', nrows=5000)
listings_df['price'] = listings_df['price'].replace('[$,]', '', regex=True).astype(float)
calendar_df['price'] = calendar_df['price'].replace('[$,]', '', regex=True).astype(float)

def ex1():
    # Exercice 1:

    # 1. Affichez les 5 premières lignes du DataFrame.
    print(listings_df.head())

    # 2. Affichez les informations sur le DataFrame (nombre de lignes, nombre de colonnes, types de données, etc.).
    listings_df.info()

    # 3. Affichez les noms des colonnes du DataFrame.
    print(list(listings_df.columns))

    # 4. Affichez les statistiques descriptives du DataFrame (moyenne, écart-type, minimum, maximum, etc.).
    print(listings_df.describe())


def return_vals_in_quartiles(df: pd.DataFrame, columnName):
    q1 = df[columnName].quantile(0.25)
    q3 = df[columnName].quantile(0.75)
    iqr = q3 - q1
    threshold1 = q1 - 1.5 * iqr
    threshold2 = q3 + 1.5 * iqr
    return df[(df[columnName] >= threshold1) & (df[columnName] <= threshold2)]

def ex2():
    global listings_df

    # Exercice 2
    # 1. Trouvez les lignes qui contiennent des doublons. Enlevez les doublons du DataFrame.
    print(listings_df.duplicated().sum())
    listings_df.drop_duplicates(inplace=True)

    # 2. Affichez le nombre de valeurs manquantes dans chaque colonne du DataFrame. Identifier la colonne qui ne contient aucune valeur et la supprimer.
    # Option #1
    print(listings_df.isnull().sum()[listings_df.isnull().sum() == len(listings_df)])
    # Option #2
    print(listings_df.columns[listings_df.isnull().all()])
    listings_df.dropna(axis=1, how='all', inplace=True)

    # 3. Remplacez les valeurs manquantes de la colonne price par la moyenne du quartier.
    listings_df['price'] = listings_df.groupby('neighbourhood')['price'].transform(
        lambda x: x.fillna(x.mean())
    )

    # 4. Remplacez les valeurs manquantes de la colonne host_name par "unkown"
    listings_df['host_name'] = listings_df['host_name'].fillna("unknown")

    # 5. Vérifiez que le dataframe ne contient plus de valeurs manquantes.
    print(listings_df.isnull().sum().sum())

    # 6. Y a-t-il des valeurs aberrantes dans la colonne price ? Si oui, supprimez-les. Faites de même pour toutes les colonnes numériques.
    for colName in listings_df.select_dtypes(include=[np.number]).columns:
        listings_df = return_vals_in_quartiles(listings_df, colName)



def ex3():
    # 1. Quel est le prix moyen des logements dans chaque quartier ? Affichez les résultats sous forme de tableau.
    # Option 1:
    limited_listings = listings_df[['neighbourhood_cleansed', 'price']]    
    print(limited_listings.groupby('neighbourhood_cleansed').mean())
    # Option 2:
    print(listings_df.groupby('neighbourhood_cleansed')['price'].mean())

    # 2. Quel est le nombre de logements disponibles dans chaque quartier ? Affichez les résultats sous forme de tableau. Puis sous forme de graphique (barplot).
    count_by_neigh = listings_df['neighbourhood_cleansed'].value_counts()
    print(count_by_neigh)
    count_by_neigh.plot(kind='bar', title="Nombre de logements par quartier")
    plt.xlabel("District")
    plt.ylabel("Amount of appartments")
    plt.tight_layout()
    plt.show()
    
    # 3. Quelle est la répartition des logements par type de propriété ? Affichez les résultats sous forme de tableau. Puis sous forme de graphique (graphique circulaire).
    prop_type_regrouping = listings_df['property_type'].value_counts()
    print(prop_type_regrouping)
    prop_type_regrouping.plot(kind='pie', autopct='%1.1f%%', title="Amount of different property types in percentage")
    plt.show()

    # 4. A l'aide du plot scatter, visualisez la relation entre le prix et le nombre de chambres. Utilisez une couleur par quartier.
    print(listings_df.columns)
    sns.scatterplot(data=listings_df, x='price', y='bedrooms', hue='neighbourhood_cleansed', alpha=0.6)
    plt.title("Correlation between amount of bedrooms and price for rent")
    plt.tight_layout()
    plt.show()
    
    # 5. A l'aide du plot scatter, dessinez dans un nuage de points la latitude et la longitude des logements.
    plt.figure(figsize=(10, 6))
    plt.scatter(listings_df['longitude'], listings_df['latitude'], alpha=0.5, s=5)
    plt.title("Coords of appartments (latitude, longitude)")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.show()



def ex4():
    # 1. Lisez le fichier calendar.csv.gz et affichez les 5 premières lignes du DataFrame.
    print(calendar_df.head(5))
    
    # 2. Affichez les informations sur le DataFrame (nombre de lignes, nombre de colonnes, types de données, etc.).
    print(calendar_df.info())

    # 3. Affichez les noms des colonnes du DataFrame.
    print(calendar_df.columns)

    # 4. Combien y a-t-il de logements disponibles dans le calendrier pour le 14 juillet 2025 ?
    date_filter = calendar_df['date'] == '2025-07-14'
    availability_filter = calendar_df['available'] == 't'
    calendar_grouped_date = calendar_df[date_filter & availability_filter]
    print(f"Amount of appartments available 2025-07-14 = {calendar_grouped_date['listing_id'].count()}")

    # 5. Quel est le prix moyen des logements disponibles pour le 14 juillet 2025 ?
    print(f"Mean price for appartments available 2025-07-14 = {calendar_grouped_date['price'].mean()}")



def mean_price_for_last_month(merged_df, appartment_name):
    today = datetime.today().date()
    today_plus_month = today + timedelta(30)

    fluent_date = pd.to_datetime(merged_df['date']).dt.date
    date_filter = (fluent_date >= today) & (fluent_date <= today_plus_month)
    app_name_filter = merged_df['name'] == appartment_name
    availability_filter = merged_df['available'] == 't'

    return merged_df[date_filter & app_name_filter & availability_filter]['price_x'].mean()

def appartments_for_date_and_district(merged_df: pd.DataFrame, date_str: str, district: str):
    date = pd.to_datetime(date_str).date()
    district_filter = merged_df['neighbourhood_cleansed'] == district
    date_filter = pd.to_datetime(merged_df['date']).dt.date == date
    availability_filter = merged_df['available'] == 't'

    return merged_df[district_filter & date_filter & availability_filter]

def reviews_for_appartment(merged_df: pd.DataFrame, appartment_name: str) -> pd.DataFrame:
    name_filter = merged_df['name'] == appartment_name
    sorted = merged_df[name_filter][['name', 'date','comments']].sort_values(by='date')
    return sorted


def ex5():
    # 1. Fusionnez les deux DataFrames sur la colonne listing_id.
    listings_calendar_merged = pd.merge(calendar_df, listings_df, left_on='listing_id', right_on='id')

    # 2. Affichez les 5 premières lignes du DataFrame fusionné.
    print(listings_calendar_merged.head(5))

    # 3. Affichez les informations sur le DataFrame fusionné (nombre de lignes, nombre de colonnes, types de données, etc.).
    print(listings_calendar_merged.info())

    # 4. Écrire une fonction qui prend en entrée un nom de logement et qui retourne le prix moyen de ce logement pour les 30 prochains jours.
    print(mean_price_for_last_month(listings_calendar_merged, "Stylish Private Suite + Sunny Balcony Paris"))
    
    # 5. Écrire une fonction qui prend en entrée une date et un quartier et qui retourne la liste des logements disponibles dans ce quartier pour cette date.    
    print(appartments_for_date_and_district(listings_calendar_merged, "2025-06-11", "Batignolles-Monceau")[['name', 'date', 'neighbourhood_cleansed']])
    
    # 6. Grâce à une fusion entre listings et reviews, écrire une fonction qui prend en entrée un nom de logement et qui retourne la liste des commentaires pour ce logement, triée par date.
    listings_reviews_merged = pd.merge(reviews_df, listings_df, left_on='listing_id', right_on='id')
    print(reviews_for_appartment(listings_reviews_merged, 'Your perfect Paris studio on Île Saint-Louis'))



def print_on_map(appartment_name):
    name_filter = listings_df['name'] == appartment_name
    required_listing = listings_df[name_filter]
    
    tiles = GoogleTiles()

    # Figure window setup
    plt.figure(figsize=(8, 8))
    ax = plt.axes(projection=tiles.crs)

    # Set map bordures (for Paris)
    ax.set_extent([2.2, 2.5, 48.8, 48.91], crs=ccrs.PlateCarree())

    # Add background for our map
    ax.add_image(tiles, 12)

    # Print points from DataFrame
    ax.scatter("longitude", "latitude", data=required_listing, s=100, transform=ccrs.PlateCarree(), alpha=0.7, color='red')
    plt.title("Airbnb Paris with Google Tiles")
    plt.show()


def ex6():
    # Find location for appartment with provided name.
    print_on_map("Your perfect Paris studio on Île Saint-Louis")


ex6()



