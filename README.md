# Python for Data analysis and Machine Learning

## Using Pandas for Data Analysis
## Project Description

For this project, I used public data from the [Inside AirBnB](http://insideairbnb.com) website to perform a complete data analysis and prediction pipeline on housing prices in Paris.

Following the instructions provided, I completed all steps including data cleaning, exploratory data analysis, model building, and evaluation.

---

## Work Summary

### 1. Dataset Exploration (`listings.csv`)

- Displayed the first 5 rows.
- Displayed information about the dataset (number of rows, columns, data types).
- Listed column names.
- Computed basic statistical summaries.

### 2. Cleaning the `listings` Dataset

- Identified and removed duplicate rows.
- Analyzed missing values:
  - Removed columns with too many missing values (>1000).
  - Filled missing `reviews_per_month` with 0.
- Cleaned the `price` column:
  - Removed outliers using IQR filtering.
- Binned `latitude` and `longitude` into categorical groups to improve model generalization.

### 3. Data Analysis

- Calculated the average price per neighborhood.
- Counted the number of available listings per neighborhood (both table and barplot).
- Analyzed the distribution of listings by `room_type` (table and pie chart).
- Visualized:
  - Price vs number of rooms (colored by neighborhood).
  - Spatial distribution of listings (scatter plot of latitude vs longitude).

### 4. Exploration of the `calendar.csv` Dataset

- Loaded and explored the calendar dataset.
- Found the number of available listings for July 14, 2025.
- Calculated the average price for available listings on that date.

### 5. Merging Listings and Calendar Data

- Merged the two datasets on `listing_id`.
- Built two custom functions:
  - To find the average price of a listing over the next 30 days.
  - To list available listings by date and neighborhood.

- Merged with `reviews.csv` to create a function:
  - To retrieve all reviews for a specific listing sorted by date.

### 6. Mapping Listings on OpenStreetMap

- Plotted the geographic distribution of listings on an OpenStreetMap map using Cartopy.
- Created alternative map versions with Google Maps background.


## How to run:
1. Download data from AirBnb site (listings.csv.gz, calendar.csv.gz, reviews.csv.gz)
2. Create your environment:
 ```bash
 python3 -m venv my_env
 ```
3. Activate your environment:
```bash
source my_env/bin/activate
```
4. Install dependencies.
```bash
pip install -r requirements.txt
```
5. Launch main.py file:
 ```bash
 python3 main.py
 ```