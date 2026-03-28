import Graph as g
import csv 

def load_karate():
    groupes = {}
    karate_graph = g.Graph()
    with open("Karate_club_dataset/nodes.csv") as fnodes:
        nodes = csv.reader(fnodes)
        next(nodes)
        for line in nodes:
            karate_graph.add_vertex(line[1])
            if line[2] not in groupes.keys():
                groupes[line[2]] = [line[1]]
            else :
                groupes[line[2]].append(line[1])
    
    with open("Karate_club_dataset/edges.csv") as fedges :
        edges = csv.reader(fedges)
        next(edges)
        for line in edges:
            print(line[0])
            
            karate_graph.add_edge(line[0], line[1])
    
    return karate_graph, groupes

            

karate_graph, groupes = load_karate()[0],load_karate()[1]

