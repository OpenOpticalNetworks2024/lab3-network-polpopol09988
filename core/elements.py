import json
from core.parameters import c
import matplotlib.pyplot as plt

class Signal_information(object):
    def __init__(self, signal_power, path):
        self._signal_power = signal_power
        self._noise_power = 0.0
        self._latency = 0.0
        self._path = path if path is not None else []

    @property
    def signal_power(self):
        return self._signal_power

    def update_signal_power(self,increment):
        self._signal_power += increment

    @property
    def noise_power(self):
        return self._noise_power

    @noise_power.setter
    def noise_power(self, value):
        self._noise_power = value

    def update_noise_power(self,increment):
        self._noise_power += increment

    @property
    def latency(self):
        return self._latency

    @latency.setter
    def latency(self,value):
        self._latency = value

    def update_latency(self,increment):
        self.latency += increment

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self,stringa):
        self._path = stringa

    def update_path(self):
        self._path = self._path[1:len(self._path)]


class Node(object):
    def __init__(self,nodo_diz,label):
        self._label = label
        self._position = nodo_diz["position"]
        self._connected_nodes = nodo_diz["connected_nodes"]
        self._successive = dict()

    @property
    def label(self):
        return self._label

    @property
    def position(self):
        return self._position

    @property
    def connected_nodes(self):
        return self._connected_nodes

    @property
    def successive(self):
        return self._successive

    @successive.setter
    def successive(self,line):
        self._successive = line

    def propagate(self,signal):
        if(len(signal.path)>=2):
            nextline = signal.path[0:2]
            signal.update_path()
            self.successive[nextline].propagate(signal)


class Line(object):
    def __init__(self, label, length):
        self._label = label
        self._length = length
        self._successive = dict()

    @property
    def label(self):
        return self._label

    @property
    def length(self):
        return self._length

    @property
    def successive(self):
        return self._successive

    @successive.setter
    def successive(self, node):
        self._successive = node

    # 2/3*c = l/t ->  t = l*3/2*c
    def latency_generation(self):
        return self._length*3/2/3e8

    def noise_generation(self, signal_power):
        return 1e-9*signal_power*self._length

    def propagate(self,signal):
        signal.update_noise_power(self.noise_generation(signal.noise_power))
        signal.update_latency(self.latency_generation())
        self.successive[signal.path[0]].propagate(signal)


class Network(object):
    def __init__(self,infile):
        self._nodes = dict()
        self._lines = dict()
        with open(infile, mode="r", encoding="utf-8") as read_file:
            a = json.load(read_file)
        for el in a:
            if el not in self._nodes:
                self._nodes[el] = Node(a[el],el)
        for nodo in a:
            for nextnodo in a[nodo]["connected_nodes"]:
                linelabel = nodo+nextnodo
                if linelabel not in self._lines:
                    deltax = a[nodo]["position"][0]-a[nextnodo]["position"][0]
                    deltay = a[nodo]["position"][1]-a[nextnodo]["position"][1]
                    length = (deltax**2+deltay**2)**(1/2)
                    self._lines[linelabel] = Line(linelabel,length)


    @property
    def nodes(self):
        return self._nodes

    @property
    def lines(self):
        return self._lines

    def draw(self):
        for node in self.nodes:
            x = self.nodes[node].position[0]
            y = self.nodes[node].position[1]
            plt.scatter(x,y)
            plt.text(x, y, node, fontsize=12, verticalalignment='bottom', horizontalalignment='right')
            for riga in self.nodes[node].connected_nodes:
                x2 = self.nodes[riga].position[0]
                y2 = self.nodes[riga].position[1]
                plt.plot([x,x2],[y,y2],'k')


        plt.show()

    # find_paths: given two node labels, returns all paths that connect the 2 nodes
    # as a list of node labels. Admissible path only if cross any node at most once
    # def find_paths(self, label1, label2):
    #     paths = list()
    #     tmp = label1
    #     for el1 in self.nodes[label1].connected_nodes:
    #         tmp = tmp+el1
    #         if (el1 == label2) & (tmp not in paths):
    #             paths.append(tmp)
    #         else:
    #             for el2 in self.nodes[el1].connected_nodes:
    #                 if el2 not in tmp:
    #                     tmp = tmp+el2
    #                     if (el2 == label2) & (tmp not in paths):
    #                         paths.append(tmp)
    #                     else:
    #                         for el3 in self.nodes[el2].connected_nodes:
    #                             if el3 not in tmp:
    #                                 tmp = tmp+el3
    #                                 if (el3 == label2) & (tmp not in paths):
    #                                     paths.append(tmp)
    #                                 else:
    #                                     for el4 in self.nodes[el3].connected_nodes:
    #                                         if el4 not in tmp:
    #                                             tmp = tmp+el4
    #                                             if (el4 == label2) & (tmp not in paths):
    #                                                 paths.append(tmp)
    #                                             else:
    #                                                 for el5 in self.nodes[el4].connected_nodes:
    #                                                     if el5 not in tmp:
    #                                                         tmp = tmp+el5
    #                                                         if (el5 == label2) & (tmp not in paths):
    #                                                             paths.append(tmp)
    #                                                         tmp=tmp[:-1]
    #                                             tmp = tmp[:-1]
    #                                 tmp = tmp[:-1]
    #                     tmp = tmp[:-1]
    #         tmp = tmp[:-1]
    #     return paths
    def find_paths(self, label1, label2, paths=list()):
        depth = len(label1)
        if depth > len(self.nodes):
            return
        else:
            for el in self.nodes[label1[-1]].connected_nodes:
                if el not in label1:
                    label1=label1+el
                    if(el == label2) & (label1 not in paths):
                        paths.append(label1)
                    else:
                        self.find_paths(label1,label2,paths)
                    label1 = label1[:-1]
        return paths


    # connect function set the successive attributes of all NEs as dicts
    # each node must have dict of lines and viceversa
    def connect(self):
        for line in self.lines:
            self.lines[line].successive[line[1]] = self.nodes[line[1]]
        for nodo in self.nodes:
            for line in self.lines:
                if line[0] == nodo:
                    self.nodes[nodo].successive[line]=self.lines[line]

    # propagate signal_information through path specified in it
    # and returns the modified spectral information
    def propagate(self, signal_information):
        self.nodes[signal_information.path[0]].propagate(signal_information)
