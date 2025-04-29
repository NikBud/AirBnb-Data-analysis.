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
    # Exercise 1:

    # 1. Display the first 5 rows of the DataFrame.
    print(listings_df.head())

    # 2. Display information about the DataFrame (number of rows, columns, data types, etc.).
    listings_df.info()

    # 3. Display the column names of the DataFrame.
    print(list(listings_df.columns))

    # 4. Display descriptive statistics of the DataFrame (mean, std, min, max, etc.).
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

    # Exercise 2
    # 1. Find and remove duplicate rows from the DataFrame.
    print(listings_df.duplicated().sum())
    listings_df.drop_duplicates(inplace=True)

    # 2. Display the number of missing values per column. Identify and remove columns that are entirely empty.
    # Option #1
    print(listings_df.isnull().sum()[listings_df.isnull().sum() == len(listings_df)])
    # Option #2
    print(listings_df.columns[listings_df.isnull().all()])
    listings_df.dropna(axis=1, how='all', inplace=True)

    # 3. Replace missing values in the 'price' column with the neighborhood mean.
    listings_df['price'] = listings_df.groupby('neighbourhood')['price'].transform(
        lambda x: x.fillna(x.mean())
    )

    # 4. Replace missing values in the 'host_name' column with "unknown".
    listings_df['host_name'] = listings_df['host_name'].fillna("unknown")

    # 5. Check that there are no more missing values.
    print(listings_df.isnull().sum().sum())

    # 6. Check for outliers in numerical columns and remove them.
    for colName in listings_df.select_dtypes(include=[np.number]).columns:
        listings_df = return_vals_in_quartiles(listings_df, colName)


def ex3():
    # 1. What is the average price of accommodations in each neighborhood? Display results as a table.
    # Option 1:
    limited_listings = listings_df[['neighbourhood_cleansed', 'price']]    
    print(limited_listings.groupby('neighbourhood_cleansed').mean())
    # Option 2:
    print(listings_df.groupby('neighbourhood_cleansed')['price'].mean())

    # 2. How many accommodations are available in each neighborhood? Display results as a table and as a bar plot.
    count_by_neigh = listings_df['neighbourhood_cleansed'].value_counts()
    print(count_by_neigh)
    count_by_neigh.plot(kind='bar', title="Number of accommodations per neighborhood")
    plt.xlabel("District")
    plt.ylabel("Number of apartments")
    plt.tight_layout()
    plt.show()
    
    # 3. What is the distribution of accommodations by property type? Display results as a table and as a pie chart.
    prop_type_regrouping = listings_df['property_type'].value_counts()
    print(prop_type_regrouping)
    prop_type_regrouping.plot(kind='pie', autopct='%1.1f%%', title="Distribution of property types")
    plt.show()

    # 4. Using a scatter plot, visualize the relationship between price and number of bedrooms, colored by neighborhood.
    print(listings_df.columns)
    sns.scatterplot(data=listings_df, x='price', y='bedrooms', hue='neighbourhood_cleansed', alpha=0.6)
    plt.title("Correlation between number of bedrooms and rental price")
    plt.tight_layout()
    plt.show()
    
    # 5. Using a scatter plot, display latitude and longitude of the accommodations.
    plt.figure(figsize=(10, 6))
    plt.scatter(listings_df['longitude'], listings_df['latitude'], alpha=0.5, s=5)
    plt.title("Coordinates of accommodations (latitude, longitude)")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.show()


def ex4():
    # 1. Read the calendar.csv.gz file and display the first 5 rows.
    print(calendar_df.head(5))
    
    # 2. Display information about the calendar DataFrame (number of rows, columns, data types, etc.).
    print(calendar_df.info())

    # 3. Display the column names of the calendar DataFrame.
    print(calendar_df.columns)

    # 4. How many accommodations are available in the calendar for July 14, 2025?
    date_filter = calendar_df['date'] == '2025-07-14'
    availability_filter = calendar_df['available'] == 't'
    calendar_grouped_date = calendar_df[date_filter & availability_filter]
    print(f"Number of available accommodations on 2025-07-14 = {calendar_grouped_date['listing_id'].count()}")

    # 5. What is the average price of available accommodations for July 14, 2025?
    print(f"Mean price for accommodations available on 2025-07-14 = {calendar_grouped_date['price'].mean()}")


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
    # 1. Merge the two DataFrames on the column 'listing_id'.
    listings_calendar_merged = pd.merge(calendar_df, listings_df, left_on='listing_id', right_on='id')

    # 2. Display the first 5 rows of the merged DataFrame.
    print(listings_calendar_merged.head(5))

    # 3. Display information about the merged DataFrame (number of rows, columns, data types, etc.).
    print(listings_calendar_merged.info())

    # 4. Write a function that takes a listing name and returns the average price for the next 30 days.
    print(mean_price_for_last_month(listings_calendar_merged, "Stylish Private Suite + Sunny Balcony Paris"))
    
    # 5. Write a function that takes a date and district and returns the list of available accommodations.
    print(appartments_for_date_and_district(listings_calendar_merged, "2025-06-11", "Batignolles-Monceau")[['name', 'date', 'neighbourhood_cleansed']])
    
    # 6. Merge listings and reviews, and write a function to return all comments for a given listing, sorted by date.
    listings_reviews_merged = pd.merge(reviews_df, listings_df, left_on='listing_id', right_on='id')
    print(reviews_for_appartment(listings_reviews_merged, 'Your perfect Paris studio on Île Saint-Louis'))


def print_on_map(appartment_name):
    name_filter = listings_df['name'] == appartment_name
    required_listing = listings_df[name_filter]
    
    tiles = GoogleTiles()

    # Setup figure window
    plt.figure(figsize=(8, 8))
    ax = plt.axes(projection=tiles.crs)

    # Set map boundaries (for Paris)
    ax.set_extent([2.2, 2.5, 48.8, 48.91], crs=ccrs.PlateCarree())

    # Add background tiles
    ax.add_image(tiles, 12)

    # Plot points from DataFrame
    ax.scatter("longitude", "latitude", data=required_listing, s=100, transform=ccrs.PlateCarree(), alpha=0.7, color='red')
    plt.title("Airbnb Paris with Google Tiles")
    plt.show()


def ex6():
    # Find the location for the given accommodation name.
    print_on_map("Your perfect Paris studio on Île Saint-Louis")


ex6()
