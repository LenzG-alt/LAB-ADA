import time
from random import choice

# tryItABunch: runs a function a bunch, and times how long it takes.
#
# Input: myFn: a function which takes as input a list of integers
# Output: lists nValues and tValues so that running myFn on a list of length nValues[i] took (on average over numTrials tests) time tValues[i] milliseconds.
#
# Other optional args:
#    - startN: smallest n to test
#    - endN: largest n to test
#    - stepSize: test n's in increments of stepSize between startN and endN
#    - numTrials: for each n tests, do numTrials tests and average them
#    - listMax: the input lists of length n will have values drawn uniformly at random from range(listMax)
def tryItABunch(myFn, startN=10, endN=100, stepSize=10, numTrials=20, listMax = 10):
    nValues = []
    tValues = []
    for n in range(startN, endN, stepSize):
        # run myFn several times and average to get a decent idea.
        runtime = 0
        for t in range(numTrials):
            lst = [ choice(range(listMax)) for i in range(n) ] # generate a random list of length n
            start = time.time()
            myFn( lst )
            end = time.time()
            runtime += (end - start) * 1000 # measure in milliseconds
        runtime = runtime/numTrials
        nValues.append(n)
        tValues.append(runtime)
    return nValues, tValues

# next, you can do:
# plot(nValues, tValues)
# or something like that


import math

class Vertex:
    def __init__(self, v):
        self.inNeighbors = []
        self.outNeighbors = []
        self.value = v
        # util para DFS/BFS/Dijkstra
        self.inTime = None
        self.outTime = None
        self.status = "unvisited"
        self.parent= None
        # Para Dijkstra
        self.estD = math.inf  # Estimación de distancia

    def hasOutNeighbor(self,v):
        if v in self.getOutNeighbors():
            return True
        return False

    def hasInNeighbor(self,v):
        if v in self.getInNeighbors():
            return True
        return False

    def hasNeighbor(self,v):
        if v in self.getInNeighbors() or v in self.getOutNeighbors():
            return True
        return False

    def getOutNeighbors(self):
        return [v[0] for v in self.outNeighbors]

    def getInNeighbors(self):
        return [v[0] for v in self.inNeighbors]

    def getOutNeighborsWithWeights(self):
        return self.outNeighbors

    def getInNeighborsWithWeights(self):
        return self.inNeighbors

    def addOutNeighbor(self,v,wt):
        self.outNeighbors.append((v,wt))

    def addInNeighbor(self,v,wt):
        self.inNeighbors.append((v,wt))

    def __str__(self):
        return str(self.value)

# También se puede utilizar como un grafo no dirigido agregando aristas en ambas direcciones.

class Graph:
    def __init__(self):
        self.vertices = []

    def addVertex(self,n):
        self.vertices.append(n)

    # agregar una arista dirigida del  Nodo u al Nodo v
    def addDiEdge(self,u,v,wt=1):
        u.addOutNeighbor(v,wt=wt)
        v.addInNeighbor(u,wt=wt)

    # agregar aristas en ambas direcciones entre u y v
    def addBiEdge(self,u,v,wt=1):
        self.addDiEdge(u,v,wt=wt)
        self.addDiEdge(v,u,wt=wt)

    # obtener una lista de todos las aristas dirigidas
    #
    def getDirEdges(self):
        ret = []
        for v in self.vertices:
          for u, wt in v.getOutNeighborsWithWeights():
            ret.append( [v,u,wt] )
        return ret

    def __str__(self):
        ret = "Grafo con:\n"
        ret += "\t Vertices:\n\t"
        for v in self.vertices:
            ret += str(v) + ","
        ret += "\n"
        ret += "\t Aristas:\n\t"
        for a,b,wt in self.getDirEdges():
            ret += "(" + str(a) + "," + str(b) + "; wt:" + str(wt)+") "
        ret += "\n"
        return ret


def dijkstraDumb(w, G):
    for v in G.vertices:
        v.estD = math.inf
    w.estD = 0
    unsureVertices = G.vertices[:]  # copia de la lista de vértices

    while len(unsureVertices) > 0:
        u = None
        minD = math.inf
        for x in unsureVertices:
            if x.estD < minD:
                minD = x.estD
                u = x
        if u is None:
            return  # desconectado

        for v, wt in u.getOutNeighborsWithWeights():
            if u.estD + wt < v.estD:
                v.estD = u.estD + wt
                v.parent = u
        unsureVertices.remove(u)

from heapdict import heapdict

def dijkstraHeap(start, G):
    for v in G.vertices:
        v.estD = math.inf
    start.estD = 0

    pq = heapdict()
    for v in G.vertices:
        pq[v] = v.estD

    while len(pq) > 0:
        u, dist_u = pq.popitem()
        if dist_u == math.inf:
            continue  # nodo inalcanzable

        for v, wt in u.getOutNeighborsWithWeights():
            if u.estD + wt < v.estD:
                v.estD = u.estD + wt
                v.parent = u
                pq[v] = v.estD  # actualizar en la cola

import time
import math
import matplotlib.pyplot as plt
import networkx as nx
from heapdict import heapdict
import random

def randomGraph(n, num_edges_per_vertex=2, wts=[1]):
    G = Graph()
    V = [Vertex(i) for i in range(n)]
    for v_obj in V: # Use v_obj to avoid conflict with outer v
        G.addVertex(v_obj)

    if n == 0:
        return G

    for v_obj in V: # Use v_obj to avoid conflict with outer v
        # Ensure we don't try to pick more neighbors than available
        actual_num_edges = min(num_edges_per_vertex, n - 1 if n > 0 else 0)
        if actual_num_edges <= 0 and n > 1: # if n=1, actual_num_edges can be 0
             continue


        # Create a list of potential neighbors, excluding v_obj itself
        potential_neighbors = [neighbor for neighbor in V if neighbor != v_obj]

        # Shuffle potential_neighbors to pick randomly
        random.shuffle(potential_neighbors)

        # Select the first 'actual_num_edges' neighbors
        selected_neighbors = potential_neighbors[:actual_num_edges]

        for neighbor_obj in selected_neighbors: # Use neighbor_obj
            G.addDiEdge(v_obj, neighbor_obj, wt=random.choice(wts))
    return G


def pruebaDijkstraArray(lst):
    n = len(lst)
    G = randomGraph(n)
    inicio = G.vertices[0]
    dijkstraDumb(inicio, G)

def pruebaDijkstraHeap(lst):
    n = len(lst)
    G = randomGraph(n)
    inicio = G.vertices[0]
    dijkstraHeap(inicio, G)

from random import choice

nValues, tValues_array = tryItABunch(pruebaDijkstraArray,startN=10,endN=1000,stepSize=10,numTrials=2,listMax=1)

_, tValues_heap = tryItABunch(pruebaDijkstraHeap,startN=10,endN=1000,stepSize=10,numTrials=2,listMax=1)

plt.plot(nValues, tValues_array, label='Dijkstra con Array')
plt.plot(_, tValues_heap, label='Dijkstra con Heap')
plt.xlabel('Número de vértices')
plt.ylabel('Tiempo promedio (ms)')
plt.title('Comparación Dijkstra: Array vs Heap (con randomGraph)')
plt.legend()
plt.grid(True)
plt.savefig('dijkstra_comparison_plot.png')
print("Plot saved to dijkstra_comparison_plot.png")
