import sys
import pygame
from level import Level
from settings import level_map

screen_width: int = 1200
screen_height: int = 700

# setup pygame
pygame.init()

screen: object = pygame.display.set_mode([screen_width, screen_height])
clock: object = pygame.time.Clock()
level = Level(level_map, screen)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill("black")
    level.run()

    pygame.display.update()
    clock.tick(60)
