import math
import random
import pygame

from .Options import *


class Ball:

    def __init__(self, width, height):
        self.size = width / 70
        self.x = self.o_x = width / 2 - self.size / 2
        self.y = self.o_y = height / 2 - self.size / 2
        self.vel = self.o_vel = self.size * START_VEL
        self.y_vel = self.get_random_y_vel()
        self.x_vel = 0
        self.x_vel = self.get_x_vel() * random.choice([-1, 1])

    def draw(self, window):
        pygame.draw.circle(window, WHITE, (self.x, self.y), self.size)

    def move(self):
        self.y += self.y_vel
        self.x += self.x_vel


    def get_random_angle(self, min_angle, max_angle, excluded):
        angle = 0
        while angle in excluded:
            angle = math.radians(random.randrange(min_angle, max_angle))

        return angle

    def reset(self):
        self.x = self.o_x
        self.y = self.o_y
        self.vel = self.o_vel
        self.y_vel = self.get_random_y_vel()
        self.x_vel = self.get_x_vel()

    def get_random_y_vel(self):
        angle = self.get_random_angle(-30, 30, [0])
        y_vel = math.sin(angle) * self.vel
        return y_vel

    def get_x_vel(self):
        if self.x_vel < 0:
            x_vel = -self.vel + abs(self.y_vel)
        if self.x_vel >= 0:
            x_vel = self.vel - abs(self.y_vel)
        return x_vel

    def vel_increase(self):
        if self.vel + VEL_INCREASE <= MAX_VEL*10:
            self.vel += VEL_INCREASE
            self.x_vel = self.get_x_vel()

