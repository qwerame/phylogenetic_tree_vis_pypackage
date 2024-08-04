from typing import Union, Callable
from .tree import Tree
from .node import Node, Leaf


import re

tipMap_format = r'([0-9]+) ([A-Za-z0-9|\/\-_.]+)'
start_format = r'tree [A-Za-z0-9|\/\-_.]+'
tip_format = r'(\(|,)([A-Za-z0-9|\/\-_.\']+)(\[)'
length_format = r'(;|\:-?\d+(\.\d+)?)'
node_length_format = r'(;|\:-?\d+(\.\d+)?)'
node_name_format = r'(\))([A-Za-z0-9|\/\-_.]+)(\[)'

def is_float(string):
    try:
        float_value = float(string)
        return True
    except ValueError:
        return False


def load_nexus(tree_path, time_attr, location_attr):
    """
       This function is used for uploading nexus file.

       Args:
       tree_path (string): The location of the nexus file.
       time_attr (string | func): The attr name indicating time or the func used for calculating time.
       location_attr (string): The attr name indicating location.

       Returns:
       Tree: The tree object to be used in vis_info.
    """
    phylo_tree = None
    if isinstance(tree_path, str):
        handle = open(tree_path, 'r')
    else:
        handle = tree_path

    translating = False
    tips = {}
    for line in handle:
        l = line.strip('\n')
        if translating:
            tip_map_item = re.match(tipMap_format, l)
            if tip_map_item is not None:
                tips[tip_map_item.group(1)] = tip_map_item.group(2)
            elif ';' in l:
                translating = False
            # todo: error
            # else:

        elif 'Translate' in l:
            translating = True

        elif re.search(start_format, l):
            treeString_start = l.index('(')
            phylo_tree = translate_nexus(l[treeString_start:], time_attr, location_attr)

        # todo: error
        # else:

    # phylo_tree.to_string()

    if isinstance(tree_path, str):
        handle.close()
    return phylo_tree


def translate_nexus(data, time_attr, location_attr):
    new_tree = Tree()
    index = 0
    previous_index = None
    while index < len(data) and index != previous_index:
        tip_info = re.match(tip_format, data[index: index + 1000])
        while tip_info is None and index < len(data):
            if data[index] == '(':
                new_tree.add_node(index=index)
            previous_index = index
            index += 1
            tip_info = re.match(tip_format, data[index: index + 1000])

        if index >= len(data):
            break

        if tip_info.group(1) == '(':
            new_tree.add_node(index=index)
        tip_name = tip_info.group(2)
        index += len(tip_info.group(0))
        annotation_start_index = index
        annotation_end_index = data[index: index + 10000].find(']')
        index += annotation_end_index + 1
        length_info = re.match(length_format, data[index: index + 1000])
        # todo:
        # if length_info is None:
        tip_length = float(length_info.group(0)[1:]) if length_info.group(0) is not None and is_float(
            length_info.group(0)[1:]) else 0.0
        leaf = new_tree.add_leaf(index=index, name=tip_name, length=tip_length)
        get_annotations(leaf, data[annotation_start_index: annotation_start_index + annotation_end_index])
        leaf.location = leaf.traits.get(location_attr)
        leaf.time = time_attr(leaf) if isinstance(time_attr, Callable) else leaf.traits.get(time_attr)
        previous_index = index
        index += len(length_info.group(0))

        while index < len(data) and data[index] == ')':
            node_name = re.match(node_name_format, data[index: index + 1000])
            if node_name is not None:
                new_tree.curNode.name = node_name.group(2)
                index += len(node_name.group(0))
                annotation_start_index = index
                annotation_end_index = data[index: index + 10000].find(']')
                get_annotations(new_tree.curNode,
                                data[annotation_start_index: annotation_start_index + annotation_end_index])
                new_tree.curNode.location = new_tree.curNode.traits.get(location_attr)
                new_tree.curNode.time = time_attr(new_tree.curNode) if isinstance(time_attr, Callable) \
                    else new_tree.curNode.traits.get(time_attr)
                index += annotation_end_index + 1

            if data[index:].startswith(")["):
                index += 2
                annotation_start_index = index
                annotation_end_index = data[index: index + 10000].find(']')
                get_annotations(new_tree.curNode,
                                data[annotation_start_index: annotation_start_index + annotation_end_index])
                new_tree.curNode.location = new_tree.curNode.traits.get(location_attr)
                new_tree.curNode.time = time_attr(new_tree.curNode) if isinstance(time_attr, Callable) \
                    else new_tree.curNode.traits.get(time_attr)
                index += annotation_end_index + 1

            node_length = re.match(node_length_format, data[index: index + 1000])
            if node_length is None:
                print(index)
            else:
                new_tree.curNode.length = float(node_length.group(0)[1:]) if node_length.group(
                    0) is not None and is_float(node_length.group(0)[1:]) else 0.0
                new_tree.curNode = new_tree.curNode.parent
                previous_index = index
                index += len(node_length.group(0))

    return new_tree


def get_annotations(node: Union[Node, Leaf], annotation_data):
    numeric_format = r'(,|&)([A-Za-z\_\.0-9\%]+)(=)([0-9\-Ee\.]+)'
    string_format = r'(,|&)([A-Za-z\_\.0-9\%]+)(=)(["|\']*[A-Za-z\_0-9\.\+ :\/\(\)\&\-]+[\"|\']*)'
    range_format = r'(,|&)([A-Za-z\_\.0-9\%]+)(=\{)([0-9\-Ee\.]+)(,)([0-9\-Ee\.]+)'

    numerics = re.findall(numeric_format, annotation_data)
    strings = re.findall(string_format, annotation_data)
    pure_strings = [item for item in strings if item not in numerics]
    ranges = re.findall(range_format, annotation_data)

    for vals in pure_strings:
        attr_name = vals[1]
        attr_value = vals[3].strip('"')
        node.traits[attr_name] = attr_value

    for vals in numerics:
        attr_name = vals[1]
        attr_value = vals[3]
        if attr_value.replace('E', '', 1).replace('e', '', 1).replace('-', '', 1).replace('.', '', 1).isdigit():
            node.traits[attr_name] = float(attr_value)

    for vals in ranges:
        attr_name = vals[1]
        attr_value_low = vals[3]
        attr_value_high = vals[5]
        if (attr_value_low.replace('E', '', 1).replace('e', '', 1).replace('-', '', 1).replace('.', '', 1).isdigit()
                and attr_value_high.replace('E', '', 1).replace('e', '', 1).replace('-', '', 1).replace('.', '', 1).isdigit()):
            node.traits[attr_name] = (float(attr_value_low), float(attr_value_high))
