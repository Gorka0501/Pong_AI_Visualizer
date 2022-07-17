import pygame.draw


class Paddle:
    COLOR = (255, 255, 255)
    VEL = 5

    def __init__(self, width, height, place):
        self.width = width / 35
        self.height = height / 5
        if place == 'L':
            self.x = self.o_x = width / 50
        else:
            self.x = self.o_x = width - width / 50 - self.width

        self.y = self.o_y = height / 2 - self.height / 2

    def draw(self, window):
        pygame.draw.rect(window, self.COLOR, (self.x, self.y, self.width, self.height))

    def move(self, up=True):
        if up:
            self.y -= self.VEL
        else:
            self.y += self.VEL

    def reset(self):
        self.x = self.o_x
        self.y = self.o_y