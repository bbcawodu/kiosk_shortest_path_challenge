# -*- coding: utf-8 -*-
import json
import csv
import os
import googlemaps
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_models import KioskLocations
from db_models import TravelDiatances
from settings import DATABASE_URL
from settings import GOOGLE_API_KEY


def open_csv_file_and_convert_data_to_list(csv_file, encoding=None):
  if encoding:
    with open(csv_file, encoding=encoding) as file_obj:
        reader = csv.reader(file_obj)
        data_list = list(reader)
  else:
    with open(csv_file) as file_obj:
        reader = csv.reader(file_obj)
        data_list = list(reader)

  return data_list


def load_data_from_csv(f_name):
  cur_path = os.path.dirname(__file__)
  csv_file_name = os.path.join(os.path.dirname(cur_path), f_name)
  csv_list = open_csv_file_and_convert_data_to_list(csv_file_name)
  csv_list_data = csv_list[1:]

  return csv_list_data


def add_locations_to_db(db_session, locations_from_csv):
  location_db_row = KioskLocations(
    name='Farmers Fridge Kitchen',
    address='Lake and Racine Ave',
    latitude=41.8851024,
    longitude=-87.6618988,
  )
  db_session.add(location_db_row)

  for location_csv_row in locations_from_csv:
    location_db_row = KioskLocations(
      name=location_csv_row[0],
      address=location_csv_row[1],
      latitude=location_csv_row[2],
      longitude=location_csv_row[3],
    )
    db_session.add(location_db_row)

  db_session.commit()


def get_driving_distances_and_add_to_db(db_session):
  gmaps = googlemaps.Client(key=GOOGLE_API_KEY)
  kiosk_locations = db_session.query(KioskLocations).order_by(KioskLocations.id)

  locations_copy = kiosk_locations
  for location_1 in kiosk_locations:
    origins = [(location_1.latitude, location_1.longitude)]
    destinations = []
    destination_db_objects = []
    for location_2 in locations_copy:
      if location_1.id != location_2.id:
        destination_db_objects.append(location_2)
    for location_2 in destination_db_objects:
      destinations.append((location_2.latitude, location_2.longitude))

    distance_matrix = gmaps.distance_matrix(
      origins,
      destinations,
      language="eng-US",
      mode="driving"
    )['rows']
    travel_distances = distance_matrix[0]['elements']

    for idx, location_2 in enumerate(destination_db_objects):
      travel_distance_dict = travel_distances[idx]
      travel_distance_row = TravelDiatances(
        from_kiosk_location_id=location_1.id,
        to_kiosk_location_id=location_2.id,
        distance=travel_distance_dict['distance']['value'],
      )
      db_session.add(travel_distance_row)
      db_session.commit()


def main():
  engine = create_engine(DATABASE_URL, echo=False)
  Session = sessionmaker(bind=engine)

  file_name ='kiosk_coords.csv'
  kiosk_data_from_csv = load_data_from_csv(file_name)
  
  db_session = Session()

  add_locations_to_db(db_session, kiosk_data_from_csv)
  get_driving_distances_and_add_to_db(db_session)

  db_session.close()


if __name__ == "__main__":
  main()
