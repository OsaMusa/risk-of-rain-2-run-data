# Risk of Rain 2 Run Data Parser

## Overview
This project reads the Risk of Rain 2 run history data by parsing the xml files the game saves to the hard drive. The create_db.py script creates a SQLite database in the project directory that will be used to store the run data. The run_db.py script is the primary script of the project. 

With each use the database is updated with all runs that were saved since the last run on record. The database's tables are also exported as CSV files for more usability with analysis tools like Power BI and Tableau.

## Settings File
The settings file is used for storing necessary data that the script will use for completing its tasks. If no settings.txt exists within the project directory, then the script will create one with default values.

The data points in the file are:
1. dir_path
    - The ablsolute path to the directory that stores the run reports.
2. most_recent_run_date
    - The creation date of the most recent run file recorded by the run_db.py script.
3. export_path
    - The absolute path to the directory where the exported tables are held.