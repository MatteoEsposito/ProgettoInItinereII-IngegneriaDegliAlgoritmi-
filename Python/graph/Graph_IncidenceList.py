from graph.GraphExtended import GraphExtended
from graph.base import Edge, Node

from list.DoubleLinkedList import ListaDoppiamenteCollegata as List


class GraphIncidenceList(GraphExtended):
    """
    A graph, implemented as an incidence list.
    Each node u has a list containing its incident edges (u,v).
    ---
    Memory Complexity: O(|V|+|E|)
    """

    def __init__(self):
        """
        Constructor.
        """
        super().__init__()
        self.inc = {} # incidence lists {nodeID:listOfIncidentEdges}

    def numEdges(self):
        """
        Return the number of edges.
        :return: the number of edges.
        """
        return sum(len(adj_list) for adj_list in self.inc.values())

    def addNode(self, elem):
        """
        Add a new node with the specified value.
        :param elem: the node value.
        :return: the create node.
        """
        newnode = super().addNode(elem) # create a new node with the correct ID

        self.nodes[newnode.id] = newnode # add the new node to the dictionary
        self.inc[newnode.id] = List() # create the incidence list for the new node

        return newnode

    def deleteNode(self, index):
        """
        Remove the specified node.
        :param nodeId: the node ID (integer).
        :return: void.
        """
        # look for the node
        found = False
        for node in self.nodes.items():
            if index == node[0]:
                found = True
                break

        # if node does not exist, return
        if not found: return

        # remove the node from the set of nodes, that is to remove the node
        # from the dictionary nodes
        del self.nodes[index]

        # remove all edges starting from the node, that is to remove the
        # incidence list for the node
        del self.inc[index]

        # remove all edges pointing to the node, that is to remove all the edges
        # with the node as head from all the incidence lists
        for inc in self.inc.values():
            curr = inc.getFirstRecord()
            while curr is not None:
                if curr.elem.head == index:
                    inc.deleteRecord(curr)
                curr = curr.next

    def getNode(self, id):
        """
        Return the node, if exists.
        :param id: the node ID (integer).
        :return: the node, if exists; None, otherwise.
        """
        return None if id not in self.nodes else self.nodes[id]

    def getNodes(self):
        """
        Return the list of nodes.
        :return: the list of nodes.
        """
        return list(self.nodes.values())

    def insertEdge(self, tail, head, weight=None):
        """
        Add a new edge.
        :param tail: the tail node ID (integer).
        :param head: the head node ID (integer).
        :param weight: the (optional) edge weight (floating-point).
        :return: the created edge, if created; None, otherwise.
        """
        # if tail and head exist, add the entry into the incidence list
        if head in self.nodes and tail in self.nodes: #TODO overwrite if edge already exists
            self.inc[tail].addAsLast(Edge(tail, head, weight))

    def deleteEdge(self, tail, head):
        """
        Remove the specified edge.
        :param tail: the tail node ID (integer).
        :param head: the head node ID (integer).
        :return: void.
        """
        # if tail and head exist, delete the edge
        if tail in self.nodes and head in self.nodes:
            curr = self.inc[tail].getFirstRecord()
            while curr is not None:
                if curr.elem.head == head:
                    self.inc[tail].deleteRecord(curr)
                    break
                curr = curr.next

    def getEdge(self, tail, head):
        """
        Return the node, if exists.
        :param tail: the tail node ID (integer).
        :param head: the head node ID (integer).
        :return: the edge, if exists; None, otherwise.
        """
        if tail in self.nodes and head in self.nodes:
            curr = self.inc[tail].getFirstRecord()
            while curr is not None:
                if curr.elem.head == head:
                    return curr.elem
                curr = curr.next
        return None

    def getEdges(self):
        """
        Return the list of edges.
        :return: the list of edges.
        """
        edges = []
        for inc_val in self.inc.values():
            curr = inc_val.getFirstRecord()
            while curr is not None:
                edges.append(curr.elem)
                curr = curr.next
        return edges

    def isAdj(self, tail, head):
        """
        Checks if two nodes ar adjacent.
        :param tail: the tail node ID (integer).
        :param head: the head node ID (integer).
        :return: True, if the two nodes are adjacent; False, otherwise.
        """
        # if tail and head exist, look for the entry in the incidence list
        if super().isAdj(tail, head) == True:
            curr = self.inc[tail].getFirstRecord()
            while curr is not None:
                edge = curr.elem
                if edge.head == head:
                    return True
                curr = curr.next

        # else, return False
        return False

    def getAdj(self, nodeId):
        """
        Return all nodes adjacent to the one specified.
        :param nodeId: the node id.
        :return: the list of nodes adjacent to the one specified.
        """
        result = []
        curr = self.inc[nodeId].getFirstRecord()
        while curr is not None:
            result.append(curr.elem.head)
            curr = curr.next
        return result

    def deg(self, nodeId):
        """
        Return the node degree.
        :param nodeId: the node id.
        :return: the node degree.
        """
        if nodeId not in self.nodes:
            return 0
        else:
            return len(self.inc[nodeId])

    def print(self):
        """
        Print the graph.
        :return: void.
        """
        # if the incidence list is empty ...
        if self.isEmpty():
            print ("Incidence List: EMPTY")
            return

        # else ...
        print("Incidence Lists:")
        for inc_item in self.inc.items():
            print("{}:{}".format(inc_item[0], inc_item[1]))







