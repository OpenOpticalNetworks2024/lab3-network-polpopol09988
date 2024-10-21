import json

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
    def __init__(self,dict,nodo):
        self._label = nodo
        self._position = dict[nodo]["position"]
        self._connected_nodes = dict[nodo]["connected_nodes"]
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
    def successive(self,nodo):
        self._successive = nodo

    def propagate(self,signal):
        signal.update_path()
        newpath = signal.path()
        if newpath != "":
            nextnode = newpath[0]
            self.propagate(nextnode)


class Line(object):
    def __init__(self):
        pass

    @property
    def label(self):
        pass

    @property
    def length(self):
        pass

    @property
    def successive(self):
        pass

    @successive.setter
    def successive(self):
        pass

    def latency_generation(self):
        pass

    def noise_generation(self):
        pass

    def propagate(self):
        pass


class Network(object):
    def __init__(self):
        pass

    @property
    def nodes(self):
        pass

    @property
    def lines(self):
        pass

    def draw(self):
        pass

    # find_paths: given two node labels, returns all paths that connect the 2 nodes
    # as a list of node labels. Admissible path only if cross any node at most once
    def find_paths(self, label1, label2):
        pass

    # connect function set the successive attributes of all NEs as dicts
    # each node must have dict of lines and viceversa
    def connect(self):
        pass

    # propagate signal_information through path specified in it
    # and returns the modified spectral information
    def propagate(self, signal_information):
        pass
