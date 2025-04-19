from setting import *

# components
from game import Game
from score import Score
from preview import Preview
from random import choice
from menu import main_menu, options
from network import Network
import time
def input_ip_screen():
    font = pygame.font.SysFont("Arial", 36)
    input_text = ""
    active = True

    input_rect = pygame.Rect(WINDOW_WIDTH - 150, WINDOW_HEIGHT // 2 - 25, 300, 50)
    color_inactive = pygame.Color("gray")
    color_active = pygame.Color("white")
    color = color_active

    while active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    active = False
                    return input_text.strip() if input_text.strip() else "127.0.0.1"
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode

        screen = pygame.display.get_surface()
        screen.fill((0, 0, 0))

        # Vẽ ô nhập
        pygame.draw.rect(screen, color, input_rect, 2)
        text_surface = font.render(input_text, True, color)
        screen.blit(text_surface, (input_rect.x + 10, input_rect.y + 10))

        label = font.render("Enter IP host (Press ENTER)", True, "white")
        screen.blit(label, (WINDOW_WIDTH // 2 + 115, WINDOW_HEIGHT // 2 - 80))

        pygame.display.flip()

class Main:
    def __init__(self):
        # general
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH*2,WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('TetrisClone')
        #networking
        self.network = None
        self.player_id = None

        self.BOT = False
        self.play = None
        #shapes
        self.next_shapes = [choice (list(TETROMINOS.keys())) for _ in range(7)]
        self.opponent_next_shapes = [choice (list(TETROMINOS.keys())) for _ in range(7)]

        # player
        # Game components – tạm để None, sẽ tạo lại sau khi chọn chế độ
        self.game = None
        self.opponent_game = None
        self.score = None
        self.opponent_score = None
        self.preview = None
        self.opponent_preview = None
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
    def draw_opponent_grid(self, field_data):
        cell_size = CELL_SIZE
        x_offset = WINDOW_WIDTH + PADDING
        y_offset = PADDING
        # Vẽ lưới ngang và dọc
        for col in range(1, COLUMNS):
            x = x_offset + col * cell_size
            pygame.draw.line(self.display_surface, LINE_COLOR, (x, y_offset), (x, y_offset + ROWS * cell_size))
        for row in range(1, ROWS):
            y = y_offset + row * cell_size
            pygame.draw.line(self.display_surface, LINE_COLOR, (x_offset, y), (x_offset + COLUMNS * cell_size, y))

        # Vẽ viền quanh toàn bộ bảng
        board_rect = pygame.Rect(x_offset, y_offset, COLUMNS * cell_size, ROWS * cell_size)
        pygame.draw.rect(self.display_surface, LINE_COLOR, board_rect, 2, 2)
        # Vẽ các block đã rơi
        for y, row in enumerate(field_data):
            for x, cell in enumerate(row):
                if cell:
                    rect = pygame.Rect(
                        x_offset + x * cell_size,
                        y_offset + y * cell_size,
                        cell_size,
                        cell_size
                    )
                    pygame.draw.rect(self.display_surface, (150, 150, 150), rect)  # màu block
                    # pygame.draw.rect(self.display_surface, (50, 50, 50), rect, 1)  # viền ô

    def show_result(self, result_text):
        font = pygame.font.SysFont("Arial", 48)
        text_surface = font.render(result_text, True, "white")
        self.display_surface.blit(text_surface, (WINDOW_WIDTH // 2 - 150, WINDOW_HEIGHT // 2))
        pygame.display.update()
        pygame.time.delay(100)
    def run(self):
        game_running = True
        while game_running:
            playing = True
            selection = main_menu()

            if selection in ["single", "vsBot", "vsPlayer"]:
                self.play = selection
                self.BOT = (selection == "vsBot")

                self.game = Game(self.get_next_shape, self.update_score, bot_enable=False, x_offset=0)
                self.score = Score(x_offset=0)
                self.preview = Preview(x_offset=0)

                if self.play == "vsBot":
                    self.opponent_game = Game(self.get_opponent_next_shape, self.update_opponent_score,
                                              bot_enable=True, x_offset=WINDOW_WIDTH)
                    self.opponent_score = Score(x_offset=WINDOW_WIDTH)
                    self.opponent_preview = Preview(x_offset=WINDOW_WIDTH)
                elif self.play == "vsPlayer":
                    host_ip = input_ip_screen()
                    self.network = Network(host_ip)
                    self.opponent_game = Game(self.get_opponent_next_shape, self.update_opponent_score,
                                              bot_enable=False, x_offset=WINDOW_WIDTH, is_remoted=True)
                    self.opponent_score = Score(x_offset=WINDOW_WIDTH)
                    self.opponent_preview = Preview(x_offset=WINDOW_WIDTH)
                    try:
                        self.player_id = self.network.send("get")
                        print(f"Connected as Player {self.player_id}")
                    except:
                        print("Could not connect to server.")
                        # self.play = "single"
                    # Chờ đến khi cả 2 người chơi sẵn sàng
                    waiting = True
                    font = pygame.font.SysFont("Arial", 36)

                    while waiting:
                        my_state = self.game.get_state()
                        my_state["ready"] = True  # Đánh dấu đã sẵn sàng
                        opponent_state = self.network.send(my_state)

                        self.display_surface.fill("black")
                        text = font.render("Waiting for other player...", True, "white")
                        self.display_surface.blit(text, (WINDOW_WIDTH // 2 + 150, WINDOW_HEIGHT // 2 - 20))
                        pygame.display.update()

                        if opponent_state and opponent_state.get("both_ready"):
                            waiting = False

                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit()

                        time.sleep(0.5)
                while playing:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        elif event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_ESCAPE:
                                playing = False
                                break
                            if event.key == pygame.K_r:
                                self.game.reset()

                    # update and draw player
                    self.display_surface.fill(GRAY)
                    self.game.run()
                    self.score.run()
                    self.preview.run(self.next_shapes)
                    if self.play == "vsBot":
                        self.opponent_game.run()
                        self.opponent_score.run()
                        self.opponent_preview.run(self.opponent_next_shapes)
                    elif self.play == "vsPlayer":
                        my_state = self.game.get_state()
                        my_state["ready"] = True
                        opponent_state = self.network.send(my_state)
                        result = opponent_state.get("result", None)

                        if result in ["win", "lose", "draw"]:
                            result_text = {
                                "win": "You Win!",
                                "lose": "You Lose!",
                                "draw": "Draw!"
                            }[result]


                            # Hoặc dùng Pygame:
                            self.show_result(result_text)

                        if isinstance(opponent_state, dict) and "field_data" in opponent_state:
                            self.opponent_game.set_state(opponent_state)
                        self.opponent_game.run()
                        self.opponent_score.run()

                    pygame.display.update()
                    self.clock.tick(60)
            elif selection == "options":
                options()
            elif selection == "quit":
                game_running = False
                pygame.quit()
                sys.exit()

if __name__ == '__main__':
    main = Main()
    main.run()