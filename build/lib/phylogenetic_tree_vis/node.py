import math
from enum import Enum
from typing import Callable


class NodeType(Enum):
    NODE = 1
    LEAF = 2
    CLADE = 3


class Node:
    def __init__(self, index):
        self.height = 0.0  # distance from the root
        self.length = 0.0  # distance from the parent node
        self.parent: Node = None
        self.children = []
        self.name = None
        self.traits = {}
        self.index = index
        self.y = None
        self.childHeight = None
        self.child_max = None
        self.child_min = None
        self.time = None
        self.location = None

    def node_type(self):
        return NodeType.NODE

    def is_leaf(self):
        return False

    def is_node(self):
        return True

    # todo: is_leafLike

    def to_string(self):
        return self.index

    def initialize_height(self, time_info):

        self.height = self.parent.height + self.length if self.parent is not None else self.length
        time_info['min_time'] = min(self.time, time_info['min_time']) \
            if time_info['min_time'] is not None and self.time is not None else self.time
        time_info['max_time'] = max(self.time, time_info['max_time']) \
            if time_info['max_time'] is not None and self.time is not None else self.time
        for child in self.children:
            child.initialize_height(time_info)

    def initialize_width(self):
        sum = 0.0
        try:
            for child in self.children:
                if child.is_node():
                    child.initialize_width()
                sum += child.y
            sum /= float(len(self.children))
            self.y = sum
            self.child_max = max([item.y for item in self.children])
            self.child_min = min([item.y for item in self.children])
        except Exception:
            print(self.name)

    def generate_json(self, time_version, base, span, span_record):
        temp_time = self.time if self.time is not None else base
        x_ref = temp_time - base if time_version else self.height - base
        ndx = math.ceil(x_ref * 20 / span)
        span_record[ndx] += 1
        return {
            'height': self.height,  # distance from the root
            'length': self.length,  # distance from the parent node
            'parent': self.parent.index,
            'children': list(map(lambda x: getattr(x, 'index'), self.children)),
            'name': self.name,
            'traits': self.traits,
            'index': self.index,
            'location': self.location,
            'time': self.time,
            'x_ref': x_ref
        }


class Leaf:
    def __init__(self, index, name):
        self.height = 0.0  # distance from the root
        self.length = 0.0  # distance from the parent node
        self.parent = None
        self.name = name
        self.traits = {}
        self.index = index
        self.y = None
        self.time = None
        self.location = None

    def node_type(self):
        return NodeType.LEAF

    def is_leaf(self):
        return True

    def is_node(self):
        return False

    # todo: is_leafLike

    def to_string(self):
        return self.name

    def initialize_height(self, time_info):
        self.height = self.parent.height + self.length if self.parent is not None else self.length
        # print(self.height)
        time_info['min_time'] = min(self.time, time_info['min_time']) \
            if time_info['min_time'] is not None and self.time is not None else time_info['min_time']
        time_info['max_time'] = max(self.time, time_info['max_time']) \
            if time_info['max_time'] is not None and self.time is not None else time_info['max_time']

    def generate_json(self, time_version, base, span, span_record):
        temp_time = self.time if self.time is not None else 0.0
        x_ref = temp_time - base if time_version else self.height - base
        ndx = math.ceil(x_ref * 20 / span)
        span_record[ndx] += 1
        return {
            'height': self.height,  # distance from the root
            'length': self.length,  # distance from the parent node
            'parent': self.parent.index,
            'children': [],
            'name': self.name,
            'traits': self.traits,
            'index': self.index,
            'location': self.location,
            'time': self.time,
            'x_ref': x_ref
        }
