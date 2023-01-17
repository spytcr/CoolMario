import pygame
from player import Player
from npc import Npc
from properties import TILE_WIDTH, TILE_HEIGHT, WIDTH, HEIGHT
from tile import Tile
import pytmx


class Level:
    def __init__(self, screen, tmx, get_damage, add_coin, game_end):
        self.screen = screen

        self.get_damage = get_damage
        self.add_coin = add_coin
        self.game_end = game_end

        self.map = pytmx.load_pygame(tmx)

        self.water = pygame.sprite.Group()
        self.terrain = pygame.sprite.Group()
        self.background = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()

        self.player = pygame.sprite.GroupSingle()
        self.player_checkpoint = pygame.sprite.GroupSingle()

        self.npc = pygame.sprite.Group()
        self.npc_checkpoint = pygame.sprite.Group()

        self.load_map()

        self.camera_box = [0.25, 0.1, 0.75, 0.9]
        self.shift_x, self.shift_y = 0, 0

    def load_map(self):
        def apply_tile(_x, _y, layer, group):
            image: pygame.Surface = self.map.get_tile_image(_x, _y, layer)
            if image is not None:
                Tile(pygame.transform.scale(image, (int(TILE_WIDTH * (image.get_width() / self.map.tilewidth)),
                                                    int(TILE_HEIGHT * (image.get_height() / self.map.tileheight)))),
                     _x * TILE_WIDTH, _y * TILE_HEIGHT, group)

        def apply_helper(_x, _y, group):
            image = pygame.Surface((TILE_WIDTH, TILE_HEIGHT))
            image.set_alpha(255)
            Tile(image, _x * TILE_WIDTH, _y * TILE_HEIGHT, group)

        for x in range(self.map.width):
            for y in range(self.map.height):

                apply_tile(x, y, 0, self.water)
                apply_tile(x, y, 1, self.terrain)
                apply_tile(x, y, 2, self.background)
                apply_tile(x, y, 4, self.coins)

                if self.map.get_tile_gid(x, y, 3) != 0:
                    hid = self.map.tiledgidmap[self.map.get_tile_gid(x, y, 3)] - 625
                    if hid == 1:
                        Player(x * TILE_WIDTH, y * TILE_HEIGHT, self.player)
                    elif hid == 2:
                        apply_helper(x, y, self.player_checkpoint)
                    elif hid == 3:
                        Npc((x + 1) * TILE_WIDTH, y * TILE_HEIGHT, self.npc)
                        apply_helper(x, y, self.npc_checkpoint)
                    elif hid == 4:
                        apply_helper(x, y, self.npc_checkpoint)

    def npc_collision(self):
        for npc in pygame.sprite.groupcollide(self.npc, self.npc_checkpoint, False, False).keys():
            npc.rotate()

        player = self.player.sprite
        for npc in pygame.sprite.spritecollide(self.player.sprite, self.npc, False):
            if npc.rect.top < player.rect.bottom < npc.rect.centery and player.speed_y > 0:
                npc.kill()
            else:
                self.get_damage(1)

    def coin_collision(self):
        for _ in pygame.sprite.spritecollide(self.player.sprite, self.coins, True):
            self.add_coin()

    def check_end(self):
        if pygame.sprite.spritecollideany(self.player.sprite, self.water):
            self.game_end(False)
        if pygame.sprite.spritecollideany(self.player.sprite, self.player_checkpoint):
            self.game_end(True)

    def x_collision(self):
        player = self.player.sprite
        sprite = pygame.sprite.spritecollideany(player, self.terrain)
        if sprite:
            if player.speed_x > 0:
                player.rect.right = sprite.rect.left
            elif player.speed_x < 0:
                player.rect.left = sprite.rect.right

    def y_collision(self):
        player = self.player.sprite
        sprite = pygame.sprite.spritecollideany(player, self.terrain)
        if sprite:
            if player.speed_y > 0:
                player.rect.bottom = sprite.rect.top
                player.on_ground = True
            elif player.speed_y < 0:
                player.rect.top = sprite.rect.bottom
            player.speed_y = 0

        if player.on_ground and player.speed_y < 0 or player.speed_y > 1:
            player.on_ground = False

    def player_move(self, tick):
        player = self.player.sprite

        player.rect.x += int(player.speed_x * tick)
        self.x_collision()

        if player.rect.centerx < WIDTH * self.camera_box[0]:
            self.shift_x = int(WIDTH * self.camera_box[0] - player.rect.centerx)
        elif player.rect.centerx > WIDTH * self.camera_box[2]:
            self.shift_x = int(WIDTH * self.camera_box[2] - player.rect.centerx)
        else:
            self.shift_x = 0
        player.rect.x += self.shift_x

        player.rect.y += int(player.speed_y * tick)
        self.y_collision()

        if player.rect.centery < HEIGHT * self.camera_box[1]:
            self.shift_y = int(HEIGHT * self.camera_box[1] - player.rect.centery)
        elif player.rect.centery > HEIGHT * self.camera_box[3]:
            self.shift_y = int(HEIGHT * self.camera_box[3] - player.rect.centery)
        else:
            self.shift_y = 0
        player.rect.y += self.shift_y

    def update(self, tick):
        self.player.update(tick)
        self.player_move(tick)

        self.water.update(self.shift_x, self.shift_y)
        self.terrain.update(self.shift_x, self.shift_y)
        self.background.update(self.shift_x, self.shift_y)
        self.coins.update(self.shift_x, self.shift_y)
        self.player_checkpoint.update(self.shift_x, self.shift_y)
        self.npc.update(tick, self.shift_x, self.shift_y)
        self.npc_checkpoint.update(self.shift_x, self.shift_y)

        self.npc_collision()
        self.coin_collision()
        self.check_end()

        self.water.draw(self.screen)
        self.terrain.draw(self.screen)
        self.background.draw(self.screen)
        self.coins.draw(self.screen)
        self.player.draw(self.screen)
        self.npc.draw(self.screen)


