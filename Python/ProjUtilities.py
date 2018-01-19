# coding=utf-8
from graph.Graph_IncidenceList import GraphIncidenceList
import random


def generateAcycleGraph(nds):
    """
    Funzione atta a creare pseudo-random grafi non diretti e aciclici
    :param nds: int - numero di nodi
    :time O(n^2)
    :return: graph
    """
    graph = GraphIncidenceList()
    random.seed
    # add nodes
    nodes = []
    for i in range(nds):
        node = graph.addNode(i)
        nodes.append(node)

    # connect all nodes
    for src in nodes:
        for dst in nodes:
            #if dst.id > src.id:
            generic_weight = random.sample(range(nds),1)[0]
            graph.insertEdge(src.id, dst.id, generic_weight)

    return graph

def generateCyclicGraph(nds):
    """
    Funzione che genera grafici ciclici.
    L'algoritmo di Brandes non riesce a calcolare, a quanto pare,
    la betweennes centrality in un grafo completamente ciclico
    anche perchè effettivamente in un grafo completamente connesso
    ad ogni sua componente nessun nodo propriamente si trova più
    in mezzo ripestto ad un'altro in quanto è comuqnue posisbile
    mappare ogni singolo nodo al centro di una sfera costituita
    dagli altri nodi del grafo
    :param nds: int - numero di nodi
    :Time O(n^2)
    :return: graph
    """
    graph = GraphIncidenceList()
    random.seed()
    # add nodes
    nodes = []
    for i in range(nds):
        node = graph.addNode(i)
        nodes.append(node)

    # Crea archi per i nodi
    for src in nodes:
        for dst in nodes:
            if dst.id != src.id:

                #   Parte Pseudo-Randomica in cui viene essenzialmente fatto il seeding
                #   della funzione random, al fine di aumentare la possibilità
                #   di generare numeri ancor più "pesudo-randomici"
                random.seed()

                #   Come da implementazioen forniteci, connette ogni nodo ad ogni nodo
                graph.insertEdge(src.id, dst.id, 0)

                #   Ma susseguentemente, attraverso i valori casuali, elimina qualche arco, al fine di non avere
                #   un grafo completamente connesso, per eivatre il non-sense espresso nella descrizione
                #   di qeusta stessa funzione
                n_1 = random.sample(range(len(nodes)), 1)[0]
                n_2 = random.sample(range(len(nodes)), 1)[0]
                graph.deleteEdge(nodes[n_1].id, nodes[n_2].id);
            else:
                continue

    #   Rifaccio il seed di random
    random.seed()
    #   Rimuovo un'ultimo arco
    n_1 = random.sample(range(len(nodes)), 1)[0]
    n_2 = random.sample(range(len(nodes)), 1)[0]
    graph.deleteEdge(nodes[n_1].id, nodes[n_2].id);
    return graph