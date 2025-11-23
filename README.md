# FitList
## Introducing FitList v1


https://github.com/user-attachments/assets/948b61d1-38d1-466c-9b26-81252b17d0d8


To improve on the visual experience of FitList, this next iteration has been rebuilt in SQL and Superset. The output files as previously described in Step 3 are generated as before, but a subsequent step has been taken to combine this data into a single workouts.db file, with the following tables and schemas:

Table: workouts
| Column | Type | Description|
|:----|:-----|:------|
| id | INTEGER | Workout number |
| date | DATE | Date of workout |
| workout_type | TEXT | Workout type |
| notes | TEXT | Optional notes |

Table: heart_rate_points
| Column | Type | Description|
|:-------|:------|:------|
| id | INTEGER | Unique identifier |
| workout_id | INTEGER | Foreign key to workouts(id) |
| timestamp | DATETIME | Timestamp of heart rate |
| heart_rate | NUMERIC | Average measured heart rate |
| track_name | TEXT | track_description field |
| artist | TEXT | Optional if available/parsed |

Once imported into Superset, different chart types can be generated, and combined into a dashboard view that allows for navigating different workouts, and seeing aggregate metrics across all workouts. In the example dashboard above, the top layer contains the drop down menu to switch between workouts. Changing workouts here will update the two top charts in the dashboard (Heart Rate and Top Workout Tracks), however the bottom charts (Most Played Tracks - All time, Average heart rate per workout, and Workout minutes per month) remain unchanged.


## v0 Introduction
A series of scripts to merge Apple Music data with Apple Fitness data
![fitlistdemo](https://github.com/dmatica/fitlist/assets/4794041/eb9c6723-7656-4195-9cf9-6ed0bfc33667)

[Step 1: Apple Music Merge](/Step1/)
<br>
[Step 2: Apple Fitness Data Acquisition](/Step2/)
<br>
[Step 3: Merging Apple Fitness and Apple Music data](/Step3/)
<br>
[Step 4: Building the FitList Visualizer with Dash](/Step4/)

Across the different products and services within the Apple ecosystem, it can sometimes be shocking to see the lack of integration between products. One such gap I’ve noticed in my everyday life is the seeming lack of communication between Apple Music and Apple Fitness. As someone who is interested in finding patterns in my music listening behavior (https://github.com/dmatica/lastify), I was curious to see if I could merge my music listening history with the heart rate information from the workouts I record on my watch while at the gym, with the goal of identifying a trend between the type of music I listen to and how effective my workouts are.

## How Apple Fitness works
Currently, Apple Fitness workouts are initiated, paused, resumed, and ended from within Apple  Watch’s Workouts app. Users with an Apple Fitness+ subscription will initially be prompted with a promoted audio-based fitness workout, but can otherwise select from a growing list of workouts. Upon selecting the workout, a three-second countdown will start and the workout commences.

After the workout completes, you can review the workout will be available in the Fitness app on the phone. For each workout, the Fitness app will provide some workout details and a heart rate chart. If performing an outdoor workout, a map will show the route of the workout.

Tapping into the heart rate will give a more detailed, color-coded chart, with a breakdown of how much time of the workout was in each heart rate zone. 

However, this is the extent to which the data is available, natively. Apple currently does not provide a convenient way to export your workout data, such as heart rate or caloric activity. Instead, a third-party app is required to export workout data into CSV files with a more expansive look at the data. For this experiment, I was utilizing Health Auto Export ( https://apps.apple.com/us/app/health-auto-export-json-csv/id1115567069). This app requires a paid subscription to export the data (I used the $0.99 / month Premium option). The data exported breaks down each workout into multiple files: a Walking file that contains the number of steps in the workout, an Active Energy file with the active calories expended per minute of the workout, a Basal Energy file with the basal calories expended during the workout, a summary file with the basic workout details, and a Heart Rate file that contains the min, max, and average heart rate per minute of the workout.

## Getting Started
For the scope of this project, I was studying the role that music plays on my elliptical workouts at the gym. I set some constraints in order to keep this as controlled as possible; each workout was using the same machine (Precor AMT 100I). Each exercise used the manual program, with the level at the maximum setting of 20. And to cancel out the music from the gym’s sound system, these workouts were using noise cancelling headphones. During the workouts, I was mostly listening to Apple Music playlists, although  After performing the workouts, the next step becomes acquisition of the data.

Apple does not currently provide a real-time solution for retrieving your music listening history, as the Apple Music API’s “Get Recently Played Tracks” call will only retrieve a maximum of 30 recently played tracks. In order to retrieve your full music listening history, you need to request  a copy of your data with Apple’s Privacy team (https://privacy.apple.com/).

This request takes approximately one week. Afterwards you receive an email with a link to download the data. Once we have both the Apple Fitness data exported from Health Auto Export and the Apple Music data, we are able to proceed with the four steps listed at the top.
