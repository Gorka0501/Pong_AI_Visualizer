import pygame as py
py.font.init()

# -------------DISPLAY OPTIONS--------------
SHOW = True
FPS = 60
WIDTH = 800
HEIGHT = 500

#------------GAME OPTIONS-------------------
WIN_POINTS = 10
START_VEL = 1     #Ball Velocity = Ball Size * START_VEL
MAX_VEL = 10         #Ball Max Velocity = Ball Size * MAX_VEL
VEL_INCREASE = 0.5
N_TOUCHES = 5       #Every N_TOUCHES ball velocity will increase by VEL_INCREASE

#------------AI_OPTIONS--------------------
INPUTS = 6
OUTPUTS = 3

#------------COLORS and FONTS--------------
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
DARK_RED = (100, 0, 0)
RED_PALE = (250, 200, 200)
DARK_RED_PALE = (150, 100, 100)
GREEN = (0, 200, 0)
DARK_GREEN = (0, 100, 0)
GREEN_PALE = (200, 250, 200)
DARK_GREEN_PALE = (100, 150, 100)
BLUE = (0,0,255)
BLUE_PALE = (200, 200, 255)
DARK_BLUE = (100, 100, 150)
ORANGE = (255,165,0)

NODE_FONT = py.font.SysFont("comicsans", 15)
STAT_FONT = py.font.SysFont("comicsans", 50)
