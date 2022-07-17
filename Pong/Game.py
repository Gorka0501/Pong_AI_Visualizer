import pygame

from .Ball import Ball
from .Paddle import Paddle
from .GameInfo import GameInfo
from .Options import *

pygame.init()


class Game:

    WINNING_SCORE = 7

    def __init__(self, wall=False):
        self.wall = wall
        self.WIDTH = WIDTH
        self.height = HEIGHT
        self.left_paddle = Paddle(WIDTH, HEIGHT, 'L')
        if not wall:
            self.right_paddle = Paddle(WIDTH, HEIGHT, 'R')
        self.ball = Ball(WIDTH, HEIGHT)
        self.left_score = 0
        self.right_score = 0
        self.left_hits = 0
        self.right_hits = 0
        if SHOW:
            self.win = pygame.display.set_mode((WIDTH+500, HEIGHT))
        self.font = pygame.font.SysFont('comicsansms', HEIGHT // 10)

    def draw(self, hits=False):
        pygame.draw.rect(self.win, BLACK, pygame.Rect(0, 0, WIDTH, HEIGHT))

        left_score_text = self.font.render(str(self.left_score), 1, WHITE)
        right_score_text = self.font.render(str(self.right_score), 1, WHITE)
        self.win.blit(left_score_text, (WIDTH // 4 - left_score_text.get_width() // 2, HEIGHT / 40))
        self.win.blit(right_score_text, ((WIDTH // 4) * 3 - right_score_text.get_width() // 2, HEIGHT / 40))

        self.left_paddle.draw(self.win)
        if not self.wall:
            self.right_paddle.draw(self.win)


        self.ball.draw(self.win)
        if hits:
            hits_text = self.font.render(str(self.right_hits + self.left_hits), 1, WHITE)
            self.win.blit(hits_text, (WIDTH // 2 - hits_text.get_width() // 2, HEIGHT / 40))

        pygame.display.update()

    def handle_paddle_movement(self, left, up):
        if up:
            if left and self.left_paddle.y - self.left_paddle.VEL >= 0:
                self.left_paddle.move(up=True)
            elif not self.wall and not left and self.right_paddle.y - self.right_paddle.VEL >= 0:
                self.right_paddle.move(up=True)
            else:
                return False
        else:
            if left and self.left_paddle.y + self.left_paddle.VEL + self.left_paddle.height <= HEIGHT:
                self.left_paddle.move(up=False)
            elif not self.wall and not left and self.right_paddle.y + self.right_paddle.VEL + self.right_paddle.height <= HEIGHT:
                self.right_paddle.move(up=False)
            else:
                return False
        return True

    def handle_collision(self):
        if self.ball.y + self.ball.size >= HEIGHT:
            self.ball.y = HEIGHT - self.ball.size
            self.ball.y_vel *= -1
        elif self.ball.y <= 0:
            self.ball.y_vel *= -1

        if self.ball.x_vel < 0:
            if self.ball.y >= self.left_paddle.y and self.ball.y <= self.left_paddle.y + self.left_paddle.height:
                if self.ball.x >= self.left_paddle.x and self.ball.x <= self.left_paddle.x + self.left_paddle.width:
                    self.ball.x_vel *= -1

                    middle_y = self.left_paddle.y + self.left_paddle.height / 2
                    difference_y = self.ball.y + self.ball.size / 2 - middle_y
                    reduction_factor = (self.left_paddle.height / 2) / self.ball.vel
                    y_vel = difference_y / reduction_factor
                    self.ball.y_vel = y_vel * 0.75
                    self.ball.x_vel = self.ball.vel - abs(self.ball.y_vel)

                    self.left_hits += 1

                    return True

        if self.ball.x_vel > 0 and not self.wall:
            if self.ball.y >= self.right_paddle.y and self.ball.y <= self.right_paddle.y + self.right_paddle.height:
                if self.ball.x >= self.right_paddle.x and self.ball.x <= self.right_paddle.x + self.right_paddle.width:
                    self.ball.x_vel *= -1

                    middle_y = self.right_paddle.y + self.right_paddle.height / 2
                    difference_y = self.ball.y + self.ball.size / 2 - middle_y
                    reduction_factor = (self.right_paddle.height / 2) / self.ball.vel
                    y_vel = difference_y / reduction_factor
                    self.ball.y_vel = y_vel * 0.75
                    self.ball.x_vel = -self.ball.vel + abs(self.ball.y_vel)

                    self.right_hits += 1

                    return True

    def handle_vel(self):
        if (self.left_hits + self.right_hits) % 5 == 0:
            self.ball.vel_increase()

    def reset(self):
        self.ball.reset()
        self.left_paddle.reset()
        if not self.wall:
            self.right_paddle.reset()
        self.left_score = 0
        self.right_score = 0
        self.left_hits = 0
        self.right_hits = 0

    def loop(self):

        self.ball.move()
        if self.handle_collision():
            self.handle_vel()

        if self.ball.x < 0:
            self.right_score += 1
            self.ball.reset()
            if self.wall:
                self.ball.x_vel *= -1
        if self.ball.x > WIDTH:
            if not self.wall:
                self.left_score += 1
                self.ball.reset()
            else:
                self.ball.vel = self.ball.o_vel
                self.ball.x = WIDTH - self.ball.size * 2
                self.ball.y_vel = self.ball.get_random_y_vel()
                self.ball.x_vel = self.ball.get_x_vel() * -1

        gameInfo = GameInfo(
            self.left_hits, self.right_hits, self.left_score, self.right_score)

        return gameInfo

    def pause(self):
        pause = True

        while pause:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        pause = False
