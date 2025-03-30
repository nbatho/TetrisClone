from setting import *

# components
from game import Game
from score import Score
from preview import Preview
from random import choice

class Main:
    def __init__(self):
        # general
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH*2,WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('TetrisClone')
        # bot
        #shapes
        self.next_shapes = [choice (list(TETROMINOS.keys())) for _ in range(7)]

        # player
        self.game = Game(self.get_next_shape, self.update_score,bot_enable= False, x_offset = 0)
        self.score = Score(x_offset=0)
        self.preview = Preview(x_offset=0)
        #bot
        self.bot_game = Game(self.get_next_shape, self.update_bot_score,bot_enable= True, x_offset = WINDOW_WIDTH)
        self.bot_score = Score(x_offset=WINDOW_WIDTH)
        self.bot_preview = Preview(x_offset=WINDOW_WIDTH)

    def update_score(self,lines,score,level):
        self.score.lines = lines
        self.score.score = score
        self.score.level = level
    def update_bot_score(self,lines,score,level):
        self.bot_score.lines = lines
        self.bot_score.score = score
        self.bot_score.level = level
    def get_next_shape(self):
        next_shape = self.next_shapes.pop(0)
        self.next_shapes.append(choice (list(TETROMINOS.keys())))
        return next_shape

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:  # Nhấn phím 'R' để reset
                        self.game.reset()
            # display
            self.display_surface.fill(GRAY)
            self.game.run()
            self.bot_game.run()
            self.score.run()
            self.bot_score.run()

            self.preview.run(self.next_shapes)
            self.bot_preview.run(self.next_shapes)
            #updating the game
            pygame.display.update()
            self.clock.tick(60)
if __name__ == '__main__':
    main = Main()
    main.run()
