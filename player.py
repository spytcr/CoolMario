import pygame
import os
from sprite import AnimatedSprite
from properties import character, TILE_WIDTH, TILE_HEIGHT


class Player(AnimatedSprite):
    def __init__(self, x, y, group):
        self.movement_speed = 0.8
        self.jump_speed = 1.4
        self.gravity = 0.005

        self.hp = 100

        self.speed_x, self.speed_y = 0, 0

        self.on_ground = False
        self.rotated = False
        self.status = 'idle'

        self.animations = character.copy()
        for k, v in self.animations.items():
            self.animations[k] = [pygame.transform.scale(
                pygame.image.load(el).convert_alpha(), (1.5 * TILE_WIDTH, 1.5 * TILE_HEIGHT)) for el in v]

        super().__init__(self.animations[self.status], x, y, group)

    def set_status(self, status):
        if self.status != status:
            self.status = status
            self.images = self.animations[self.status]
            self.frame = 0

    def update(self, tick):
        self.speed_y += self.gravity * tick

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.speed_x = -self.movement_speed
            self.set_status('run')
            self.rotated = True
        elif keys[pygame.K_RIGHT]:
            self.speed_x = self.movement_speed
            self.set_status('run')
            self.rotated = False
        else:
            self.speed_x = 0
            self.set_status('idle')
        if keys[pygame.K_SPACE] and self.on_ground:
            self.speed_y = -self.jump_speed
            self.set_status('jump')

        self.animate(tick)
        if self.rotated:
            self.image = pygame.transform.flip(self.image, True, False)

