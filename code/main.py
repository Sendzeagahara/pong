import json

from settings import *
from sprites import *
from groups import AllSprites


class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Pong')
        self.clock = pygame.time.Clock()
        self.running = True

        # groups
        self.all_sprites = AllSprites()
        self.paddle_sprites = pygame.sprite.Group()

        # sprites
        self.ball = Ball(self.all_sprites, self.paddle_sprites, self.update_score)
        self.player = Player((self.all_sprites, self.paddle_sprites))
        self.opponent = Opponent((self.all_sprites, self.paddle_sprites), self.ball)

        # score
        try:
            with open(join('..', 'data', 'score.txt'), 'r') as score_file:
                self.score = json.load(score_file)
        except FileNotFoundError:
            self.score = {'player': 0, 'opponent': 0}
        self.font = pygame.font.Font(None, 160)

    def display_score(self):
        # player
        player_surf = self.font.render(str(self.score['player']), True, COLORS['bg detail'])
        player_rect = player_surf.get_frect(midleft=(WINDOW_WIDTH / 2 + 50, WINDOW_HEIGHT / 2))
        self.display_surface.blit(player_surf, player_rect)

        #opponent
        opponent_surf = self.font.render(str(self.score['opponent']), True, COLORS['bg detail'])
        opponent_rect = opponent_surf.get_frect(midright=(WINDOW_WIDTH / 2 - 50, WINDOW_HEIGHT / 2))
        self.display_surface.blit(opponent_surf, opponent_rect)

        # line separator
        pygame.draw.line(self.display_surface,
                         COLORS['bg detail'],
                         (WINDOW_WIDTH / 2, 0),
                         (WINDOW_WIDTH / 2, WINDOW_HEIGHT),
                         10)

    def update_score(self, side):
        self.score['player' if side == 'player' else 'opponent'] += 1

    def run(self):
        while self.running:
            dt = self.clock.tick() / 1000

            # event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    with open(join('..', 'data', 'score.txt'), 'w') as score_file:
                        json.dump(self.score, score_file)
                    self.running = False

            # update
            self.all_sprites.update(dt)

            #draw
            self.display_surface.fill(COLORS['bg'])
            self.display_score()
            self.all_sprites.draw()
            pygame.display.update()
        pygame.quit()


if __name__ == '__main__':
    game = Game()
    game.run()
