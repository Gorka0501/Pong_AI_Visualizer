import os.path
import pickle

import neat
import pygame
import os

from Visualization.NerualNetwork import NeuralNetwork
from .Options import *
from .Game import Game


class Pong_Controller:

    def __init__(self, cheat=False):
        self.width = WIDTH
        self.height = HEIGHT
        self.cheat = cheat
        self.game = Game(cheat)
        self.left_paddle = self.game.left_paddle
        if not cheat:
            self.right_paddle = self.game.right_paddle
        self.ball = self.game.ball

    def play(self, lAI=False, rAI=False, config=False):
        if lAI:
            net1 = NeuralNetwork.create(lAI, config)
        if rAI:
            net2 = NeuralNetwork.create(rAI, config, False)

        clock = pygame.time.Clock()
        run = True
        while run:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.game.pause()

            if lAI:
                output1 = net1.activate(self.get_inputs(True))
                decision1 = output1.index(max(output1))

                if decision1 == 0:
                    pass
                elif decision1 == 1:
                    self.game.handle_paddle_movement(left=True, up=True)
                elif decision1 == 2:
                    self.game.handle_paddle_movement(left=True, up=False)
            else:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_w]:
                    self.game.handle_paddle_movement(left=True, up=True)
                if keys[pygame.K_s]:
                    self.game.handle_paddle_movement(left=True, up=False)

            if rAI:
                output2 = net2.activate(self.get_inputs(False))
                decision2 = output2.index(max(output2))

                if decision2 == 0:
                    pass
                elif decision2 == 1:
                    self.game.handle_paddle_movement(left=False, up=True)
                elif decision2 == 2:
                    self.game.handle_paddle_movement(left=False, up=False)

            elif not self.cheat:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_UP]:
                    self.game.handle_paddle_movement(left=False, up=True)
                if keys[pygame.K_DOWN]:
                    self.game.handle_paddle_movement(left=False, up=False)

            game_info = self.game.loop()
            self.game.draw()
            if lAI:
                net1.update()
                net1.draw(self.game.win)
            if rAI:
                net2.update()
                net2.draw(self.game.win)

            if game_info.left_score >= WIN_POINTS or game_info.right_score >= WIN_POINTS:
                break
                pygame.quit()

    def train_ai(self, genome1, genome2, config, both):
        net1 = NeuralNetwork.create(genome1, config)
        if not self.cheat:
            net2 = NeuralNetwork.create(genome2, config, False)


        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.game.pause()
                    if event.key == pygame.K_LALT:
                        global SHOW
                        SHOW = not SHOW

            output1 = net1.activate(self.get_inputs(True))
            decision1 = output1.index(max(output1))

            if decision1 == 0:
                pass
            elif decision1 == 1:
                self.game.handle_paddle_movement(left=True, up=True)
            elif decision1 == 2:
                self.game.handle_paddle_movement(left=True, up=False)

            if not self.cheat:
                output2 = net2.activate(self.get_inputs(False))
                decision2 = output2.index(max(output2))
                if decision2 == 0:
                    pass
                elif decision2 == 1:
                    self.game.handle_paddle_movement(left=False, up=True)
                elif decision2 == 2:
                    self.game.handle_paddle_movement(left=False, up=False)

            if SHOW:
                self.game.draw(True)
                net1.update()
                net1.draw(self.game.win)
                if not self.cheat:
                    net2.update()
                    net2.draw(self.game.win)

            game_info = self.game.loop()

            if game_info.right_score >= WIN_POINTS or game_info.left_score >= WIN_POINTS or game_info.right_hits + game_info.left_hits >= 1000:
                if not both or self.cheat:
                    self.calculate_fitness(genome1, game_info, both)
                else:
                    self.calculate_fitness((genome1, genome2), game_info, both)
                break

    def calculate_fitness(self, genomes, game_info, both):
        if not both:
            if self.cheat:
                genomes.fitness += game_info.left_hits
            else:
                genomes.fitness += game_info.left_hits + 1000 * (game_info.left_score - game_info.right_score)
        else:
            genomes[0].fitness += game_info.left_hits
            genomes[1].fitness += game_info.right_hits

    def get_inputs2(self, left=True):
        if left:
            inputs = [(self.left_paddle.y - self.left_paddle.height / 2) / HEIGHT, (self.ball.y - self.ball.size) / HEIGHT,
                      abs(self.left_paddle.x + self.left_paddle.width / 2 - self.ball.x + self.ball.size / 2) / WIDTH,
                      self.ball.y_vel / HEIGHT, - self.ball.x_vel / WIDTH]
            if not self.cheat:
                inputs.append((self.right_paddle.y + self.right_paddle.height / 2) / HEIGHT)
            else:
                inputs.append(0)
        else:
            inputs = [(self.right_paddle.y - self.right_paddle.height / 2) / HEIGHT, (self.ball.y - self.ball.size) / HEIGHT,
                      abs(self.right_paddle.x + self.right_paddle.width / 2 - self.ball.x + self.ball.size / 2) / WIDTH,
                      self.ball.y_vel / HEIGHT, self.ball.x_vel / WIDTH,
                      (self.left_paddle.y + self.left_paddle.height / 2) / HEIGHT]

        return inputs

    def get_inputs(self, left=True):
        if left:
            inputs = [(self.ball.y - self.ball.size), HEIGHT - (self.ball.y - self.ball.size),
                      self.ball.y_vel, -self.ball.x_vel, self.left_paddle.y, HEIGHT - self.left_paddle.y,
                      self.ball.x + self.ball.size - self.left_paddle.x]
            if not self.cheat:
                inputs.append(self.right_paddle.y)
                inputs.append(HEIGHT - self.right_paddle.y)
            else:
                inputs.append(0)
                inputs.append(0)
        else:
            inputs = [(self.ball.y - self.ball.size), HEIGHT - (self.ball.y - self.ball.size),
                      self.ball.y_vel, self.ball.x_vel, self.right_paddle.y, HEIGHT - self.right_paddle.y,
                      self.right_paddle.x + self.right_paddle.width - self.ball.x + self.ball.size,
                      self.left_paddle.y, HEIGHT - self.left_paddle.y]

        return inputs

