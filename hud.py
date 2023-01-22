import pygame
from sprite import Sprite
from properties import WIDTH, health_bar_path, coin_path


class Button(Sprite):
    _clicked = False

    def __init__(self, text, on_click, color, surface, x, y, group, *args):
        super().__init__(surface, x, y, group)

        self.on_click = on_click
        self.args = args

        font = pygame.font.SysFont('arialblack', self.rect.height // 3)
        sign = font.render(text, True, color)
        self.image.blit(sign, ((self.rect.width - sign.get_width()) // 2, (self.rect.height - sign.get_height()) // 2))

    def update(self):
        if pygame.mouse.get_pressed()[0]:
            if not Button._clicked:
                x, y = pygame.mouse.get_pos()
                if self.rect.collidepoint(x, y):
                    Button._clicked = True
                    self.on_click(*self.args)
        elif Button._clicked:
            Button._clicked = False


class HealthBar:
    def __init__(self, screen):
        self.screen = screen

        self.image = pygame.image.load(health_bar_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x += WIDTH - 100 - self.rect.width
        self.rect.y += 15

        self.bar_rect = pygame.Rect(118 + self.rect.x, 37 + self.rect.y, 380, 34)

    def update(self, health):
        self.screen.blit(self.image, (self.rect.x, self.rect.y))

        rect = self.bar_rect.copy()
        rect.width *= health / 100
        pygame.draw.rect(self.screen, pygame.Color('red'), rect)


class MoneyCounter:
    def __init__(self, screen):
        self.screen = screen

        self.image = pygame.image.load(coin_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x += 50
        self.rect.y += 15

        self.font = pygame.font.SysFont('arialblack', self.rect.height)

    def update(self, money):
        self.screen.blit(self.image, (self.rect.x, self.rect.y))

        sign = self.font.render(str(money), True, pygame.Color('yellow'))
        self.screen.blit(sign, (self.rect.right + 15, self.rect.y - 20))

