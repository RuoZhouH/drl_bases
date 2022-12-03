# -*- coding: utf-8 -*-
import pygame
import sys

pygame.init()
screen = pygame.display.set_caption("game test")
screen = pygame.display.set_mode([640, 480])
screen.fill([0, 0, 0])
pygame.draw.rect(screen, [255, 255, 255], [150, 50, 4, 4])
pygame.draw.rect(screen, [255, 255, 255], [150, 150, 4, 4])
pygame.draw.rect(screen, [255, 0, 0], [150, 0, 4, 4])
pygame.display.flip()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
