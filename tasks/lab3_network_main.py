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
#for wl in a.lines:
    #print(wl, a.lines[wl].length, a.lines[wl].successive)

#for nodo in a.nodes:
    #print(nodo, a.nodes[nodo].successive)

#print(a.find_paths('D','B'))

#a.draw()

#creo possible couples
lista_nodi = a.nodes.keys()
lista_percorsi = list()
for nodo in lista_nodi:
    for nodo2 in lista_nodi:
        if nodo != nodo2:
            tmp = nodo+nodo2
            lista_percorsi.append(tmp)


for percorso in lista_percorsi:
    paths = a.find_paths(percorso[0], percorso[1])
    for path in paths:
        s = Signal_information(1e-3,path)
        for letter in path[:-1]:
            pass
            print(letter+'->', end="")
        print(path[-1], end="")
        a.propagate(s)
        print(", latenza: "+ str(s.latency), end ="")
        print(", noise: "+ str(s.noise_power), end ="")
        snr = 10 * np.log10(s.signal_power/s.noise_power)
        print(", SNR: "+ str(snr))

#manca solo il pandas
