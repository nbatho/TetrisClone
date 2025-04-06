import pygame, sys
from setting import *

# components
from game import Game
from score import Score
from preview import Preview
from random import choice
from menu import main_menu, options
from network import Network
class Main:
    def __init__(self):
        # general
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH*2,WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('TetrisClone')

        #networking
        self.network = Network()
        self.player_id = None

        self.BOT = False
        self.play = "vsPlayer"
        if self.play == "vsBot":
            self.BOT = True
        elif self.play == "vsPlayer":
            self.BOT = False
            try:
                # Kết nối đến server
                self.player_id = self.network.send("get")
                print(f"Connected as Player {self.player_id}")
            except:
                print("Could not connect to server!")
                self.play = "single"  # Fallback to bot mode if connection fails
        #shapes
        self.next_shapes = [choice (list(TETROMINOS.keys())) for _ in range(7)]
        self.opponent_next_shapes = [choice (list(TETROMINOS.keys())) for _ in range(7)]

        # player
        self.game = Game(self.get_next_shape, self.update_score,bot_enable= False, x_offset = 0)
        self.score = Score(x_offset=0)
        self.preview = Preview(x_offset=0)
        # opponent
        if self.play == "vsBot":
            self.opponent_game = Game(self.get_opponent_next_shape, self.update_opponent_score,bot_enable= self.BOT, x_offset = WINDOW_WIDTH)
        else:
            self.opponent_game = Game(self.get_opponent_next_shape, self.update_opponent_score, bot_enable=self.BOT,x_offset=WINDOW_WIDTH,is_remoted= True)
        self.opponent_score = Score(x_offset=WINDOW_WIDTH)
        self.opponent_preview = Preview(x_offset=WINDOW_WIDTH)

    def update_score(self,lines,score,level):
        self.score.lines = lines
        self.score.score = score
        self.score.level = level
    def update_opponent_score(self,lines,score,level):
        self.opponent_score.lines = lines
        self.opponent_score.score = score
        self.opponent_score.level = level
    def get_next_shape(self):
        next_shape = self.next_shapes.pop(0)
        self.next_shapes.append(choice (list(TETROMINOS.keys())))
        return next_shape
    def get_opponent_next_shape(self):
        bot_next_shape = self.opponent_next_shapes.pop(0)
        self.opponent_next_shapes.append(choice(list(TETROMINOS.keys())))
        return bot_next_shape
    def run(self):
        game_running  = True
        while game_running:
            selection = main_menu()

            if selection == "play":
                playing = True
                if self.play == "vsPlayer":
                    player_id = self.network.send("get")  # Nhận player ID từ server
                    print(f"Connected as Player {player_id}")
                while playing:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        elif event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_ESCAPE:
                                playing = False
                                break
                            if event.key == pygame.K_r:  # Nhấn phím 'R' để reset
                                self.game.reset()

                    # display
                    self.display_surface.fill(GRAY)
                    self.game.run()
                    self.score.run()
                    self.preview.run(self.next_shapes)
                    if self.play in ["vsBot", "vsPlayer"]:
                        self.opponent_game.run()
                        self.opponent_score.run()
                        self.opponent_preview.run(self.opponent_next_shapes)
                    #updating the game
                    pygame.display.update()
                    self.clock.tick(60)

            elif selection == "options":
                options()
            elif selection == "quit":
                game_runinning = False
                pygame.quit()
                sys.exit()

if __name__ == '__main__':
    main = Main()
    main.run()
