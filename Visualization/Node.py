import pygame as py

from Pong.Options import WHITE, OUTPUTS, NODE_FONT, BLACK, GREEN


class Node:
    def __init__(self, node, layer):
        self.y = None
        self.x = None
        self.size = None
        if type(node) == int:
            self.key = node
        else:
            self.key = node[0]
            self.act_func = node[1]
            self.agg_fuction = node[2]
            self.bias = node[3]
            self.response = node[4]
        self.layer = layer
        self.value = 0

    def draw(self, win, width, height, x, y):
        self.x = x
        self.y = y
        self.size = min(width, height)/2
        py.draw.circle(win, WHITE, (x, y), self.size)

        ID = NODE_FONT.render(str(round(self.value,2)), 1, GREEN)
        win.blit(ID, (x, y))


