# Step 4: Building the FitList Visualizer with Dash

Now that the Apple Music track information is integrated with the heart rate timepoints in the {Workout_Date_Timestamp}_tracks.csv, we can visualize this information to get a more detailed version of the graphs that are output by the Apple Fitness app. This step uses the Dash python library to start up a Flask server to load in all of the data to generate the graphs.
﻿<p align="center">
 <img src='https://github.com/dmatica/fitlist/assets/4794041/66e2a859-edb4-4250-beef-acc0df5554b9'>
</p>
The first part of this script scans all of the folders in the base directory with the workout folders, and only keeps workout folders that contain the corresponding {Workout_Date_Timestamp}_tracks.csv file. All of these workouts are stored into the dropdown menu. From there, we can select a work out of interest to view the graphs for.
﻿<p align="center">
 <img src='https://github.com/dmatica/fitlist/assets/4794041/591914df-162f-4a4a-8546-47b50bb1bcb1'>
</p>
The top part of this graph is a plot of the heart rate and active energy burned information for the workout. The x-axis is the time, from when the workout started to when it was completed. From my own testing, I found that keeping the y-axes fixed would allow for easier comparison of workouts. The y-axis on the left is the heart rate, ranging from 50 - 200 beats per minute, which corresponds to the colored bubbles. The second y-axis on the right is the active energy burned, ranging from 0 - 20 kcal/minute, and corresponds to the blue line. To give some further granularity in viewing the heart rate trace, the hovertext for each point is set to it's corresponding 'Track Description' value.![image](https://github.com/dmatica/fitlist/assets/4794041/2c49882d-a2fc-4e68-9626-b5bc66c4adb4)
<p align="center">
  <img src='https://github.com/dmatica/fitlist/assets/4794041/6bd1775a-726e-458d-a7a3-d99fdcf7894e'>
</p>
The bottom part of this graph is a table listing the top 5 tracks ranked by average heart rate per song. This table shows the artist and track information, with its corresponding average heart rate.
<p align="center">
<img src="https://github.com/dmatica/fitlist/assets/4794041/73b8be82-d651-4202-bdc5-980b3f7d0757">
</p>
