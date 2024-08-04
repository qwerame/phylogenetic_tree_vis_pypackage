import json


class TransNode:
    def __init__(self, id, start_time, end_time, parent, source, target):
        self.children = []
        self.start_time = start_time
        self.end_time = end_time
        self.id = id
        self.parent = parent
        self.children_set = set([id]) if id is not None else set()
        self.parent_set = set([id]) if id is not None else set()
        self.source = source
        self.target = target

    def generate_json(self, list):
        id_set = self.children_set.union(self.parent.parent_set)
        id_str = "+" + '+'.join(id_set) + "+"
        list.append({
            "source": self.parent.id,
            "target": self.id,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "id_str": id_str,
            "source_node_id": self.source,
            "target_node_id": self.target
        })
        for child in self.children:
            child.generate_json(list)

    def generate_subtree_json(self, list):
        for child in self.children:
            child.generate_json(list)

    def generate_leaves(self, leaves):
        if len(self.children) > 0:
            for child in self.children:
                child.generate_leaves(leaves)
        else:
            leaves.append(self)

    def generate_parent_set(self):
        parent_set = self.parent.parent_set
        self.parent_set.update(parent_set)
        for child in self.children:
            child.generate_parent_set()

    def update_children_set(self, new_set):
        self.children_set.update(new_set)


class TransTree:
    def __init__(self):
        self.root = TransNode(None, None, None, None, None, None)
        self.cur_node = self.root
        self.leaves = []

    def add_node(self, id, start_time, end_time, source, target):
        new_node = TransNode(id, start_time, end_time, self.cur_node, source, target)
        self.cur_node.children.append(new_node)
        self.cur_node = new_node

    def add_subtree(self, id):
        new_node = TransNode(id, None, None, self.root, None, None)
        self.root.children.append(new_node)
        self.cur_node = new_node

    def return_previous_node(self, node):
        self.cur_node = node

    def generate_json(self):
        json_list = []
        self.root.parent_set = set()
        self.root.children_set = set()
        self.generate_leaves()
        self.generate_sets()
        for subtree in self.root.children:
            subtree.generate_subtree_json(json_list)
            # print("one tree")

        for index, edge in enumerate(json_list):
            edge['id'] = index
        # file_path = 'output_edge2.json'
        # with open(file_path, 'w') as json_file:
        #     json.dump(json_list, json_file, indent=4)
        return json_list

    def generate_leaves(self):
        leaves = []
        self.root.generate_leaves(leaves)
        self.leaves = leaves
        # print(len(self.leaves))

    def generate_sets(self):
        for child in self.root.children:
            child.generate_parent_set()

        for leaf in self.leaves:
            index_node = leaf
            while index_node.parent is not None:
                index_node.parent.update_children_set(index_node.children_set)
                index_node = index_node.parent
