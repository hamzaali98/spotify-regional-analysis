import os
import pandas as pd

# Directory where CSV files are stored
data_dir = 'charts_data_backup'

# List all CSV files in the directory
csv_files = [file for file in os.listdir(data_dir) if file.endswith('.csv')]

# Initialize a consolidated DataFrame
consolidated_df = None

# Loop through each CSV file and consolidate the data
for csv_file in csv_files:
    file_path = os.path.join(data_dir, csv_file)
    df = pd.read_csv(file_path)

    consolidated_df = df

    # Calculate the number of times each track name is repeated and save it in a new column
    consolidated_df['TimesRepeated'] = consolidated_df.groupby('TrackName')['TrackName'].transform('count')
    consolidated_df = consolidated_df.drop_duplicates(subset=['TrackName'])

    # Sort the DataFrame by the "TimesRepeated" column in descending order
    consolidated_df = consolidated_df.sort_values(by='TimesRepeated', ascending=False)

    # Save the consolidated data to a new CSV
    consolidated_csv_path = os.path.join(data_dir, csv_file)
    consolidated_df.to_csv(consolidated_csv_path, index=False)

