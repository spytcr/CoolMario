import pygame
from game import Game
from properties import WIDTH, HEIGHT


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
width, height = screen.get_size()
clock = pygame.time.Clock()
running = True
game = Game(screen)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game.save()
            running = False
    screen.fill(0)
    game.update(clock.tick())
    pygame.display.flip()
pygame.quit()

