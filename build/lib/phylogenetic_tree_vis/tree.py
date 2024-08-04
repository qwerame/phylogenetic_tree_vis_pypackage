from .node import Node, Leaf, NodeType


class Tree:
    def __init__(self):
        self.root = None
        self.curNode = Node(index=0)
        self.nodeList = []  # all nodes and leafs and clades
        self.nameMap = None  # when 'translate' part is contained in a NEXUS file
        self.ySpan = 0.0  # related to the total number of the leafLike nodes
        self.xSpan = 0.0  # related to the max height of the leafLike nodes
        self.base = 0.0
        self.internalNodes = []
        self.leaves = []

    def add_node(self, index):
        # print(index)
        new_node = Node(index=index)
        if self.root is None:
            self.root = new_node

        assert self.curNode.is_node(), 'Attempted to add a child to a non-node object!!!'
        new_node.parent = self.curNode
        self.curNode.children.append(new_node)
        self.curNode = new_node
        self.nodeList.append(new_node)
        self.internalNodes.append(new_node)

    def add_leaf(self, index, name='', length=0.0):
        # print(length)
        new_leaf = Leaf(index=index, name=name)
        new_leaf.name = name
        new_leaf.length = length
        if self.root is None:
            self.root = new_leaf

        assert self.curNode.is_node(), 'Attempted to add a child to a non-node object!!!'
        new_leaf.parent = self.curNode
        self.curNode.children.append(new_leaf)
        self.nodeList.append(new_leaf)
        self.leaves.append(new_leaf)
        return new_leaf

    def to_string(self):
        for item in self.nodeList:
            attrs = " ".join(item.traits.keys())
            print(f"{item.name} {attrs}")
            # print(f"{item.length} {item.height} {item.name} {attrs[0]}")

    def initialize_height(self, time_version):
        time_span_info = {
            'min_time': float('inf'),
            'max_time': 0.0
        }
        self.root.initialize_height(time_span_info)
        try:
            self.xSpan = max(node.height for node in self.leaves) if time_version is False else \
                time_span_info['max_time'] - time_span_info['min_time']
            if time_version:
                self.base = time_span_info['min_time']
        except Exception as e:
            print(self.leaves)

    def initialize_width(self):
        for index, leaf in enumerate(self.leaves):
            leaf.y = len(self.leaves) - index
        self.ySpan = len(self.leaves)
        root = self.root
        root.initialize_width()
