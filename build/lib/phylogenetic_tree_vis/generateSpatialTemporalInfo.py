from typing import Union, Callable

from .tree import Tree
from .node import Node, Leaf
from .transTree import TransTree, TransNode
import json


def generate_spatial_temporal_info(tree: Tree):
    cur_node = tree.root

    edges = []
    nodes_detail = {}
    nodes_map = {}
    time_info = {
        "start_time": None,
        "end_time": None
    }

    trans_tree = TransTree()

    location_root = cur_node.location

    # todo: time standardize
    time_root = cur_node.time # time_attr(cur_node) if isinstance(time_attr, Callable) else cur_node.traits.get(time_attr, cur_node.height)
        # cur_node.traits.get(time_attr, cur_node.height))

    if location_root is not None:
        id = "0"
        nodes_detail[location_root] = {
            "id": id,
            "time_list": [time_root],
            "first_time": time_root
        }
        nodes_map[id] = location_root
        trans_tree.add_node(id="0", start_time=None, end_time=None, source=None, target=None)
    traverse_tree(cur_node, edges, nodes_detail, time_info, trans_tree, nodes_map)

    # file_path = 'output_node.json'
    # with open(file_path, 'w') as json_file:
    #     nodes_info = {
    #         "nodes": nodes_detail,
    #         "time_info": time_info,
    #         "nodes_map": nodes_map,
    #         "time_axis": True # if time_attr is not None else False
    #     }
    #     json.dump(nodes_info, json_file, indent=4)

    # for index, edge in enumerate(edges):
    #     edge['id'] = index
    #
    # file_path = 'output_edge.json'
    # with open(file_path, 'w') as json_file:
    #     json.dump(edges, json_file, indent=4)

    new_edges = trans_tree.generate_json()
    # trans_tree.generate_leaves()

    nodes_info = {
        "nodes": nodes_detail,
        "time_info": time_info,
        "nodes_map": nodes_map,
        "time_axis": True  # if time_attr is not None else False
    }
    return {
        'edges': new_edges,
        'nodes': nodes_info
    }

def traverse_tree(node: Union[Node, Leaf], edges, nodes_detail, time_info, trans_tree,
                  nodes_map):
    if not node.is_node():
        return

    location_parent = node.location #node.traits.get(location_attr)
    # todo: time standardize
    time_parent = node.time #traits.get(time_attr, node.parent.height)
    index_source = node.index
    # node_detail = nodes_detail.get(location)

    if node.children is not None and len(node.children) > 0:
        for node_child in node.children:
            index_target = node_child.index
            location_child = node_child.location # node_child.traits.get(location_attr)
            time_child = node_child.time #node_child.traits.get(time_attr, node_child.height)
            node_detail = nodes_detail.get(location_child)
            time_info["start_time"] = time_child if time_info["start_time"] is None \
                else min(time_info["start_time"], time_child)
            time_info["end_time"] = time_child if time_info["end_time"] is None \
                else max(time_info["end_time"], time_child)
            if node_detail is None and location_child is not None:
                index = len(nodes_detail.keys())
                id = str(index)
                node_detail = {
                    "id": id,
                    "time_list": [time_child],
                    "first_time": time_child
                }
                nodes_detail[location_child] = node_detail
                nodes_map[id] = location_child

            elif location_child is not None:
                node_detail["time_list"].append(time_child)
                node_detail["first_time"] = min(time_child, node_detail["first_time"])
                nodes_detail[location_child] = node_detail

            cur_node = trans_tree.cur_node
            if location_parent is not None and location_child is not None and location_parent != location_child:
                id_child = nodes_detail.get(location_child).get('id')
                id_parent = nodes_detail.get(location_parent).get('id')
                edges.append({
                    "source": id_parent,
                    "target": id_child,
                    "start_time": time_parent,
                    "end_time": time_child
                })
                trans_tree.add_node(id=id_child, start_time=time_parent, end_time=time_child,
                                    source=index_source, target=index_target)

            elif location_parent is None and location_child is not None:
                id_child = nodes_detail.get(location_child).get('id')
                trans_tree.add_subtree(id=id_child)

            traverse_tree(node_child, edges, nodes_detail, time_info, trans_tree, nodes_map)
            trans_tree.return_previous_node(cur_node)
