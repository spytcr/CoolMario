import pygame

from properties import WIDTH, HEIGHT, logo_path, btn_path, btn_color, menu_bg_path, level_btn_path, level_locked_path
from sprite import Sprite
from hud import Button


class MainMenu:
    def __init__(self, screen, options):
        self.screen = screen

        self.logo = pygame.sprite.GroupSingle()
        logo_surface = pygame.transform.scale(pygame.image.load(logo_path).convert_alpha(),
                                              (WIDTH * 0.5, HEIGHT * 0.3))
        Sprite(logo_surface, WIDTH * 0.25, HEIGHT * 0.05, self.logo)

        self.buttons = pygame.sprite.Group()
        btn_surface = pygame.transform.scale(pygame.image.load(btn_path).convert_alpha(),
                                             (WIDTH * 0.5, min(HEIGHT * 0.2, (HEIGHT * 0.5) // len(options))))
        btn_x, btn_y = WIDTH * 0.25, HEIGHT * 0.4
        for text, on_click in options:
            Button(text, on_click, pygame.color.Color(btn_color), btn_surface.copy(), btn_x, btn_y, self.buttons)
            btn_y += btn_surface.get_height() + 40

    def update(self):
        self.buttons.update()

        self.logo.draw(self.screen)
        self.buttons.draw(self.screen)


class LevelSelectionMenu:
    HORIZONTAL, VERTICAL = 5, 3

    def __init__(self, screen, unlocked_cnt, level_cnt, on_select, on_cancel):
        self.screen = screen

        self.background = pygame.sprite.GroupSingle()
        background_surface = pygame.transform.scale(pygame.image.load(menu_bg_path),
                                                    (WIDTH * 0.6, HEIGHT * 0.7))
        Sprite(background_surface, WIDTH * 0.2, HEIGHT * 0.1, self.background)

        self.buttons = pygame.sprite.Group()
        size = min(background_surface.get_width() * 0.75 // self.HORIZONTAL,
                   background_surface.get_height() * 0.7 // self.VERTICAL)

        btn_surface = pygame.transform.scale(pygame.image.load(level_btn_path).convert_alpha(),
                                             (size, size))

        self.locked = pygame.sprite.Group()
        locked_surface = pygame.transform.scale(pygame.image.load(level_locked_path).convert_alpha(),
                                                (size, size))

        for i in range(self.VERTICAL):
            for j in range(self.HORIZONTAL):
                k = i * self.HORIZONTAL + j + 1
                x = self.background.sprite.rect.x * 1.3 + (size + 20) * j
                y = self.background.sprite.rect.y * 1.8 + (size + 20) * i
                if k <= unlocked_cnt:
                    Button(str(k), on_select, pygame.Color(btn_color), btn_surface.copy(), x, y, self.buttons, k)
                elif k <= level_cnt:
                    Sprite(locked_surface.copy(), x, y, self.locked)
                else:
                    Sprite(btn_surface.copy(), x, y, self.locked)

        self.back_btn = pygame.sprite.GroupSingle()
        back_btn_surface = pygame.transform.scale(pygame.image.load(btn_path).convert_alpha(),
                                                  (WIDTH * 0.4, HEIGHT * 0.1))
        Button('Назад', on_cancel, pygame.color.Color(btn_color), back_btn_surface,
               WIDTH * 0.3, HEIGHT * 0.85, self.back_btn)

    def update(self):
        self.buttons.update()
        self.back_btn.update()

        self.background.draw(self.screen)
        self.buttons.draw(self.screen)
        self.locked.draw(self.screen)
        self.back_btn.draw(self.screen)

