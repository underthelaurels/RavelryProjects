# RavelryProjects
Small projects using the Ravelry API to improve personal use of Ravelry as well as knitting knowledge.
Using python 3

Current dependencies - python requests. ("python3 -m pip install requests" to install!)

<br />

## Stash Organizer [WIP]
Data visualization of your yarn stash. Sortable and filterable.
Currently collects data from Ravelry and parses and prints out basic stash information. 
You can also dump the stash information as stash_dump.json, weight_dump.json, and color_dump.json by changing "org = StashOrganizer(0)" in stashOrganizer.py to "org = StashOrganizer(1)". 
I have added an example config file if you would like to try it out on your on your own machine! You can request Ravelry api tokens at https://www.ravelry.com/pro/developer

<br />

## Scrap Tagger [WIP]
Auto tags stash yarn as scraps if the leftovers from a project are deemed as scrap. Adds scrap yarn automatically to a selected scrap project in the queue.

<br />

## Project Data Visualization [WIP]
Some charts containing fun information about project data visualization

<br />

## Pattern Stitch and Hour Estimator [WIP]
Estimates the number of stitches in an unmodded project given the size made. Uses this to estimate the number of hours it would take to complete the project given a knitter's stitches per minute. 