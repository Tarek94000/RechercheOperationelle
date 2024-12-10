from graph import Graphique
from algorithms import *
from utils import *
import copy




fichier = f"fig/fig{6}.txt"
print(f"Fichier sélectionné : {fichier}")

graph = Graphique.read_graph(fichier)
graph.display()
max_flow = ford_fulkerson(graph)
graph.display_flow()