import json
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
from core.elements import Signal_information
from core.elements import Node
from core.elements import Line
from core.elements import Network

# Exercise Lab3: Network

ROOT = Path(__file__).parent.parent
INPUT_FOLDER = ROOT / 'resources'
file_input = INPUT_FOLDER / 'nodes.json'


# Load the Network from the JSON file, connect nodes and lines in Network.
# Then propagate a Signal Information object of 1mW in the network and save the results in a dataframe.
# Convert this dataframe in a csv file called 'weighted_path' and finally plot the network.
# Follow all the instructions in README.md file


a=Network(file_input)
a.connect()
for wl in a.lines:
    print(wl, a.lines[wl].length, a.lines[wl].successive)

for nodo in a.nodes:
    print(nodo, a.nodes[nodo].successive)

print(a.find_paths('D','B'))
a.draw()

