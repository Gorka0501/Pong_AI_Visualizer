import pygame as py
from neat.graphs import feed_forward_layers
from neat.nn import FeedForwardNetwork
from neat.six_util import itervalues

from .Connection import Connection
from .Node import Node
from Pong.Options import *

py.init()


class NeuralNetwork(FeedForwardNetwork):
    def __init__(self, inputs, outputs, node_evals, layers, left=True):
        super().__init__(inputs, outputs, node_evals)
        self.left = left
        self.layers = self.get_full_layers(layers)
        self.nodes, self.connections = self.get_nodes()

    def draw(self, win):
        if self.left:
            py.draw.rect(win, BLACK, py.Rect(WIDTH, 0, 500, HEIGHT/2))
        else:
            py.draw.rect(win, BLACK, py.Rect(WIDTH, HEIGHT/2, 500, HEIGHT))
        max_layer = len(self.layers)
        node_width = 500 / max_layer
        inic_width = WIDTH + (node_width / 2)
        node_max_height = (HEIGHT / 2) - 100

        layers_ocup = [0] * len(self.layers)

        for key in self.nodes:
            x = inic_width + (node_width * self.nodes[key].layer)
            node_height = (node_max_height / len(self.layers[self.nodes[key].layer]))
            if self.left:
                y = 100 + (node_height * layers_ocup[self.nodes[key].layer] + (node_height / 2))
            else:
                y = HEIGHT / 2 + 100 + (node_height * layers_ocup[self.nodes[key].layer] + (node_height / 2))
            layers_ocup[self.nodes[key].layer] += 1

            self.nodes[key].draw(win, node_width / 5, node_height, x, y)

        for con in self.connections:
            con.draw(win, (self.nodes[con.key[1]].x + self.nodes[con.key[1]].size, self.nodes[con.key[1]].y),
                     (self.nodes[con.key[0]].x -
                      self.nodes[con.key[0]].size, self.nodes[con.key[0]].y))

    def get_full_layers(self, layers):
        new_layers = []
        i_nodes = set()
        o_nodes = set()
        for i in self.input_nodes:
            i_nodes.add(i)

        new_layers.append(i_nodes)
        n_layer = 0
        for layer in layers:
            nodes = set()
            for node in layer:
                if node not in self.output_nodes:
                    nodes.add(node)
                else:
                    o_nodes.add(node)
            if not n_layer == len(layers) - 1:
                new_layers.append(nodes)
            n_layer += 1

        new_layers.append(o_nodes)
        return new_layers

    def get_nodes(self):
        ord_nodes = {}
        for node in self.node_evals:
            ord_nodes[node[0]] = node
        nodes = {}
        connections = []
        nlayer = 0
        for layer in self.layers:
            for node in layer:
                if nlayer == 0:
                    nodes[node] = Node(node, nlayer)
                else:
                    nodes[node] = Node(ord_nodes[node], nlayer)
                    for con in ord_nodes[node][5]:
                        connections.append(Connection((ord_nodes[node][0], con[0]), con[1]))
            nlayer += 1
        return nodes, connections

    def update(self):
        for key in self.values:
            if key in self.nodes.keys():
                self.nodes[key].value = self.values[key]
        for con in self.connections:
            con.update(self.values[con.key[1]])

    @staticmethod
    def create(genome, config, left=True):
        """ Receives a genome and returns its phenotype (a FeedForwardNetwork). """

        # Gather expressed connections.
        connections = [cg.key for cg in itervalues(genome.connections) if cg.enabled]
        layers = feed_forward_layers(config.genome_config.input_keys, config.genome_config.output_keys, connections)
        nnodes = 0
        node_evals = [0] * nnodes
        for layer in layers:
            for node in layer:
                inputs = []
                node_expr = []  # currently unused
                for conn_key in connections:
                    inode, onode = conn_key
                    if onode == node:
                        cg = genome.connections[conn_key]
                        inputs.append((inode, cg.weight))
                        node_expr.append("v[{}] * {:.7e}".format(inode, cg.weight))

                ng = genome.nodes[node]
                aggregation_function = config.genome_config.aggregation_function_defs.get(ng.aggregation)
                activation_function = config.genome_config.activation_defs.get(ng.activation)
                node_evals.append((node, activation_function, aggregation_function, ng.bias, ng.response, inputs))

        return NeuralNetwork(config.genome_config.input_keys, config.genome_config.output_keys, node_evals,
                             layers, left)
