import matplotlib.pyplot as plt
from random import random
class Graph :
    """
    Class used to represent a Graph in our project
    Uses Adjacency Lists to save neighbors

    Later all functions implemented to run Girvan-Newman algorithm on graphs are based on this class
    """
    def __init__(self):
        self.nb_vertices = 0
        self.vertices = []
        self.neighborhoods = []

    def add_vertex(self, vertex):
        if vertex in self.vertices:
            print("The vertex is already in the graph.")
        else:
            self.vertices.append(vertex)
            self.nb_vertices += 1
            print("The vertex is added.")
    
    def remove_vertex(self, vertex):
        pass

    def add_neighbor(self, vertex,neighbor):
        if neighbor not in self.vertices :
            print("The neighbor is not in the vertices")
        elif vertex not in self.vertex:
            print("The vertex is not in the vertices")
        else:
            self.neighborhoods[self.vertices.index(vertex)].add(self.vertices.index(neighbor))

    def display_graph(self, k: int = 10, desired: float = 0.2, repulsion: float = 0.1, attraction: float = 0.1) -> None:
        """
        This function computes an appropriate render for our graph on a matplotlib plot.
        """
        positions = [[random(), random()] for _ in range(self.nb_vertices)]
        all_vertices = set(self.vertices)

        for _ in range(k):
            change_vectors = [[] for _ in range(self.nb_vertices)]
            for p in self.vertices:
                i = self.vertices.index(p)
                not_neighbors = all_vertices - set(self.get_neighborhood(p))

                # Repulsion
                for nn in not_neighbors:
                    j = self.vertices.index(nn)
                    dx = positions[i][0] - positions[j][0]
                    dy = positions[i][1] - positions[j][1]
                    dist = max(0.01, (dx**2 + dy**2)**0.5)
                    force = repulsion / dist
                    change_vectors[i].append([dx/dist * force, dy/dist * force])

                # Attraction
                for n in self.get_neighborhood(p):
                    j = self.vertices.index(n)
                    dx = positions[i][0] - positions[j][0]
                    dy = positions[i][1] - positions[j][1]
                    dist = max(0.01, (dx**2 + dy**2)**0.5)
                    force = attraction * (dist - desired)
                    change_vectors[i].append([-dx/dist * force, -dy/dist * force])

            # Apply change vectors
            for i in range(self.nb_vertices):
                final_dx = sum([x[0] for x in change_vectors[i]])
                final_dy = sum([x[1] for x in change_vectors[i]])
                positions[i][0] += final_dx
                positions[i][1] += final_dy

        x, y = [pos[0] for pos in positions], [pos[1] for pos in positions]

        # Plot vertices
        fig, ax = plt.subplots()
        ax.scatter(x, y, c='red')

        # Plot edges
        for p in self.vertices:
            i = self.vertices.index(p)
            for n in self.get_neighborhood(p):
                j = self.vertices.index(n)
                ax.plot([x[i], x[j]], [y[i], y[j]], 'b-')

        plt.title("Graph")
        plt.show()

    
