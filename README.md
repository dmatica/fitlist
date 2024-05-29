# FitList
A series of scripts to merge Apple Music data with Apple Fitness data
![fitlist_demo](https://github.com/dmatica/fitlist/assets/4794041/75f8504f-0721-4c3d-8fb2-04839d4a9273)

## Step 1: Apple Music Merge

Apple does not currently provide a real-time solution for retrieving your music listening history, as the Apple Music API’s “Get Recently Played Tracks” call will only retrieve a maximum of 30 recently played tracks. In order to retrieve your full music listening history, you need to request  a copy of your data with Apple’s Privacy team (https://privacy.apple.com/).

![Apple data request](https://github.com/dmatica/fitlist/assets/4794041/d08b3bd8-f9a6-4302-974b-ac982aeec266)

This request can take a week or so to process, and you should eventually receive an email that provides you with a link to download the data.

![Apple data email](https://github.com/dmatica/fitlist/assets/4794041/2b852feb-86e7-486a-bc15-067b3e6aebcc)

Nested inside this zipped folder, we should find a zipped folder titled ‘Apple_Media_Services.zip’. Inside this folder we’ll find another zipped file ‘Apple Music Activity.zip’. Inside here, we’re primarily interested in the files ‘Apple Music - Play History Daily Tracks.csv’ and ‘Apple Music Play Activity.csv’, as these files will be input for the first step ‘Apple Music Merge.py’. As the ‘Apple Music Play Activity.csv’ file gives track by track information, it only provides a song name for each entry, and does not provide the corresponding artist name.

![Apple music](https://github.com/dmatica/fitlist/assets/4794041/14d3ce5d-cffb-4aca-aa2b-ee5a9daae6c0)

This first script grabs the corresponding ‘Track Description’ field from the ‘Apple Music - Play History Daily Tracks.csv’, which provides an artist and track name. This script splits this file by year to better index the information, and creates a series of files named ‘AppleMusicTrackData_{year}.csv’ for each year. These files have the following columns for use:
- Event End Timestamp
- Event Start Timestamp
- Song Name
- UTC Offset in Seconds
- Track Description


## Step 2: Acquisition of Apple Fitness data

Apple currently does not have a way to export workout information at the granular level. Exporting workouts within the Apple Fitness application will output some basic metrics, but it’s not a lot of data to work with.
﻿<p align="center">
 <img src="https://github.com/dmatica/fitlist/assets/4794041/61cdd95b-0d3a-4050-ba10-f3767f7d67d4">
</p>
First is the Workout Details, which provides us with some general information about the workout. Next is the Heart Rate. This provides us with a chart of the heart rate over the course of the workout. Clicking the ‘Show More’ button provide a little bit more information about your workout performance.
﻿<p align="center">
 <img src="https://github.com/dmatica/fitlist/assets/4794041/4c8f8467-cd13-49ec-8441-e789aef6e99c">
 </p>
The Apple Fitness app also includes an Export button in each workout, but this gives a simple widget-looking table with some basic workout information:
﻿<p align="center">
 <img src="https://github.com/dmatica/fitlist/assets/4794041/6a8beb17-1dfb-4731-8569-d640a627bedf">
 </p>
 In order to get the detailed information from these workouts, I used the app 'Health Auto Export'. This app syncs with my Apple Health, where it is able to output a series of files for each workout, providing granular information.

**Need to add**: [Screenshots of the Health Auto Export app]

This app will export a number of files for each workout:
1. **Active Energy.csv** - This file provides granular information about the active energy burned in kcal for every second of the workout duration.
2. **Heart Rate Recovery.csv** - This file provides granular information for the heart rate (min, max, and average) for each timepoint for 2 minutes post-workout completion. The granularity is less consistent, with timepoints being every few seconds.
3. **Heart Rate.csv** - This file provides granular information for the hear rate (min, max, and average (for each timepoint for the duration of the workout. The granularity is less consistent, with timepoints being every few seconds. 
4. **Resting Energy.csv** - This file provides granular information about the resting energy burned in kcal for every second of the workout duration.
5. **Step Count.csv** - This file provides granular information about the approximated step count for each second of the workout duration.
6. **Walking + Running Distance.csv** - This file provides granular information about the approximated distance traveled in miles for each second of the workout.
	
In the process of testing out exporting the workout files, all of the files for all workouts would export to the same location. Depending on how many workouts were exported, this may result in a high number of files saving to the same location. In these instances, the workout and workout timestamps are appended to the end of the filenames. However, this is not a clean solution at managing this data. The nester.py script is used for this step to create a nested folder structure: year > Month > Date > Workout > workout files.
<p align="center">
<img src="https://github.com/dmatica/fitlist/assets/4794041/d2fe06a1-8b40-4162-a9df-9feca56ede41" width="45%">
&nbsp; &nbsp; &nbsp; &nbsp;
<img src="https://github.com/dmatica/fitlist/assets/4794041/70271630-78be-4531-bfdc-e25829753c8c" width="45%">
</p>
