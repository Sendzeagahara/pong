from settings import *
from random import choice, uniform


class Paddle(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)

        # image
        self.image = pygame.Surface(SIZE['paddle'], pygame.SRCALPHA)
        pygame.draw.rect(self.image,
                         COLORS['paddle'],
                         pygame.FRect((0, 0), SIZE['paddle']),
                         0,
                         5)

        # shadow surface
        self.shadow_surf = self.image.copy()
        pygame.draw.rect(self.shadow_surf,
                         COLORS['paddle shadow'],
                         pygame.FRect((0, 0), SIZE['paddle']),
                         0,
                         5)

        # rect & movement
        self.rect = self.image.get_frect(center=POS['player'])
        self.old_rect = self.rect.copy()
        self.direction = 0

    def move(self, delta_time):
        self.rect.centery += self.direction * self.speed * delta_time
        self.rect.top = 0 if self.rect.top < 0 else self.rect.top
        self.rect.bottom = WINDOW_HEIGHT if self.rect.bottom > WINDOW_HEIGHT else self.rect.bottom

    def update(self, delta_time):
        self.old_rect = self.rect.copy()
        self.get_direction()
        self.move(delta_time)


class Player(Paddle):
    def __init__(self, groups):
        super().__init__(groups)

        self.speed = SPEED['player']

    def get_direction(self):
        keys = pygame.key.get_pressed()
        self.direction = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])


class Opponent(Paddle):
    def __init__(self, groups, ball):
        super().__init__(groups)

        self.rect.center = POS['opponent']
        self.speed = SPEED['opponent']
        self.ball = ball

    def get_direction(self):
        self.direction = 1 if self.rect.centery < self.ball.rect.centery else -1


class Ball(pygame.sprite.Sprite):
    def __init__(self, groups, paddle_sprites, update_score):
        super().__init__(groups)
        self.paddle_sprites = paddle_sprites
        self.update_score = update_score

        # image
        self.image = pygame.Surface(SIZE['ball'], pygame.SRCALPHA)
        pygame.draw.circle(self.image,
                           COLORS['ball'],
                           (SIZE['ball'][0] / 2, SIZE['ball'][1] / 2),
                           SIZE['ball'][0] / 2)

        # shadow surface
        self.shadow_surf = self.image.copy()
        pygame.draw.circle(self.shadow_surf,
                           COLORS['ball shadow'],
                           (SIZE['ball'][0] / 2, SIZE['ball'][1] / 2),
                           SIZE['ball'][0] / 2)

        # rect & movement
        self.rect = self.image.get_frect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
        self.old_rect = self.rect.copy()
        self.direction = pygame.math.Vector2(choice((1, -1)), uniform(0.7, 0.8) * choice((-1, 1)))
        self.speed = SPEED['ball']
        self.speed_modifier = 0

        # reset timer
        self.start_time = pygame.time.get_ticks()
        self.reset_timer = 1200

    def move(self, delta_time):
        self.rect.x += self.direction.x * self.speed * delta_time * self.speed_modifier
        self.collision('horizontal')
        self.rect.y += self.direction.y * self.speed * delta_time * self.speed_modifier
        self.collision('vertical')

    def collision(self, direction):
        for sprite in self.paddle_sprites:
            if sprite.rect.colliderect(self.rect):
                if direction == 'horizontal':
                    if self.rect.right >= sprite.rect.left and self.old_rect.right <= sprite.old_rect.left:
                        self.rect.right = sprite.rect.left
                        self.direction.x *= -1
                    elif self.rect.left <= sprite.rect.right and self.old_rect.left >= sprite.old_rect.left:
                        self.rect.left = sprite.rect.right
                        self.direction.x *= -1
                elif direction == 'vertical':
                    if self.rect.bottom >= sprite.rect.top and self.old_rect.bottom <= sprite.old_rect.top:
                        self.rect.bottom = sprite.rect.top
                        self.direction.y *= -1
                    elif self.rect.top <= sprite.rect.bottom and self.old_rect.top >= sprite.old_rect.bottom:
                        self.rect.top = sprite.rect.bottom
                        self.direction.y *= -1

    def wall_collision(self):
        if self.rect.top <= 0:
            self.rect.top = 0
            self.direction.y *= -1
        if self.rect.bottom >= WINDOW_HEIGHT:
            self.rect.bottom = WINDOW_HEIGHT
            self.direction.y *= -1
        if self.rect.left <= 0 or self.rect.right >= WINDOW_WIDTH:
            self.update_score('player' if self.rect.x < WINDOW_WIDTH / 2 else 'opponent')
            self.reset()

    def reset(self):
        self.rect.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
        self.direction = pygame.math.Vector2(choice((1, -1)), uniform(0.7, 0.8) * choice((-1, 1)))
        self.start_time = pygame.time.get_ticks()

    def timer(self):
        if pygame.time.get_ticks() - self.start_time >= self.reset_timer:
            self.speed_modifier = 1
        else:
            self.speed_modifier = 0

    def update(self, delta_time):
        self.old_rect = self.rect.copy()
        self.timer()
        self.move(delta_time)
        self.wall_collision()
