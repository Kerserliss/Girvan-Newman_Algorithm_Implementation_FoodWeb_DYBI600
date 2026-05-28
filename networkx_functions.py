import networkx as nx
import itertools
from girvannewman import _modularity
from girvannewman import _communities
from girvannewman import girvannewman
from networkx.algorithms.community.quality import modularity
import matplotlib.pyplot as plt
from Graph import Graph
from performance_evaluation import random_graph

def bis_communities(g, k):
    comp = nx.community.girvan_newman(g)
    
    for communities in comp:
        if len(communities) >= k:
            return [set(c) for c in communities]
    
    return None
    
def bis_modularity(g):
    best_Q = -100
    best_partition = None 

    g_current = g.copy()

    while g_current.number_of_edges() > 0:
        betweenness = nx.edge_betweenness_centrality(g_current)
        edge = max(betweenness, key=lambda e: betweenness[e])
        g_current.remove_edge(*edge)
        partition = list(nx.connected_components(g_current))
        Q = modularity(g, partition)

        if Q > best_Q :
            best_Q = Q
            best_partition = partition
    return best_partition, best_Q

def to_networkx(g):
    g_nx = nx.Graph()
    for v in g.vertices:
        g_nx.add_node(v)
    for v in g.vertices:
        for u in g.get_neighborhood(v):
            g_nx.add_edge(v, u)
    return g_nx


def comparison_communities(g, k):
    g_nx = to_networkx(g)
    ntx_partition = bis_communities(g_nx, k)
    best_partition_com = _communities(g,k, return_graph= False)

    in_communities = {}

    for i, community in enumerate(best_partition_com):
        for vertex in community:
            in_communities[str(vertex)] = i
    
    in_communities_ntx = {}

    for i, community in enumerate(ntx_partition):
        for vertex in community:
            in_communities_ntx[str(vertex)] = i

    resemblance = 0
    differences = 0
    total = len(in_communities)

    for vertex in in_communities:
        com_mod = {v for v in in_communities if in_communities[v] == in_communities[vertex]}
        if vertex not in in_communities_ntx:
            differences += 1
            continue
        
        com_nx = {v for v in in_communities_ntx if in_communities_ntx[v] == in_communities_ntx.get(vertex)}

        if com_mod == com_nx:
            resemblance += 1
        else:
            differences += 1
        
    total_resemblance = (resemblance/ total)*100

    return total_resemblance, resemblance, differences


def comparison_modularit(g):
    g_nx = to_networkx(g)
    ntx_partition, ntx_Q = bis_modularity(g_nx)
    best_partition_mod, best_Q_mod = _modularity(g, return_graph= False)

    in_communities = {}

    for i, community in enumerate(best_partition_mod):
        for vertex in community:
            in_communities[str(vertex)] = i
    
    in_communities_ntx = {}

    for i, community in enumerate(ntx_partition):
        for vertex in community:
            in_communities_ntx[str(vertex)] = i

    resemblance = 0
    differences = 0
    total = len(in_communities)

    for vertex in in_communities:
        com_mod = {v for v in in_communities if in_communities[v] == in_communities[vertex]}
        com_nx = {v for v in in_communities_ntx if in_communities_ntx[v] == in_communities_ntx[vertex]}

        if com_mod == com_nx :
            resemblance +=1
        else:
            differences +=1
    
    total_resemblance = (resemblance/ total)*100

    return total_resemblance, resemblance, differences

#test com 
#from loader import load_karate
#g, groups = load_karate()

#print(comparison_communities(g, 2))


def bis_dendogram(g):
    composition = nx.girvan_newman(g)

    partitions = []
    for partition in composition :
        partitions.append(partition)
    
    return partitions
def compare_partitions(partition_custom, partition_nx):
    """Calcule le taux de ressemblance entre deux partitions"""
    in_communities = {}
    for i, community in enumerate(partition_custom):
        for vertex in community:
            in_communities[str(vertex)] = i

    in_communities_ntx = {}
    for i, community in enumerate(partition_nx):
        for vertex in community:
            in_communities_ntx[str(vertex)] = i

    resemblance = 0
    differences = 0
    total = len(in_communities)

    for vertex in in_communities:
        com_mod = {v for v in in_communities if in_communities[v] == in_communities[vertex]}
        if vertex not in in_communities_ntx:
            differences += 1
            continue
        com_nx = {v for v in in_communities_ntx if in_communities_ntx[v] == in_communities_ntx.get(vertex)}
        if com_mod == com_nx:
            resemblance += 1
        else:
            differences += 1

    return (resemblance / total) * 100


def plot_comparison_communities(g, k):
    g_nx = to_networkx(g)
    
    ntx_partition = bis_communities(g_nx, k)
    custom_partition = _communities(g, k, return_graph=False)

    # calcul du taux de ressemblance
    score = compare_partitions(custom_partition, ntx_partition)

    color_list = ["red", "blue", "green", "yellow", "purple", "orange", "pink", "brown"]

    colors_custom = {}
    for i, community in enumerate(custom_partition):
        for vertex in community:
            colors_custom[str(vertex)] = color_list[i % len(color_list)]

    colors_nx = {}
    for i, community in enumerate(ntx_partition):
        for vertex in community:
            colors_nx[str(vertex)] = color_list[i % len(color_list)]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

    pos = nx.spring_layout(g_nx, seed=42)
    nx.draw(g_nx,
            pos=pos,
            node_color=[colors_nx[str(v)] for v in g_nx.nodes()],
            with_labels=True,
            ax=ax1,
            font_size=8)
    ax1.set_title(f"NetworkX - {len(ntx_partition)} communities")

    nx.draw(g_nx,
            pos=pos,
            node_color=[colors_custom[str(v)] for v in g_nx.nodes()],
            with_labels=True,
            ax=ax2,
            font_size=8)
    ax2.set_title(f"Girvan Newman - {len(custom_partition)} communities")

    plt.suptitle(f"Comparison of communities (k={k})\nSimilarity score: {score:.1f}%")
    plt.tight_layout()
    plt.show()


def plot_comparison_modularity(g, return_graph: bool = False):
    g_nx = to_networkx(g)

    ntx_partition, ntx_Q = bis_modularity(g_nx)
    custom_partition, custom_Q = _modularity(g, return_graph=False)

    # calcul du taux de ressemblance
    score = compare_partitions(custom_partition, ntx_partition)

    color_list = ["red", "blue", "green", "yellow", "purple", "orange", "pink", "brown"]

    colors_custom = {}
    for i, community in enumerate(custom_partition):
        for vertex in community:
            colors_custom[str(vertex)] = color_list[i % len(color_list)]

    colors_nx = {}
    for i, community in enumerate(ntx_partition):
        for vertex in community:
            colors_nx[str(vertex)] = color_list[i % len(color_list)]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

    pos = nx.spring_layout(g_nx, seed=42)

    nx.draw(g_nx,
            pos=pos,
            node_color=[colors_nx[str(v)] for v in g_nx.nodes()],
            with_labels=True,
            ax=ax1,
            font_size=8)
    ax1.set_title(f"NetworkX\n{len(ntx_partition)} communities\nQ={ntx_Q:.3f}")

    nx.draw(g_nx,
            pos=pos,
            node_color=[colors_custom[str(v)] for v in g_nx.nodes()],
            with_labels=True,
            ax=ax2,
            font_size=8)
    ax2.set_title(f"Girvan Newman\n{len(custom_partition)} communities\nQ={custom_Q:.3f}")

    plt.suptitle(f"Comparison of partitions by modularity\nSimilarity score: {score:.1f}%")
    plt.tight_layout()
    plt.show()

#rom loader import load_karate
#g, groups = load_karate()

#g , communities= random_graph(6,100)
#plot_comparison_communities(g, 5)
#plot_comparison_modularity(g, False)
#print(comparison_modularit(g))
#print(comparison_communities(g, 5))

def average_comparison_communities(nb_tests: int = 10, k_values: list = list(range(2, 11))):
    """
    Calcule la moyenne des différences entre NetworkX et notre version
    en fonction du nombre de communautés (k de 2 à 10)
    """
    results = {}

    for k in k_values:
        scores = []
        
        for _ in range(nb_tests):
            # générer un graphe aléatoire avec k communautés et 85 arêtes
            g, _ = random_graph(k, 85)
            g_nx = to_networkx(g)

            # récupérer les partitions
            custom_partition = _communities(g, k)
            ntx_partition = bis_communities(g_nx, k)

            if custom_partition is None or ntx_partition is None:
                continue

            # calculer le score
            score = compare_partitions(custom_partition, ntx_partition)
            scores.append(score)

        if scores:
            results[k] = {
                'mean': sum(scores) / len(scores),
                'min': min(scores),
                'max': max(scores)
            }

    return results


def plot_average_comparison(nb_tests: int = 10, k_values: list = list(range(2, 11))):
    """
    Visualise la moyenne des différences entre NetworkX et notre version
    en fonction du nombre de communautés k
    """
    results = average_comparison_communities(nb_tests, k_values)

    ks = list(results.keys())
    means = [results[k]['mean'] for k in ks]
    mins = [results[k]['min'] for k in ks]
    maxs = [results[k]['max'] for k in ks]

    fig, ax = plt.subplots(figsize=(10, 6))

    # courbe moyenne
    ax.plot(ks, means, 'b-o', label='Moyenne', linewidth=2)

    # zone min/max
    ax.fill_between(ks, mins, maxs, alpha=0.2, color='blue', label='Min/Max')

    ax.set_xlabel("Nombre de communautés k")
    ax.set_ylabel("Score de ressemblance (%)")
    ax.set_title(f"Comparaison NetworkX vs Notre version\n({nb_tests} tests par k, 85 sommets)")
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.set_ylim(0, 100)
    ax.set_xticks(ks)

    plt.tight_layout()
    plt.show()

    # afficher les résultats
    print("\nRésultats :")
    print(f"{'k':>5} {'Moyenne':>10} {'Min':>10} {'Max':>10}")
    print("-" * 38)
    for k, vals in results.items():
        print(f"{k:>5} {vals['mean']:>9.1f}% {vals['min']:>9.1f}% {vals['max']:>9.1f}%")


# Test
plot_average_comparison(nb_tests=10)