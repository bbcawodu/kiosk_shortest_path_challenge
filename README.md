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
* Run ```python populate_db.py ``` to populate the database with the locations from the given CSV and calculated driving distances from the Google Maps API.
* Run ```python get_shortest_paths.py``` to generate the solution and print it to the console.


## Solution:
  * Path 1 is: Farmers Fridge Kitchen, University of Illinois at Chicago - Student Center West, University of Illinois at Chicago - Behavioral Sciences, 7-Eleven @ Jackson and Desplaines, 525 W Monroe, CME Center, General Growth Properties HQ (Employees Only), Merchandise Mart, CVS @ 344 Hubbard, 7-Eleven @ Kingsbury and Ontario , Medical College of Wisconsin, 600 W Chicago, REI Building , DePaul University - Schmitt Academic Center, DeVry Chicago Campus (Students/Staff Only), US Foods (Employees Only), Skokie Hospital / Northshore , Allstate HQ (Tenants Only), Walgreens Corporate Office (Employees Only), Chase Tower, 100 E Wisconsin, Schlitz Park Rivercenter, University of Wisconsin-Milwaukee EMS Building, 100 E Wisconsin, Allstate HQ (Tenants Only), Schaumburg Towers
  * Path 2 is: Farmers Fridge Kitchen, Feinberg Pavilion - Northwestern Medicine, Illinois Center, CVS @ 137 State, 200 W Jackson (Tenants Only), Epic Burger West Loop, University of Illinois at Chicago - Richard J Daley Library (Students/Staff Only), University of Illinois at Chicago - College of Medicine , West Suburban Medical Center, MacNeal Hospital, Loyola Medical Center, DeVry Addison (Students/Staff Only), Good Shepherd Hospital, American Airlines Lounge (Employees Only), O'Hare 3H Left, O'Hare Terminal 2 - Gate F6, Peggy Notebaert Nature Museum, North Park University, Prentice Women`s Hospital - Northwestern Medicine, CNA Center (Employees Only), 311 S Wacker (Tenants Only), MillerCoors HQ, Chicago Midway Airport - Ticketing Employee Lounge, Chicago Midway Airport - Southwest Employee Lounge, Good Samaritan Hospital, Moraine Valley Community College: Police Academy- Building B

## Solution Breakdown
* Uses one of my graph implementations imported from: [Graph Module](https://github.com/bbcawodu/adt-dstructures-algos/tree/master/adts-dstructures/graphs)
* Uses [Google Maps API Key](https://github.com/googlemaps/google-maps-services-python) to get shortest driving distances between kiosks and add them to db in order to reduce Google Maps calls.  

* The solution queries the database for distances between all the kiosks and loads them into a graph where the vertices are the kiosks and the edges are driving distances
* A copy of the graph is made to perform operations on.
* The maximum length of the desired paths are set to half the number of vertices plus 1, in order to get paths of the same length that visit every node.
* The desired paths are initialized with the Farmers Fridge Kitchen as the start.
* Next, the folowing iterative process is done on the first path and graph copy until it reaches the maximum desired path length:
  * The maximum number of intermediate vertices in the path to the closest kiosk is set as the difference between the max desired path length and the length of the first path.
  * The vertices in the first desired path are removed from the graph copy(minus the starting vertex).
  * The Prims Spanning Tree algorithm is used on the starting vertex and the graph copy to create a minimum weight(distance) spanning tree from the start. This creates a minimized shortest path from the starting vertex to every reachable vertex on the graph copy.
  * The spanning tree is used to find the closest kiosk with the most amount of stops that dont push the first path over the maximum desired path length.
  * The path to the closest kiosk is appended to the first path.
  * The starting vertex is set to the closest kiosk
* After the first path is constructed, all the vertices in the first path are removed from a new copy of the original graph, the start is set back to the Farmers Fridge Kitchen, and the above process is run again on the new copy of the graph to get the second path.
