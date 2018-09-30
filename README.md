# Kiosk Shortest Path Challenge Solution

This repo serves as the solution to the 'kiosk shortest path challenge' listed below:


## Problem Statement:
* Write a program that takes the attached list of kiosks and their coordinates as input, and outputs 2 node-disjoint routes for 2 delivery drivers that start and end at our kitchen on Lake and Racine Ave (41.8851024,-87.6618988). These routes should be optimized for the shortest total distance. Feel free to use any technology or language, but the routing code should be yours. Feel free to make other assumptions.

## Deliverables
* Your Code
* README file that describes how to compile and execute the code and any other assumption or design decisions.
* Deadline: 11:59 pm on Sunday, 30th September 2018


## Prerequisites
* Python 3
* Pipenv (to install/manage dependencies)
* Postgres
  * Set DATABASE_URL value in [local.env](../local.env) to the value that corresponds to your local database
* [Google Maps API Key](https://github.com/googlemaps/google-maps-services-python)
  * Set GOOGLE_API_KEY value in [local.env](../local.env) to your Google Maps API Key

## Installation
* Install Python, Postgres and Pipenv
  * Installation instructions at: [Local Database Installation Instructions](docs/database_programming_overview.md)
* Clone/Fork Repo
* Move to directory
* start virtual environment using pipenv
  * need to use ```PIPENV_VENV_IN_PROJECT=true pipenv shell``` to start virtual environment so that you can have the current environment as the parent directory for the 'venv' directory. This is required for alembic to find the project directory.
  * Run ```pipenv install``` to install dependencies from pipfile
* Run ``` alembic upgrade head``` to migrate database schema
* Run ```python populate_db.py ``` to populate the database with the locations from the given CSV.
* Run ```python get_shortest_paths.py``` to generate the solution and print it to the console.


## Solution Breakdown
* Uses one of my graph implementations imported from: [Graph Module](https://github.com/bbcawodu/adt-dstructures-algos/tree/master/adts-dstructures/graphs)
* 