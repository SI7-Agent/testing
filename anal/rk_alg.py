class graph(object):
    def __init__(self):
        self.Nodes = set()
        self.AdjList = dict()

    def add_node(self, node):
        if node in self.Nodes:
            raise Exception("Node " + node + " is already present in the graph.")
        else:
            self.Nodes.add(node)
            self.AdjList[node] = set()

    def add_edge(self, nd1, nd2):
        if nd1 not in self.Nodes:
            raise Exception("Node " + nd1 + " is not present in the graph.")
        if nd2 not in self.Nodes:
            raise Exception("Node " + nd2 + " is not present in the graph.")
        if nd1 not in self.AdjList.keys():
            self.AdjList[nd1] = set()
            self.AdjList[nd1].add(nd2)
        else:
            self.AdjList[nd1].add(nd2)
        if nd2 not in self.AdjList.keys():
            self.AdjList[nd2] = set()
            self.AdjList[nd2].add(nd1)
        else:
            self.AdjList[nd2].add(nd1)

    def get_edge_set(self):
        Edges = set()
        for nd1 in self.Nodes:
            N = self.get_node_neighbors(nd1)
            for nd2 in N:
                if (nd2, nd1) not in Edges:
                    Edges.add((nd1, nd2))
        return Edges

    def number_of_nodes(self):
        return len(self.Nodes)

    def number_of_edges(self):
        num_edg = 0.0
        for key in self.AdjList.keys():
            num_edg = num_edg + (float(len(self.AdjList[key])) / 2)
        return int(num_edg)

    def are_adjacent(self, nd1, nd2):
        if nd1 not in self.Nodes:
            raise Exception()
        if nd2 not in self.Nodes:
            raise Exception()
        if nd2 in self.AdjList[nd1]:
            return True
        else:
            return False

    def get_node_neighbors(self, nd):
        return self.AdjList[nd]

    def find_all_cliques(self):
        Cliques = []
        Stack = []
        nd = None
        disc_num = len(self.Nodes)
        search_node = (set(), set(self.Nodes), set(), nd, disc_num)
        Stack.append(search_node)
        while len(Stack) != 0:
            (c_compsub, c_candidates, c_not, c_nd, c_disc_num) = Stack.pop()
            if not len(c_candidates) and c_compsub not in Cliques:
                Cliques.append(c_compsub)
                continue
            for u in list(c_candidates):
                if (c_nd is None) or (not self.are_adjacent(u, c_nd)):
                    c_candidates.remove(u)
                    Nu = self.get_node_neighbors(u)
                    new_compsub = set(c_compsub)
                    new_compsub.add(u)
                    new_candidates = set(c_candidates.intersection(Nu))
                    new_not = set(c_not.intersection(Nu))
                    if c_nd is not None:
                        if c_nd in new_not:
                            new_disc_num = c_disc_num - 1
                            if new_disc_num > 0:
                                new_search_node = (new_compsub, new_candidates, new_not, c_nd, new_disc_num)
                                Stack.append(new_search_node)
                        else:
                            new_disc_num = len(self.Nodes)
                            new_nd = c_nd
                            for cand_nd in new_not:
                                cand_disc_num = len(new_candidates) - len(new_candidates.intersection(self.get_node_neighbors(cand_nd)))
                                if cand_disc_num < new_disc_num:
                                    new_disc_num = cand_disc_num
                                    new_nd = cand_nd
                            new_search_node = (new_compsub, new_candidates, new_not, new_nd, new_disc_num)
                            Stack.append(new_search_node)
                    else:
                        new_search_node = (new_compsub, new_candidates, new_not, c_nd, c_disc_num)
                        Stack.append(new_search_node)
                    c_not.add(u)
                    new_disc_num = 0
                    for x in c_candidates:
                        if not self.are_adjacent(x, u):
                            new_disc_num += 1
                    if (new_disc_num < c_disc_num) and (new_disc_num > 0):
                        new1_search_node = (c_compsub, c_candidates, c_not, u, new_disc_num)
                        Stack.append(new1_search_node)
                    else:
                        new1_search_node = (c_compsub, c_candidates, c_not, c_nd, c_disc_num)
                        Stack.append(new1_search_node)
        while set() in Cliques:
            Cliques.pop(Cliques.index(set()))
        return Cliques


test = graph()
test.add_node(0)
test.add_node(1)
test.add_node(2)
test.add_node(3)

test.add_edge(0, 1)
test.add_edge(0, 2)
test.add_edge(0, 3)
test.add_edge(2, 3)
test.add_edge(2, 1)
test.add_edge(1, 3)

print(test.find_all_cliques())
