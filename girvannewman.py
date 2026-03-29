from Graph import Graph

"""
TODO list:
    - Compute betweeness
    - Remove highest betweeness edge
    - Check end condition

What I found as end conditions:
    - Modularity (a way to tell when a graph is modular enough)
    - Remove every edge and produce a full dendrogram
    - Max nb of communities reached
    others ?

What I found for betweeness:
    - Brandes Algorithm

"""

def brandes(g: Graph):
    pass

def _modularity(g: Graph):
    pass

def _dendrogram(g: Graph):
    pass

def _communities(g: Graph, k: int):
    pass


def girvannewman(g: Graph, method: str="modularity", k: int|None = None):
    match method:
        case "modularity":
            _modularity(g)
        case "dendrogram":
            _dendrogram(g)
        case "communities":
            _communities(g, k)
        case _:
            raise ValueError("Method is not valid, should be 'modularity', 'dendrogram' or 'communities'")