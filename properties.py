import os

WIDTH, HEIGHT = 1980, 1080
TILE_WIDTH, TILE_HEIGHT = 64, 64

background_path = 'resources/background.png'
saves_path = 'resources/saves.csv'

character = {'idle': [], 'run': [], 'jump': []}
for key in character.keys():
    folder = 'resources/character/' + key
    for el in os.listdir(folder):
        if os.path.isfile(folder + '/' + el):
            character[key].append(folder + '/' + el)

npc = []
folder = 'resources/npc'
for el in os.listdir(folder):
    if os.path.isfile(folder + '/' + el):
        npc.append(folder + '/' + el)

logo_path = 'resources/hud/logo.png'
btn_path = 'resources/hud/btn.png'
btn_color = 'brown'
menu_bg_path = 'resources/hud/menu-bg.png'
level_btn_path = 'resources/hud/level-btn.png'
level_locked_path = 'resources/hud/level-locked.png'

health_bar_path = 'resources/hud/health-bar.png'
coin_path = 'resources/hud/coin.png'

levels = ['resources/tiled/level0.tmx']
