import pygame
import os
from sprite import AnimatedSprite
from properties import npc, TILE_WIDTH, TILE_HEIGHT


class Npc(AnimatedSprite):
    def __init__(self, x, y, group):
        self.movement_speed = 0.5

        self.images = [pygame.transform.scale(pygame.image.load(el).convert_alpha(), (TILE_WIDTH, TILE_HEIGHT))
                       for el in npc]

        super().__init__(self.images, x, y, group)

    def rotate(self):
        self.movement_speed = -self.movement_speed

    def update(self, tick, shift_x, shift_y):
        self.rect.x += int(self.movement_speed * tick)

        self.animate(tick)
        if self.movement_speed < 0:
            self.image = pygame.transform.flip(self.image, True, False)

        self.rect.x += shift_x
        self.rect.y += shift_y
