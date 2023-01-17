import pygame
import save
from level import Level
from menu import MainMenu, LevelSelectionMenu
from hud import HealthBar, MoneyCounter
from properties import WIDTH, HEIGHT, background_path, levels


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.background = pygame.transform.scale(pygame.image.load(background_path).convert_alpha(), (WIDTH, HEIGHT))

        self.main_menu = None
        self.level_selection_menu = None
        self.level = None
        self.level_num = 0

        self.health_bar = HealthBar(self.screen)
        self.money_counter = MoneyCounter(self.screen)

        self.data = save.load_data()
        self.show_main_menu()

    def show_main_menu(self):
        self.main_menu = MainMenu(self.screen, [('Играть', self.show_level_selection_menu),
                                                ('Выход', lambda: pygame.event.post(pygame.event.Event(pygame.QUIT)))])
        self.level_selection_menu = None
        self.level = None

    def show_level_selection_menu(self):
        self.main_menu = None
        self.level_selection_menu = LevelSelectionMenu(self.screen, self.data['level'], len(levels),
                                                       self.load_level, self.show_main_menu)
        self.level = None

    def load_level(self, num):
        self.level_num = num
        self.main_menu = None
        self.level_selection_menu = None
        self.level = Level(self.screen, levels[self.level_num - 1], self.get_damage, self.add_coin, self.game_end)

    def game_end(self, goal):
        if goal:
            if len(levels) > self.data['level'] == self.level_num:
                self.data['level'] += 1
        else:
            self.get_damage(10)
        self.show_level_selection_menu()

    def get_damage(self, damage):
        self.data['health'] -= damage
        if self.data['health'] <= 0:
            self.data['health'] = 100
            self.data['level'] = 1
            self.show_level_selection_menu()

    def add_coin(self):
        self.data['money'] += 1

    def update(self, tick):
        self.screen.blit(self.background, (0, 0))

        if self.main_menu is not None:
            self.main_menu.update()
        elif pygame.key.get_pressed()[pygame.K_ESCAPE]:
            self.show_main_menu()
        if self.level_selection_menu is not None:
            self.level_selection_menu.update()
        if self.level is not None:
            self.level.update(tick)
            self.health_bar.update(self.data['health'])
            self.money_counter.update(self.data['money'])

    def save(self):
        save.save_data(self.data)
