# RavelryProjects
Small projects using the Ravelry API to improve personal use of Ravelry as well as knitting knowledge.

<br />

## Stash Organizer [WIP]
Data visualization of your yarn stash. Sortable and filterable (not yet implemented). Assumption is that you have a Ravelry account and have your yarn logged in the stash feature.<p><p>
To use:<p>
1. Download the repository on your personal machine
2. Request a Basic Auth, personal Ravelry API token at https://www.ravelry.com/pro/developer
3. Create a 'config.json' file using the provided 'config_example.json' file as a guide. (Note: the file must be in the same directory as 'stashOrganizer.py')
4. Install all needed python packages with `pip install -r requirements.txt`
5. run `python3 runStashOrg.py` to get started! You can also use the `--help` or `-h` flags to get a better rundown of the features
Have fun!

<br />

## Scrap Tagger [Not Started]
Auto tags stash yarn as scraps if the leftovers from a project are deemed as scrap. Adds scrap yarn automatically to a selected scrap project in the queue.

<br />

## Project Data Visualization [Not Started]
Some charts containing fun information about project data visualization

<br />

## Pattern Stitch and Hour Estimator [Not Started]
Estimates the number of stitches in an unmodded project given the size made. Uses this to estimate the number of hours it would take to complete the project given a knitter's stitches per minute. 