from sprite import Sprite


class Tile(Sprite):
    def __init__(self, image, x, y, group):
        super().__init__(image, x, y, group)

    def update(self, shift_x, shift_y):
        self.rect.x += shift_x
        self.rect.y += shift_y
