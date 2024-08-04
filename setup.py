import json
from setuptools import setup, find_packages
from pathlib import Path

here = Path(__file__).parent
# with open('package.json') as f:
#     package = json.load(f)
long_description = (here / 'README.md').read_text()


# package_name = package["name"].replace(" ", "_").replace("-", "_")
setup(
    name="phylogenetic_tree_vis",
    version="0.0.1",
    author="qwerame",
    packages=find_packages(),#[package_name, 'py_files'],
    include_package_data=True,
    package_data={
        'phylogenetic_tree_vis': ['phylogenetic_tree_vis_comp/*.json'],
    },
    description="Project Description",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=['dash>=2.0.0', 'phylogenetic-tree-vis-comp==0.0.1'],
    classifiers = [
        'Framework :: Dash',
    ],    
)
