import os
import pandas as pd
import spotipy
from tqdm import tqdm

# Set your Spotify app credentials and scopes
client_id = 'b9e0df31f4a24a06bceeac33938762a0'
client_secret = '0e72223687784126ba983bd87a3d9537'

# Initialize Spotify client
client_credentials_manager = spotipy.oauth2.SpotifyClientCredentials(client_id, client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Directory where CSV files are stored
data_dir = 'charts_data'

# List all CSV files in the directory
csv_files = [file for file in os.listdir(data_dir) if file.endswith('.csv')]

# Define the audio feature columns
track_feature_columns = ['release_date']

audio_feature_columns = [
    'acousticness',
    'danceability',
    'energy',
    'instrumentalness',
    'key',
    'liveness',
    'loudness',
    'mode',
    'speechiness',
    'tempo',
    'valence'
]

for csv_file in csv_files:
    file_path = os.path.join(data_dir, csv_file)
    print(csv_file)
    df = pd.read_csv(file_path)
    for col in track_feature_columns:
        df[col] = None
    for col in audio_feature_columns:
        df[col] = None

    # Create a tqdm progress bar
    with tqdm(total=len(df)) as pbar:
        for i, row in df.iterrows():
            track_id = row['TrackId']

            # Check if any track feature or audio feature column already has a value
            if all(pd.isna(df.at[i, col]) for col in track_feature_columns + audio_feature_columns):
                # Get track features
                track_info = sp.track(track_id)
                if track_info and len(track_info) > 0:
                    track_info = track_info['album']
                    for col in track_feature_columns:
                        df.at[i, col] = track_info[col]

                # Get audio features
                audio_features = sp.audio_features(track_id)
                if audio_features and len(audio_features) > 0:
                    audio_features = audio_features[0]
                    for col in audio_feature_columns:
                        df.at[i, col] = audio_features[col]

                # Save the updated DataFrame to the same CSV file
                df.to_csv(file_path, index=False)
            pbar.update(1)  # Update the progress bar

# Display a completion message
print("Audio and track feature extraction completed.")
