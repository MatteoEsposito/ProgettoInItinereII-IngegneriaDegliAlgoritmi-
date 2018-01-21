# coding=utf-8
from graph.Graph_IncidenceList import GraphIncidenceList
from graph.mst import kruskal
import random


def generateAcycleGraph(nds):
    """
    Funzione atta a creare grafi pseudo-randomici non diretti e aciclici
    :param nds: int - numero di nodi
    :time O(n^2)
    :return: graph
    """
    graph = GraphIncidenceList()
    random.seed

    #   Crea tanti nodi quanto specificato nel parametro nds
    nodes = []
    for i in range(nds):
        node = graph.addNode(i)
        nodes.append(node)

    #   Connette con pesi randomici ogni singolo nodo
    #   a tutti gli altri nodi
    for src in nodes:
        for dst in nodes:
            generic_weight = random.sample(range(nds),1)[0]
            graph.insertEdge(src.id, dst.id, generic_weight)

    #   Dalla nuova versione, il grafo viene inizializzato con tutti i nodi connessi
    #   a tutti con pesi però randomici, allora ora mi genero una Minimo Albero Ricoprente
    #   sfruttando Kruskal e la sua implementazione che restituisce una lista di archi
    w_kruskal, mst_kruskal = kruskal(graph)

    #   Elimino tuti gli archi dal grafo originale
    for edge in graph.getEdges():
        graph.deleteEdge(edge.tail, edge.head)

    #   Ora riconnetto il grafo con gli archi del suo Minimo Albero Ricoprente
    #   secondo l'invocazione precedente dell'algorimto di Kruskal
    for edge in mst_kruskal:
        graph.insertEdge(edge.tail, edge.head, edge.weight)

    return graph

def generateCyclicGraph(nds):
    """
    Funzione che genera grafici ciclici.
    Piccola Nota:
    L'algoritmo di Brandes riporta un nodo qualsiasi ( normalmente il primo )
    in un grafo completamente connesso ove ogni nodo è connesso
    ad ogni altro nodo, nessun di essi propriamente si trova più
    al centro rispetto ad un'altro in quanto è comuqnue possibile
    mappare ogni singolo nodo al centro di una sfera costituita
    dagli altri nodi del grafo e avere di volta in volta ogni singolo nodo
    come risultato. Infatti in tal caso l'algoritmo riporta 0 per ogni singolo valore
    :param nds: int - numero di nodi
    :Time O(n^2)
    :return: graph
    """
    graph = GraphIncidenceList()
    random.seed()
    #   Crea tanti nodi quanto specificato nel parametro nds
    nodes = []
    for i in range(nds):
        node = graph.addNode(i)
        nodes.append(node)

    #   Crea gli archi per connettere i vari nodi
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
    #   N.B: rimuovere randomicamente un grafo serve esclusivamente ad assicuraci:
    #        1) di non avere grafi completamente connessi
    #        2) aumenta il fattore di "randomicità" del grafo
    n_1 = random.sample(range(len(nodes)), 1)[0]
    n_2 = random.sample(range(len(nodes)), 1)[0]
    graph.deleteEdge(nodes[n_1].id, nodes[n_2].id)

    return graph
