from settings import *


class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()

    def draw(self):
        for sprite in self:
            for i in range(4):
                self.display_surface.blit(sprite.shadow_surf, sprite.rect.topleft + pygame.math.Vector2(i, i))

        for sprite in self:
            self.display_surface.blit(sprite.image, sprite.rect)
