import os

import pygame


class Sprite(pygame.sprite.Sprite):
    def __init__(self, image, x, y, group):
        super().__init__(group)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y


class AnimatedSprite(Sprite):
    def __init__(self, images, x, y, group):
        self.anim_speed = 0.005

        self.images = images
        self.frame = 0

        super().__init__(self.images[self.frame], x, y, group)

    def animate(self, tick):
        self.image = self.images[int(self.frame)]
        self.rect = self.image.get_rect().move(self.rect.x, self.rect.y)

        self.frame += tick * self.anim_speed
        if self.frame >= len(self.images):
            self.frame = 0
