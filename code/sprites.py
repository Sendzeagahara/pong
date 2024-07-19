from settings import * 
from random import choice, uniform


class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)


class Ball(pygame.sprite.Sprite):
    def __init__(self, groups, paddle_sprites):
        super().__init__(groups)
