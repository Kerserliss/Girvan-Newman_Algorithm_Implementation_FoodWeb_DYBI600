import Graph as g
import csv 

name_food_web = {
    0 : "Phytoplancton", 
    1 : "Bacteria attached to suspended POC",
    2 : "Bacteria attached to sediment POC", 
    3 : "Benthic diatoms", 
    4 : "Free bacteria in water columns/DOC", 
    5 : "Heterotrophic microflagellates", 
    6 : "Microzooplankton",
    7 : "Zooplankton", 
    8 : "Cnetophores", 
    9 : "Sea nettle", 
    10 : "Other suspendions feeders", 
    11 : "Softshell clam", 
    12 : "American oysters", 
    13 : "Other polychaetes", 
    14 : "Nereis (Rag Worm)", 
    15 : "Macoma spp (bivalve)", 
    16 : "MeioFauna", 
    17 : "Crustacean deposit feeders", 
    18 : "Blue Crab", 
    19 : "Fish Larvae", 
    20 : "Alewife and Blue herring", 
    21 : "Bay anchovy", 
    22 : "Atlantic menhaden", 
    23 : "American Shad", 
    24 : "Atlantic Croaker", 
    25 : "Hogchoker", 
    26 : "Spot", 
    27 : "White Perch", 
    28 : "Sea catfish", 
    29 : "Bluefish", 
    30 : "Weakfish", 
    31 : "Summer Flounder", 
    32 : "Striped bassy", 
    }

foodweb_groups = {
    "benthic": [
        2,
        3,
        11,
        12,
        13,
        14,
        15,
        17,
        18,
        24,
        25,
        26,
        28,
        30,
        31

    ],
    "pelagic": [
        0,
        1,
        4,
        6,
        7,
        8,
        9,
        19,
        20,
        21,
        22,
        23,
        29,
        32

    ],
    "undetermined": [
        5,
        10,
        16,
        27

    ]
}

def load_karate():
    """
        Function to load the karate club dataset. Will return the graph and the groups in the graph.
    """

    # Initilaze dict and graph.
    groups = {}
    karate_graph = g.Graph(name="Karate dataset")

    # Open the first csv file where the vertices are in.
    with open("data/Karate_club_dataset/nodes.csv") as fnodes:
        nodes = csv.reader(fnodes)

        # Skip the first line with the columns names.
        next(nodes)

        # For each line :
        for line in nodes:
            # Add the vertex.
            karate_graph.add_vertex(line[1])

            # Add in which community is in.
            if line[2] not in groups.keys():
                groups[line[2]] = [line[1]]
            else :
                groups[line[2]].append(line[1])
    
    # Open the second csv file with the edges.
    with open("data/Karate_club_dataset/edges.csv") as fedges :
        edges = csv.reader(fedges)

        # Skip the first line with the columns names.
        next(edges)
        # For each line :
        for line in edges:

            # Add the edge with + 1, because in the file index are used and not name.
            karate_graph.add_edge(str(int(line[0])+1), str(int(line[1])+1))
    
    return karate_graph, groups

def load_college_football():
    """
        Function to load the college football network dataset. Will return the graph and the groups in the graph.
    """

    # Initilaze dict and graph.
    groups = {}
    college_football_graph = g.Graph(name="College_football_dataset")

    # Open the first csv file where the vertices are in.
    with open("data/NCAA_college_football_2000_dataset/nodes.csv") as fnodes:
        nodes = csv.reader(fnodes)
        next(nodes)

        # For each line : 
        for line in nodes:
            # Add the vertex.
            college_football_graph.add_vertex(line[1])

            # Add in which community is in.
            if line[2] not in groups.keys():
                groups[line[2]] = [line[1]]
            else :
                groups[line[2]].append(line[1])

    # Open the second csv file with the edges.

    with open("data/NCAA_college_football_2000_dataset/edges.csv") as fedges :
        edges = csv.reader(fedges)

        # Skip the first line with the columns names.
        next(edges)
        # For each line :
        for line in edges:
            # Add the edge with + 1, because in the file index are used and not name.
            college_football_graph.add_edge(college_football_graph.get_vertex(int(line[0])), college_football_graph.get_vertex(int(line[1])))
    
    return college_football_graph, groups

def load_data_food_web_mat1():
    """
        Function to load the foodweb dataset. Will return the graph.
    """
    foodweb_graph = g.Graph(name="FoodWeb")
    with open("data/Foodweb_data/mat_fig7.txt") as fmat :
        lines  = fmat.readlines()
        # assert len(lines) == 36, "Not the right count of vertices in the files."
        line_init = lines[0].strip().split()
        k = 0 
        line_init = line_init[1:]
        while k < (len(line_init)) :
            foodweb_graph.add_vertex(name_food_web[k])
            k+=1
        for i in range(len(lines)):
            line = lines[i].strip().split()[1:]
            for j in range(len(lines)):
                if int(line[j]) > 0:
                    foodweb_graph.add_edge(foodweb_graph.get_vertex(i),foodweb_graph.get_vertex(j))
    
    groups = {k:[] for k in range(len(foodweb_groups.keys()))}
    for k,v_list in enumerate(foodweb_groups.values()):
        for v in v_list:
            groups[k].append(name_food_web[v])


    return foodweb_graph, groups

if __name__ == "__main__":            
    karate_graph, groups = load_karate()

    college_graph, groups2 = load_college_football()
    foodweb_graph = load_data_food_web_mat1()
    foodweb_graph.plot(labels=True)
    dict_n ={}
    for v in foodweb_graph.vertices:
        dict_n[v] = len(foodweb_graph.neighborhoods[v])
    print(dict_n)
    #print(groups2)
    #college_graph.plot()
    #karate_graph.plot(labels=True)
