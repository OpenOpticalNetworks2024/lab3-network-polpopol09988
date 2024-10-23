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
OUTPUT_FOLDER = ROOT / 'results'
file_input = INPUT_FOLDER / 'nodes.json'
file_output = OUTPUT_FOLDER / 'out.csv'


# Load the Network from the JSON file, connect nodes and lines in Network.
# Then propagate a Signal Information object of 1mW in the network and save the results in a dataframe.
# Convert this dataframe in a csv file called 'weighted_path' and finally plot the network.
# Follow all the instructions in README.md file


a=Network(file_input)
a.connect()
#prove varie in fase di debug
#for wl in a.lines:
    #print(wl, a.lines[wl].length, a.lines[wl].successive)

#for nodo in a.nodes:
    #print(nodo, a.nodes[nodo].successive)

#print(a.find_paths('D','B'))

a.draw()

#creo possible couples
lista_nodi = a.nodes.keys()
lista_percorsi = list()
for nodo in lista_nodi:
    for nodo2 in lista_nodi:
        if nodo != nodo2:
            tmp = nodo+nodo2
            lista_percorsi.append(tmp)

pathstring = list()
latencystring = list()
noisestring = list()
snrstring = list()
stringa = str()
for percorso in lista_percorsi:
    paths = a.find_paths(percorso[0], percorso[1])
    for path in paths:
        stringa = str()
        s = Signal_information(1e-3, path)
        for letter in path[:-1]:
            pass
            stringa = stringa+letter+"->"
            #print(letter+'->', end="")
        #print(path[-1], end="")
        stringa = stringa+path[-1]
        pathstring.append(stringa)
        a.propagate(s)
        #print(", latenza: " + str(s.latency), end="")
        latencystring.append(str(s.latency))
        #print(", noise: " + str(s.noise_power), end="")
        noisestring.append(str(s.noise_power))
        snr = 10 * np.log10(s.signal_power/s.noise_power)
        #print(", SNR: " + str(snr))
        snrstring.append(str(snr))
#manca solo il pandas
data = {
    "path": pathstring,
    "latency": latencystring,
    "noise_power": noisestring,
    "SNR": snrstring
}
df = pd.DataFrame(data)
df.to_csv(file_output, index=False)

