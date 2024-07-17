import seaborn as sns
import os
import pandas as pd
import matplotlib
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from plotly.subplots import make_subplots
from datetime import datetime
import pytz
import re

#root_folder='/Users/davindersandhu/Downloads/Auto Export/2023/July'
root_folder = 'Data'
workout = 'Elliptical'
plt.style.use('default')
desired_timezone = 'America/New_York'
appleMusicDataPath = '/Users/davindersandhu/PycharmProjects/Fitcheck/'

folders=[]
for root, dirs, files in os.walk(root_folder):
    #print(dirs,files)
    for directory in dirs:
        if directory.startswith(workout):
            folder_path = os.path.join(root, directory)
            #print(folder_path)
            folders.append(folder_path)
folders.sort()
print(folders)
# Add track descriptions to appropriate heart rate data
def track_add(df_heart_rate,x):
    for index, row in df_heart_rate.iterrows():
        for index2,row2 in x.iterrows():
            if row2['Event Start Timestamp'] <= row['Date/Time'].tz_localize(desired_timezone) <= row2['Event End Timestamp']:
                df_heart_rate.at[index, 'Track Description'] = str(row2['Track Description'])
    return df_heart_rate

# Load in 'Apple Music track data.csv'
folder_path = appleMusicDataPath  # Update this with the path to your folder
music_history_cols = ["Event End Timestamp", "Event Start Timestamp", "Track Description"]
x = {}
valid_timestamps = {}
for file_name in os.listdir(folder_path):
    if file_name.startswith('AppleMusicTrackData_') and file_name.endswith('.csv'):
        year = file_name.split('_')[1].split('.')[0]
        file_path = os.path.join(folder_path, file_name)
        df = pd.read_csv(file_path, usecols=music_history_cols, parse_dates=['Event Start Timestamp', 'Event End Timestamp'])
        x[year] = df
        valid_timestamps[year] = df.loc[
            (df['Event Start Timestamp'].notna()) &
            (df['Event End Timestamp'].notna())
            ].sort_values('Event Start Timestamp')

#music_history_file = 'Apple Music track data.csv'
#music_history_cols = ["Event End Timestamp","Event Start Timestamp","Track Description"]
#df_music_history = pd.read_csv(music_history_file, usecols=music_history_cols, parse_dates=['Event Start Timestamp','Event End Timestamp'])
#x = (df_music_history)
##print(x)

w_year=0
for folder in folders:
    #GET YEAR OF FOLDER
    if workout.lower() in folder.lower():
        w_year = re.search(r'(\d{4})', folder).group(1)
        print(w_year)



    #Set folder to Exercise folder path (need to make this recursive)
    exercise = os.path.basename(os.path.normpath(folder))
    print(exercise)

    if os.path.exists(folder+'/'+exercise+'_tracks.csv'):
        print(folder+'/'+exercise+'_tracks.csv: File already exists')
        continue


    # Read heart rate data
    heart_rate_file = folder+'/Heart Rate.csv'
    df_heart_rate = pd.read_csv(heart_rate_file, parse_dates=['Date/Time'])
    workout_start = pd.to_datetime(df_heart_rate['Date/Time'].iloc[0]).tz_localize('America/New_York')
    workout_end = pd.to_datetime(df_heart_rate['Date/Time'].iloc[-1]).tz_localize('America/New_York')
    df_heart_rate['Track Description'] = ''

    # Filter out timestamps outside the range of [workout_start, workout_end]
    # print(type(workout_start), type(workout_end))
    # print(valid_timestamps.columns)
    wos = pd.to_datetime(workout_start)
    woe = pd.to_datetime(workout_end)
    #filtered_timestamps = valid_timestamps[w_year].loc[(valid_timestamps[w_year]['Event Start Timestamp'] >= wos) &(valid_timestamps[w_year]['Event Start Timestamp'] <= woe)]
    if w_year in valid_timestamps:
        filtered_timestamps = valid_timestamps[w_year].loc[
            (valid_timestamps[w_year]['Event Start Timestamp'] >= wos) &
            (valid_timestamps[w_year]['Event Start Timestamp'] <= woe)
            ]
    else:
        print(f"Year {w_year} not found in valid_timestamps.")

    # Don't generate plot if no overlapping timestamps
    if len(filtered_timestamps) == 0:
        continue

    df_heart_rate = track_add(df_heart_rate,x[w_year])

    #SAVE OPTION TO EXPORT DF WITH TRACK DESCRIPTIONS
    df_heart_rate.to_csv(folder+'/'+exercise+'_tracks.csv')
