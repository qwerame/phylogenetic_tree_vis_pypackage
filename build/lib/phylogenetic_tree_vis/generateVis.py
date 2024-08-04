


from dash import Dash, callback, html, Input, Output

import phylogenetic_tree_vis_comp
from .generateSpatialTemporalInfo import generate_spatial_temporal_info
from .generateTreeStructure import generate_tree_structure


def vis_info(tree, time_version, location_constraints):
    """
       This function is used for uploading geojson file.

       Args:
       tree (Tree): The return value of load_nexus api.
       time_version (boolean): Whether the specified time version should be used, default False.
       translation (string): The location of the csv file containing information about Chinese version of the location names.

       Returns:
       Constraints: The constraints info to be used in vis_info.
    """

    treeInfo = generate_tree_structure(tree=tree, time_version=time_version)
    transInfo = generate_spatial_temporal_info(tree=tree)

    app = Dash(__name__)

    app.layout = html.Div([
        phylogenetic_tree_vis_comp.PhylogeneticTreeVisComp(
            id='input',
            value='my-value',
            label='my-label',
            tree=treeInfo,
            raw_nodes=transInfo['nodes'],
            raw_links=transInfo['edges'],
            gridConstraints=location_constraints
        ),
        # html.Div(id='output')
    ])

    app.run_server(debug=True)