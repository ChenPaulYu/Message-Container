import pygame, sys
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
background = pygame.image.load('bridge.jpg')


while True:
    screen.blit(background, [0,0])
    pygame.display.flip()