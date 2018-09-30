class Vertex(object):
  """
  Vertex data structure for the adjacency list implementation of the Graph ADT. Adjacency list implementation of the graph adt requires vertec data structure/class because the
  edges/neighbors of each vertex are maintained on the vertex object while the master list of verticies are maintained on the Graph data structure/class.
  """

  def __init__(self, key, db_row=None):
    self.id = key
    self.db_row = db_row
    self.connectedTo = {}
    self.color = 'white'

  def addNeighbor(self, neighbor, weight=0):
    self.connectedTo[neighbor] = weight

  def __str__(self):
    return str(self.id) + ' connectedTo: ' + str([neighbor.id for neighbor in self.connectedTo])

  def getConnections(self):
    return self.connectedTo.keys()

  def getId(self):
    return self.id

  def getWeight(self, neighbor):
    return self.connectedTo[neighbor]

  def setColor(self, col):
    self.color = col

  def getColor(self):
    return self.color


class Graph(object):
  """
  Graph Data Structure with an adjacency list implementation - Recall that when we give an abstract data type a physical implementation we refer to the implementation as a data structure.
  """
  
  def __init__(self):
    self.vertList = {}
    self.numVertices = 0

  def addVertex(self, key, db_row=None):
    self.numVertices = self.numVertices + 1
    newVertex = Vertex(key, db_row)
    self.vertList[key] = newVertex
    return newVertex

  def getVertex(self, key):
    if key in self.vertList:
      return self.vertList[key]
    else:
      return None

  def __contains__(self, key):
    return key in self.vertList

  def addEdge(self, from_vertex_key, to_vertex_key, cost=0):
    if from_vertex_key not in self.vertList:
      nv = self.addVertex(from_vertex_key)
    if to_vertex_key not in self.vertList:
      nv = self.addVertex(to_vertex_key)
    self.vertList[from_vertex_key].addNeighbor(self.vertList[to_vertex_key], cost)

  def getVertices(self):
    return self.vertList.keys()

  def __iter__(self):
    return iter(self.vertList.values())
