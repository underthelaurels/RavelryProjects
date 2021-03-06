# RavelryProjects
Small projects using the Ravelry API to improve personal use of Ravelry as well as knitting knowledge.


## Stash Organizer [1.0]
Visualization of Ravelry yarn stash data either as a text file or as pdf charts. Sortable and filterable (not yet implemented). Assumption is that you have a Ravelry account and have your yarn logged in the stash feature.

To use:
1. Download the repository on your personal machine and `cd` into it
2. Request a Basic Auth, personal Ravelry API token at https://www.ravelry.com/pro/developer
3. Create a 'config.json' file using the provided 'config_example.json' file as a guide.
4. Install all needed python packages with `pip install -r requirements.txt`
5. run `python3 runStashOrganizer.py` to get started! You can also use the `--help` or `-h` flags to get a better rundown of the features

Have fun!

Pro Tip: To decrease loading times for multiple runs, output your stash data with the `--dump` or `-d` flags.  

## Scrap Tagger [Not Started]
Adds scrap yarn automatically to a selected scrap project in the queue.  

## Project Data Visualization [Not Started]
Some charts containing fun information about project data visualization  


## Pattern Stitch and Hour Estimator [Not Started]
Estimates the number of stitches in an unmodded project given the size made. Uses this to estimate the number of hours it would take to complete the project given a knitter's stitches per minute. 