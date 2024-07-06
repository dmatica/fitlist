import pandas as pd
from datetime import datetime
desired_timezone = 'America/New_York'

def convert_numerical_to_date(numerical_date):
    # Reads in numerical_date value and returns as a datetime object
    date_str = str(numerical_date)
    return datetime.strptime(date_str, "%Y%m%d").date()


def split_dataframe_by_year(df):
    # Extract unique years from the 'date' column
    unique_years = df['Event Start Timestamp'].dt.year.unique()

    # Create a dictionary to store DataFrames for each year
    dfs_by_year = {}

    # Iterate over unique years and filter the DataFrame for each year
    for year in unique_years:
        dfs_by_year[year] = df[df['Event Start Timestamp'].dt.year == year]

    return dfs_by_year, unique_years

# Read music history data
music_history_file = 'Apple Music Play Activity.csv'
music_history_cols = ["Event End Timestamp","Event Start Timestamp","Song Name", "UTC Offset In Seconds"]
df_music_history = pd.read_csv(music_history_file, usecols=music_history_cols, parse_dates=['Event Start Timestamp','Event End Timestamp'])

# Read music history track description data
music_desc_file = 'Apple Music - Play History Daily Tracks.csv'
music_desc_cols = ["Date Played", "Track Description"]
df_music_desc = pd.read_csv(music_desc_file, usecols=music_desc_cols)

# Convert date numbers into datetime.date objects
df_music_desc['Date'] = df_music_desc['Date Played'].apply(convert_numerical_to_date)

# Filter out invalid timestamps (NaT)
x = (df_music_history)
x = x.dropna(subset=['Event End Timestamp', 'Event Start Timestamp']).sort_values('Event Start Timestamp')

# Add in column for 'Track Description' field
x['Track Description'] = ''
count=0
for index, row in x.iterrows():

    #
    count=count+1
    song = str(row['Song Name'])
    date = row['Event Start Timestamp'].date()
    #print(song,date)
    for index2, row2 in df_music_desc.iterrows():
        song_title = str(row2['Track Description'])
        date2 = row2['Date']
        if date==date2 and song in song_title:
            #print(song,date,song_title)
            x.at[index, 'Track Description'] = song_title
#    print(index)

#print(x, x.columns)
x.to_csv('AppleMusicTrackData.csv',encoding='utf-8', index=False)



dfs_by_year, unique_years = split_dataframe_by_year(x)
for year in unique_years:
    print(dfs_by_year[year])
    filename="AppleMusicTrackData_"+str(year)+".csv"
    dfs_by_year[year].to_csv(filename, encoding='utf-8', index=False)
    print("__________-----------")
