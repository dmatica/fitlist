# FitList
A series of scripts to merge Apple Music data with Apple Fitness data
![fitlist_demo](https://github.com/dmatica/fitlist/assets/4794041/75f8504f-0721-4c3d-8fb2-04839d4a9273)

## Step 1: Apple Music Merge

Apple does not currently provide a real-time solution for retrieving your music listening history, as the Apple Music API’s “Get Recently Played Tracks” call will only retrieve a maximum of 30 recently played tracks. In order to retrieve your full music listening history, you need to request  a copy of your data with Apple’s Privacy team (https://privacy.apple.com/).

![image](https://github.com/dmatica/fitlist/assets/4794041/d08b3bd8-f9a6-4302-974b-ac982aeec266)

This request can take a week or so to process, and you should eventually receive an email that provides you with a link to download the data.

![image](https://github.com/dmatica/fitlist/assets/4794041/2b852feb-86e7-486a-bc15-067b3e6aebcc)

Nested inside this zipped folder, we should find a zipped folder titled ‘Apple_Media_Services.zip’. Inside this folder we’ll find another zipped file ‘Apple Music Activity.zip’. Inside here, we’re primarily interested in the files ‘Apple Music - Play History Daily Tracks.csv’ and ‘Apple Music Play Activity.csv’, as these files will be input for the first step ‘Apple Music Merge.py’. As the ‘Apple Music Play Activity.csv’ file gives track by track information, it only provides a song name for each entry, and does not provide the corresponding artist name.

![image](https://github.com/dmatica/fitlist/assets/4794041/14d3ce5d-cffb-4aca-aa2b-ee5a9daae6c0)

This first script grabs the corresponding ‘Track Description’ field from the ‘Apple Music - Play History Daily Tracks.csv’, which provides an artist and track name. This script splits this file by year to better index the information, and creates a series of files named ‘AppleMusicTrackData_{year}.csv’ for each year. These files have the following columns for use:
-Event End Timestamp
-Event Start Timestamp
-Song Name
-UTC Offset in Seconds
-Track Description
