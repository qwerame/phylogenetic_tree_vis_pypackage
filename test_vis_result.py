from phylogenetic_tree_vis import load_nexus, generate_constraints, vis_info

# PEDV数据集可视化效果
# time_func = lambda node: 2019.95342466 - node.traits.get('height') if 'height' in node.traits else None
# tree = load_nexus('input_data/China/PEDV_China.MCC.nexus', time_attr=time_func, location_attr="location")
# location_constraints = generate_constraints("input_data/China/China_2.geojson", "name",
#                                            "input_data/China/translation.csv")
# vis_info(tree=tree, time_version=False, location_constraints=location_constraints)


# ebola数据集可视化效果
# tree = load_nexus('input_data/Africa/ebola.nexus', location_attr="division", time_attr="num_date")
# location_constraints = generate_constraints("input_data/Africa/africa.json", "NAME_2",)
# vis_info(tree=tree, time_version=False, location_constraints=location_constraints)


# mumps数据集可视化效果
tree = load_nexus('input_data/northAmerica/mumps.nexus', location_attr="division", time_attr="num_date")
location_constraints = generate_constraints("input_data/northAmerica/northAmerica.json", "name",)
vis_info(tree=tree, time_version=False, location_constraints=location_constraints)
