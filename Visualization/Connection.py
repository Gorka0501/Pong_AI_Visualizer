import pygame as py

from Pong.Options import *


class Connection:
    def __init__(self, key, weight):
        self.key = key
        self.weight = weight
        self.value = weight

    def draw(self, win, place1, place2):
        if self.value < 0:
            color = RED
        else:
            color = GREEN
        py.draw.line(win, color, place1, place2, width=self.get_width())

    def get_width(self):
        if abs(self.weight) < 1:
            return 1
        elif abs(self.weight) > 10:
            return 10
        else:
            return int(abs(self.weight))

    def update(self, value):
        self.value = value * self.weight
