import copy
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_models import KioskLocations
from db_models import TravelDiatances
from settings import DATABASE_URL
from graph_module import Graph, Vertex, PriorityQueue


def get_two_disjoint_vertex_paths(graph, original_start):
  start = copy.copy(original_start)
  path_1 = [start]
  path_2 = [start]
  final_path_length = graph.numVertices//2 + 1
  graph_copy = copy.copy(graph)

  while len(path_1) < final_path_length:
    max_intermediate_vertices_to_closest = final_path_length - len(path_1)

    graph_copy = copy.copy(graph_copy)
    if len(path_1) > 1:
      for vertex in path_1:
        if vertex.id != start.getId() and vertex.getId() in graph_copy:
          graph_copy.delVertex(vertex.getId())

    generate_prims_spanning_tree(graph_copy, start)
    vertices_without_start = list(vertex for vertex in graph_copy if vertex.id != start.getId())

    verts_with_path_lengths = get_path_lengths(vertices_without_start)
    for vert_with_len in verts_with_path_lengths:
      if vert_with_len[0] < max_intermediate_vertices_to_closest:
        closest_kiosk = vert_with_len[1]
        break

    path = return_path_by_traversing_predecessor_refs(closest_kiosk)[1:]
    path = list(reversed(path))

    if path:
      path_1.extend(path)
    else:
      path_1.append(closest_kiosk)

    start = closest_kiosk



  graph_copy = copy.copy(graph)
  start = copy.copy(original_start)
  for vertex in path_1:
    if vertex.getId() != start.getId() and vertex.getId() in graph_copy:
      graph_copy.delVertex(vertex.getId())

  while len(path_2) < final_path_length:
    max_distance_path = final_path_length - len(path_2)

    graph_copy = copy.copy(graph_copy)
    if len(path_2) > 1:
      for vertex in path_2:
        if vertex.id != start.getId() and vertex.getId() in graph_copy:
          graph_copy.delVertex(vertex.getId())

    generate_prims_spanning_tree(graph_copy, start)
    vertices_without_start = list(vertex for vertex in graph_copy if vertex.id != start.getId())

    verts_with_path_lengths = get_path_lengths(vertices_without_start)
    for vert_with_len in verts_with_path_lengths:
      if vert_with_len[0] < max_distance_path:
        closest_kiosk = vert_with_len[1]
        break

    path = return_path_by_traversing_predecessor_refs(closest_kiosk)[1:]
    path = list(reversed(path))

    if path:
      path_2.extend(path)
    else:
      path_2.append(closest_kiosk)

    start = closest_kiosk

  return path_1, path_2


def get_path_lengths(vertices):
  verts_with_lengths = []
  for vertex in vertices:
    path = return_path_by_traversing_predecessor_refs(vertex)[1:]
    vert_with_len = (len(path), vertex)
    verts_with_lengths.append(vert_with_len)
  verts_with_lengths.sort(key=lambda x: x[0])
  verts_with_lengths = list(reversed(verts_with_lengths))

  return verts_with_lengths

def generate_prims_spanning_tree(G,start):
  pq = PriorityQueue()
  for v in G:
    v.setDistance(sys.maxsize)
    v.setPred(None)
  start.setDistance(0)
  pq.buildHeap([(v.getDistance(),v) for v in G])
  while not pq.isEmpty():
    currentVert = pq.delMin()
    for nextVert in currentVert.getConnections():
      newCost = currentVert.getWeight(nextVert)
      if nextVert in pq and newCost<nextVert.getDistance():
        nextVert.setPred(currentVert)
        nextVert.setDistance(newCost)
        pq.setKeyForValue(nextVert, newCost)


def return_path_by_traversing_predecessor_refs(start):
  path = [start]

  current = start
  while (current.getPred()):
    current = current.getPred()
    path.append(current)
  
  return path


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

  path_1, path_2 = get_two_disjoint_vertex_paths(kiosk_graph, kiosk_graph.getVertex(51))
  path_1_string = "Path 1 is: "
  for vertex in path_1:
    path_1_string = path_1_string + vertex.db_row.name + ", "
  path_1_string = path_1_string[:-2]

  path_2_string = "Path 2 is: "
  for vertex in path_2:
    path_2_string = path_2_string + vertex.db_row.name + ", "
  path_2_string = path_2_string[:-2]

  return_string = path_1_string + "\n" + path_2_string
  print(return_string)

  db_session.close()


if __name__ == "__main__":
  main()
