class Vertex(object):
  """
  Vertex data structure for the adjacency list implementation of the Graph ADT. Adjacency list implementation of the graph adt requires vertec data structure/class because the
  edges/neighbors of each vertex are maintained on the vertex object while the master list of verticies are maintained on the Graph data structure/class.
  """

  def __init__(self, key, db_row=None):
    self.id = key
    self.connectedTo = {}
    self.db_row = db_row
    self.color = 'white'
    self.distance = 0
    self.predecessor = None

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

  def setDistance(self, dist):
    self.distance = dist

  def getDistance(self):
    return self.distance

  def setPred(self, pred):
    self.predecessor = pred

  def getPred(self):
    return self.predecessor


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

  def delVertex(self, key):
    del self.vertList[key]
    self.numVertices -= 1

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


class PriorityQueue(object):
  def __init__(self):
    self.heapList = [(0,0)]
    self.currentSize = 0

  def percUp(self,i):
    while i // 2 > 0:
      if self.heapList[i][0] < self.heapList[i // 2][0]:
        tmp = self.heapList[i // 2]
        self.heapList[i // 2] = self.heapList[i]
        self.heapList[i] = tmp
      i = i // 2

  def insert(self,k):
    self.heapList.append(k)
    self.currentSize = self.currentSize + 1
    self.percUp(self.currentSize)

  def percDown(self,i):
    while (i * 2) <= self.currentSize:
      mc = self.minChild(i)
      if self.heapList[i][0] > self.heapList[mc][0]:
        tmp = self.heapList[i]
        self.heapList[i] = self.heapList[mc]
        self.heapList[mc] = tmp
      i = mc

  def minChild(self,i):
    if i * 2 + 1 > self.currentSize:
      return i * 2
    else:
      if self.heapList[i*2][0] < self.heapList[i*2+1][0]:
        return i * 2
      else:
        return i * 2 + 1

  def delMin(self):
    retval = self.heapList[1]
    self.heapList[1] = self.heapList[self.currentSize]
    self.currentSize = self.currentSize - 1
    self.heapList.pop()
    self.percDown(1)

    return retval[1]

  def buildHeap(self,alist):
    i = len(alist) // 2
    self.currentSize = len(alist)
    self.heapList = [(0,0)] + alist[:]
    while (i > 0):
      self.percDown(i)
      i = i - 1

  def isEmpty(self):
    return self.currentSize == 0

  def setKeyForValue(self, value, key):
    self.heapList = [heap_tuple for heap_tuple in self.heapList if heap_tuple[0] != 0 and heap_tuple[1] != value]
    self.heapList.append((key, value))
    self.buildHeap(self.heapList)

  def __iter__(self):
    return iter([value[1] for value in self.heapList])
