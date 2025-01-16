from graph import Graphique
from algorithms import *
import copy
import sys

for i in range(1, 11):

    fichier = f"Propositions/Proposition {i}.txt"
    output_file = f"C3-trace/C3-trace{i}-FF.txt"

    with open(output_file, "w") as f:
        
        sys.stdout = f  # Rediriger print vers le fichier

        print(f"Fichier sélectionné : {fichier}")

        graph = Graphique.read_graph(fichier)
        graph.display()
        graphford = copy.deepcopy(graph)
        graphpush = copy.deepcopy(graph)


        print ("\n/////////////////////////Ford Fulkerson/////////////////////////") 
        max_flowford = ford_fulkerson(graphford)
        graphford.display_flow()

        print(f"\nMax flow Ford-Fulkerson: {max_flowford}")

        """
        print ("\n////////////////////////Pousser Réétiqueter/////////////////////////\n") 
        max_flowpush = push_relabel(graphpush)
        graphpush.display_flow()

        print(f"\nMax flow Push-Relabel: {max_flowpush}")




        for i in range(2):
            if i == 0:
                print ("\n/////////////////////////Ford Fulkerson/////////////////////////") 
                max_flowford = ford_fulkerson(graphford)
                graphford.display_flow()

                print(f"\nMax flow Ford-Fulkerson: {max_flowford}")
            else:
                print ("\n////////////////////////Pousser Réétiqueter/////////////////////////\n") 
                max_flowpush = push_relabel(graphpush)
                graphpush.display_flow()

                print(f"\nMax flow Push-Relabel: {max_flowpush}")

            print (f"\n//////////// Min avec ", "Ford Fulkerson" if i == 0 else "Pousser Réétiqueter", "////////////\n") 
            for j in range(max_flowford):
                j+=1
                target = j
                graphmin = copy.deepcopy(graph)

                print (f"\n//////////// Target flow {j} avec", "Ford Fulkerson" if i == 0 else "Pousser Réétiqueter", "////////////\n") 
                max_flow = min_cost_flow(graphmin, target)

                graphmin.display()
                graphmin.display_flow()
                print(f"Max flow: {max_flow}")"""

        # Restaurer la sortie standard
        sys.stdout = sys.__stdout__
        print(f"Résultats enregistrés dans {output_file}")