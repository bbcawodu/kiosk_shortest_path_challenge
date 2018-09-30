import copy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_models import KioskLocations
from db_models import TravelDiatances
from settings import DATABASE_URL
from graph_module import Graph, Vertex


def knightTour(n,path,u,limit):
  u.setColor('gray')
  path.append(u)
  if n < limit:
    nbrList = orderByMovesAvail(u)
    i = 0
    done = False
    while i < len(nbrList) and not done:
      if nbrList[i].getColor() == 'white':
        done = knightTour(n+1, path, nbrList[i], limit)
      i = i + 1
    if not done:  # prepare to backtrack
      path.pop()
      u.setColor('white')
  else:
    done = True
  return done


def orderByMovesAvail(n):
  resList = []
  for v in n.getConnections():
    if v.getColor() == 'white':
      c = 0
      for w in v.getConnections():
        if w.getColor() == 'white':
          c = c + 1
      resList.append((c,v))
  resList.sort(key=lambda x: x[0])

  return [y[1] for y in resList]


def add_locations_and_edges_to_graph(kiosk_locations, db_session):
  kiosk_graph = Graph()

  for location in kiosk_locations:
    kiosk_graph.addVertex(location.id, location)

  add_edges_to_graph(kiosk_locations, kiosk_graph, db_session)

  return kiosk_graph


def add_edges_to_graph(kiosk_locations, kiosk_graph, db_session):
  locations_copy = kiosk_locations
  for location_1 in kiosk_locations:
    for location_2 in locations_copy:
      if location_1.id != location_2.id:
        travel_distance_obj = db_session.query(TravelDiatances).\
        filter(TravelDiatances.from_kiosk_location_id==location_1.id).\
        filter(TravelDiatances.to_kiosk_location_id==location_2.id)[0]

        distance = travel_distance_obj.distance
        kiosk_graph.addEdge(location_1.id, location_2.id, distance)


def main():
  engine = create_engine(DATABASE_URL, echo=False)
  Session = sessionmaker(bind=engine)
  db_session = Session()

  kiosk_locations = db_session.query(KioskLocations)
  kiosk_graph = add_locations_and_edges_to_graph(kiosk_locations, db_session)

  # path = []
  # start = kiosk_graph.getVertex(51)
  # found = knightTour(1,path,start,51)
  # print(found)
  # print([vertex.db_row.name for vertex in path])

  for v in kiosk_graph:
    for w in v.getConnections():
      print("( %s , %s , %s )" % (v.db_row.name, w.db_row.name, v.getWeight(w)))

  db_session.close()


if __name__ == "__main__":
  main()
