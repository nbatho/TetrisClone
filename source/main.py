from setting import *
from leaderboard import save_score, draw_leaderboard
from game import Game
from score import Score
from preview import Preview
from random import choice
from network import Network
import time
from sound import *
from menu import *


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
                elif event.key == pygame.K_ESCAPE:
                    return None
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

def get_player_name(screen, clock, font):
    input_box = pygame.Rect(440, 300, 400, 60)
    color = pygame.Color('dodgerblue2')
    text = ''
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if text.strip() != '':
                        return text.strip()
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    if len(text) < 15:
                        text += event.unicode

        # Giao diện nền đen
        screen.fill((0, 0, 0))  # màu đen

        # Tiêu đề
        title_surface = font.render("Enter your name:", True, pygame.Color('white'))
        screen.blit(title_surface, title_surface.get_rect(center=(640, 200)))

        # Khung nhập tên
        pygame.draw.rect(screen, color, input_box, 2)
        txt_surface = font.render(text, True, pygame.Color("white"))
        screen.blit(txt_surface, (input_box.x + 10, input_box.y + 15))

        pygame.display.flip()
        clock.tick(30)

class Main:
    def __init__(self):
        # general
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH*2,WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('TetrisClone')
        # Sound
        pygame.mixer.init()
        self.sound = SoundManager()
        pygame.mixer.music.set_volume(MASTER_VOLUME)
        self.sound.music_theme()
        #Player
        self.player_name = "Player"
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
                if self.play == 'single': 
                    offset = WINDOW_WIDTH//2 + 50
                    self.player_name = get_player_name(self.display_surface, self.clock, pygame.font.SysFont("Arial", 36))
                else: offset = 0
                self.game = Game(self.get_next_shape, self.update_score, bot_enable=False, x_offset=offset)
                self.score = Score(x_offset=offset)
                self.preview = Preview(x_offset=offset)
                if self.play == "vsBot":
                    self.opponent_game = Game(self.get_opponent_next_shape, self.update_opponent_score,
                                              bot_enable=True, x_offset=WINDOW_WIDTH)
                    self.opponent_score = Score(x_offset=WINDOW_WIDTH)
                    self.opponent_preview = Preview(x_offset=WINDOW_WIDTH)
                elif self.play == "vsPlayer":
                    host_ip = input_ip_screen()
                    if host_ip is None:
                        self.play = None
                        playing = False
                        continue 
                    else:
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

                            if isinstance(opponent_state, dict)  and opponent_state.get("both_ready"):
                                waiting = False

                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    pygame.quit()
                                    sys.exit()
                                if event.type == pygame.KEYDOWN:
                                    if event.key == pygame.K_ESCAPE:
                                        waiting = False
                                        playing = False
                                       
                        time.sleep(0.5)
                while playing:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        elif event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_ESCAPE:
                                if self.play == "vsPlayer" and hasattr(self, "network"):
                                    try:
                                        self.network.send("exit")
                                        self.network.client.close()
                                    except:
                                        pass
                                    playing = False

                                if self.play in ['single','vsBot']:
                                    print(self.game.paused)
                                    if not self.game.paused:
                                        self.game.pause()
                                        result = paused_screen()

                                        if result == "resume":
                                            self.game.resume()
                                        elif result == "save":
                                            save_score(self.player_name, self.score.score)
                                            print("Saving game...")  # or call self.game.save()
                                            draw_leaderboard(self.display_surface, pygame.font.SysFont("Arial", 24))
                                            self.game.pause()
                                            playing = False
                                        elif result == "home":
                                            print("Returning to main menu...")
                                            playing = False  # Or however you switch to main menu
                                        elif result == "reset":
                                            print("Resetting game...")
                                            self.game.reset()
                                        self.game.resume()

                    # update and draw player
                    self.display_surface.fill(GRAY)
                    # if self.play == "single" and self.game.game_over:
                    # save_score(self.player_name, self.score.score)
                    draw_leaderboard(self.display_surface, pygame.font.SysFont("Arial", 24))
                    #     playing = False
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
                        if opponent_state and isinstance(opponent_state, dict):
                            result = opponent_state.get("result", None)
                            if result in ["win", "lose", "draw"]:
                                result_text = {
                                    "win": "You Win!",
                                    "lose": "You Lose!",
                                    "draw": "Draw!"
                                }[result]
                                self.show_result(result_text)

                        if isinstance(opponent_state, dict) and "field_data" in opponent_state:
                            self.opponent_game.set_state(opponent_state)
                        self.opponent_game.run()
                        self.opponent_score.run()

                    pygame.display.update()
                    self.clock.tick(60)
                if self.play == "single" and self.game.game_over:
                    save_score(self.player_name, self.score.score)
                    # Hiển thị leaderboard
                    self.display_surface.fill("black")
                    draw_leaderboard(self.display_surface, pygame.font.SysFont("Arial", 24))
                    playing = False
                    pygame.display.update()
                    # pygame.time.wait(5000)  # Hiển thị 5 giây
                    waiting = True
                    while waiting:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit()
                            elif event.type == pygame.KEYDOWN:
                                if event.key in [pygame.K_RETURN, pygame.K_ESCAPE]:
                                    waiting = False

            elif selection == "options":
                options()
            elif selection == "quit":
                game_running = False
                pygame.quit()
                sys.exit()

if __name__ == '__main__':
    main = Main()   
    main.run()