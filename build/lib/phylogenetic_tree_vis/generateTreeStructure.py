import json
from typing import Union
from .tree import Tree
from .node import Node, Leaf


def generate_json_nodes(node: Union[Node, Leaf], nodes_list, time_version, base, span, span_record):

    nodes_list[node.index] = node.generate_json(time_version, base, span, span_record)
    if not isinstance(node, Leaf):
        for child in node.children:
            generate_json_nodes(child, nodes_list, time_version, base, span, span_record)


def generate_tree_structure(tree: Tree, time_version):
    leaves = list(map(lambda x: getattr(x, 'index'), tree.leaves))

    tree.initialize_height(time_version)
    tree_info = {
        'root': tree.root.index,
        'xSpan': tree.xSpan,
        'ySpan': tree.ySpan,
        'base': tree.base
    }
    nodes = {}
    span_record = [0] * 21
    # print(tree.xSpan)
    generate_json_nodes(tree.root, nodes, time_version, tree.base, tree.xSpan, span_record)
    max_ref = (max(span_record) + 49)//50 * 50
    # print(max_ref)
    tree_json = {
        'tree_info': tree_info,
        'leaves': leaves,
        'nodes': nodes,
        'span_record': [[i, span_record[i]] for i in range(0, len(span_record))],
        'max_ref': max_ref
    }
    return tree_json
    # file_path = 'output_tree.json'
    # with open(file_path, 'w') as json_file:
    #     json.dump(tree_json, json_file, indent=4)
