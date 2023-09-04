# Risk of Rain 2 Run Data Parser

## Overview
This project reads your Risk of Rain 2 run history by parsing the xml files the game saves to your hard drive. There is a script that is used for creating a SQLite database that will be used to store the run data. With each use the database is updated with your most recent runs.

## Settings File
- The directory path to your run reports. Please replace this with the relavent path on your machine.
- The date of your most recent run. This is updated upon running the parser if there is a new run (according to the date on file).