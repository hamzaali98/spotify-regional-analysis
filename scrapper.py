import requests
import pandas as pd
from datetime import date, timedelta
import os
from tqdm import tqdm

# Define the base URL
base_url = 'https://charts-spotify-com-service.spotify.com/auth/v0/charts/regional-{country}-weekly/{date}'

# Define the headers with the Authorization token
headers = {
    'Authorization': 'Bearer BQA0bbmaphIT2uVcUgTEqsMvhefxKfIINAkeVdbetKUOg3GpQ-G43ji_6jukcyrYSf_-rCd9iqGs_s218-FLpFGgpJCTbWDiThOS7VZAV--jyeV-269vC_pPwH2IU58cSvINdrppXrbLhuy4MOrJGpV9DXrhry7eTOjs9NFTzczRt-t1oEnaA8-vq7_fO6az03ddBntIPOpsQZlLA41aW9Em',
}

all_possible_countries = [
    # "se",  # Sweden
    # "pk",  # Pakistan
    "fr",  # France
    # "gr",  # Greece
    # "ca",  # Canada
    # "us",  # United States
    # "mx",  # Mexico
    # "cr",  # Costa Rica
    # "ni",  # Nicaragua
    # "ar",  # Argentina
    # "br",  # Brazil
    # "bo",  # Bolivia
    # "cl",  # Chile
    # "pe",  # Peru
    # "at",  # Austria
    # "be",  # Belgium
    # "fr",  # France
    # "de",  # Germany
    # "it",  # Italy
    # "in",  # India
    # "jp",  # Japan
    # "kr",  # South Korea
    # "ae",  # United Arab Emirates
    # "vn",  # Vietnam
    # "eg",  # Egypt
    # "ma",  # Morocco
    # "ng",  # Nigeria
    # "za",  # South Africa
    # "au",  # Australia
    # "nz"   # New Zealand
]

# Create a folder to store CSV files
if not os.path.exists('charts_data_backup'):
    os.makedirs('charts_data_backup')

# Start with today's date and go back 7 days for 52 weeks
start_date = date.today() - timedelta(days=10)

# Create a tqdm progress bar for the number of weeks
for week_number in tqdm(range(5*52), desc="Weeks Progress"):
    end_date = start_date - timedelta(days=7)

    # Loop through each country and fetch data
    for country in tqdm(all_possible_countries, desc="Country Progress", leave=False):
        url = base_url.format(country=country, date=start_date)
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            chart = []
            for entry in response.json()['entries']:
                chart.append({
                    "Artist": ', '.join([artist['name'] for artist in entry['trackMetadata']['artists']]),
                    "TrackName": entry['trackMetadata']['trackName'],
                    "TrackId": entry['trackMetadata']['trackUri']
                })
            df = pd.DataFrame(chart)

            # Define the filename for the CSV based on the country
            csv_filename = os.path.join('charts_data_backup', f'{country}_chart_data.csv')

            if os.path.exists(csv_filename):
                # Append the data to the existing CSV file
                df.to_csv(csv_filename, mode='a', header=False, index=False)
            else:
                # Create a new CSV file and save the data
                df.to_csv(csv_filename, index=False)

        else:
            print(f"Request for {country} on {start_date} failed with status code {response.status_code}")

    # Move to the previous week
    start_date = end_date