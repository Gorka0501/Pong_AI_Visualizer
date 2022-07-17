import pygame as py
from neat.nn import FeedForwardNetwork

from .Connection import Connection
from .Node import Node
from Pong.Options import *

py.init()


class NeuralNetwork(FeedForwardNetwork):
    def __init__(self, inputs, outputs, node_evals, left=True):
        self.left = left
        super().__init__(inputs, outputs, node_evals)


    def draw(self, win):
        max_layer = len(self.layers)
        node_width = 500 / max_layer
        inic_width = WIDTH + (node_width/2)
        node_max_height = (HEIGHT / 2) - 100


        layers_ocup = [0] * len(self.layers)

        for key in self.nodes:
            x = inic_width + (node_width * self.nodes[key].layer)
            node_height = (node_max_height / self.layers[self.nodes[key].layer])
            if self.left:
                y = 100 + (node_height * layers_ocup[self.nodes[key].layer] + (node_height / 2))
            else:
                y = HEIGHT / 2 + 100 + (node_height * layers_ocup[self.nodes[key].layer] + (node_height / 2))
            layers_ocup[self.nodes[key].layer] += 1

            self.nodes[key].draw(win, node_width / 5, node_height, x, y)

        for con in self.connections:
            con.draw(win, (self.nodes[con.key[0]].x + self.nodes[con.key[0]].size, self.nodes[con.key[0]].y), (self.nodes[con.key[1]].x -
                                                                                                               self.nodes[con.key[1]].size, self.nodes[con.key[1]].y))

    def create(self, o_nodes, o_connections):
        nodes = {}
        connections = []
        layers = []
        max_layer = 0

        for key in o_connections:
            connections.append(Connection(o_connections[key]))
            for i in range(0, 2):
                if key[i] not in nodes.keys():
                    if key[i] < 0:
                        node = Node(key[i])
                    else:
                        node = Node(o_nodes[key[i]])
                    nodes[key[i]] = node
                    if not 0 <= key[i] < OUTPUTS:
                        layer = nodes[key[i]].calculate_layer(nodes[key[0]].layer)
                        max_layer = max(max_layer, layer)
                        if len(layers) <= layer:
                            layers.append(1)
                        else:
                            layers[layer] += 1

                elif i == 1 and not 0 <= key[i] < OUTPUTS:
                    if not len(layers) <= nodes[key[1]].layer:
                        layers[nodes[key[1]].layer] -= 1
                    layer = nodes[key[1]].calculate_layer(nodes[key[0]].layer)
                    max_layer = max(max_layer, layer)
                    if len(layers) <= layer:
                        layers.append(1)
                    else:
                        layers[layer] += 1

        for i in range(0, OUTPUTS):
            if i not in nodes.keys():
                node = Node(o_nodes[i])
                nodes[i] = node
            layer = nodes[i].calculate_layer(max_layer + 1)
            if len(layers) <= layer:
                layers.append(1)
            else:
                layers[layer] += 1

        max_layer += 2
        self.layers = layers

        return nodes, connections
