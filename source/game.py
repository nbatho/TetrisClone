from setting import *
from random import choice
from timer import Timer
import numpy as np
class Game:
    def __init__(self, get_next_shape, update_score):
        #general
        self.surface = pygame.Surface((GAME_WIDTH,GAME_HEIGHT))
        self.display_surface = pygame.display.get_surface()
        self.rect = self.surface.get_rect(topleft = (PADDING,PADDING))
        self.sprites = pygame.sprite.Group()
        self.get_next_shape = get_next_shape
        self.update_score = update_score
        self.game_over = False
        #bot
        self.bot_enable = True
        # lines
        self.line_surface = self.surface.copy()
        self.line_surface.fill((0,255,0))
        self.line_surface.set_colorkey((0,255,0))
        self.line_surface.set_alpha(120)

        # tetrominos
        self.field_data = [[0 for x in range(COLUMNS)] for y in range(ROWS)]
        self.tetrominos = Tetromino(
            choice(list(TETROMINOS.keys())),
            self.sprites,
            self.create_new_tetromino,
            self.field_data,
            self.game_over,
        )

        # timer
        self.down_speed = UPDATE_START_SPEED
        self.down_speed_faster = self.down_speed * 0.3
        self.down_pressed = False
        self.timers = {
            'vertical move': Timer(self.down_speed, True,self.move_down),
            'horizontal move': Timer(MOVE_WAIT_TIME),
            'rotate': Timer(ROTATE_WAIT_TIME),
            'hard drop': Timer(200),
            'print':Timer(1000),
            'calculate score': Timer(750),
        }
        self.timers['vertical move'].activate()

        # score
        self.current_level = 1
        self.current_score = 0
        self.current_lines = 0
    def calculate_score(self, num_lines):
        self.current_lines += num_lines
        self.current_score += SCORE_DATA[num_lines] * self.current_level

        # every 10 lines += level by 1
        if self.current_lines / 10 > self.current_level:
            self.current_level += 1
            self.down_speed *= 0.75
            self.down_speed_faster = self.down_speed * 0.3
            self.timers['vertical move'].duration = self.down_speed
        self.update_score(self.current_lines,self.current_score,self.current_level)
    def create_new_tetromino(self):

        self.check_finished_rows()
        self.tetrominos = Tetromino(
            self.get_next_shape(),
            self.sprites,
            self.create_new_tetromino,
            self.field_data,
            self.game_over,
    )

    def cal_hoes(self, matrix):
        holes = 0
        for j in range(COLUMNS):
            block_found = False
            for i in range(ROWS):
                if matrix[i][j] != 0:
                    block_found = True
                elif matrix[i][j] == 0 and block_found:
                    holes += 1
        return holes
    def cal_complete_line(self,matrix):
        complete_line = 0
        for i in range(ROWS):
            cnt = 0
            for j in range(COLUMNS):
                if matrix[i][j] != 0:
                    cnt +=1
            if cnt == COLUMNS:
                complete_line += 1
        return complete_line
    def evaluate_board(self,matrix):
        height = 0
        bumpiness = 0
        hole = self.cal_hoes(matrix)
        complete_line = self.cal_complete_line(matrix)
        ls_height = [0]*COLUMNS
        a = -0.510066
        b = 0.760666
        c = -0.35663
        d = -0.184483
        for j in range(COLUMNS):
            for i in range(ROWS):
                if matrix[i][j] != 0:
                    ls_height[j] = ROWS - i
                    height += ROWS - i
                    break
        for i in range(len(ls_height) - 1):
            bumpiness += abs(ls_height[i] - ls_height[i+1])

        return height * a + complete_line * b + hole * c + bumpiness * d

    def all_possible_move(self):
        if not self.timers['calculate score'].active:
            best_score = float('-inf')
            best_state = None
            all_states = self.tetrominos.generate_all_states()
            for data, rotation in all_states:
                field_data_clone = [row[:] for row in self.field_data]
                positions = data.copy()  # Tạo bản sao để không ảnh hưởng đến dữ liệu gốc

                # Rơi xuống vị trí thấp nhất
                while True:
                    new_positions = []
                    can_move = True

                    for pos in positions:
                        x, y = int(pos.x), int(pos.y) + 1

                        if y >= len(field_data_clone) or (
                                0 <= x < len(field_data_clone[0]) and
                                0 <= y < len(field_data_clone) and
                                field_data_clone[y][x] != 0):
                            can_move = False
                            break
                        new_positions.append(pygame.math.Vector2(x, y))

                    if not can_move:
                        break

                    positions = new_positions

                # Cập nhật field_data_clone với trạng thái mới
                for pos in positions:
                    x, y = int(pos.x), int(pos.y)
                    if 0 <= y < len(field_data_clone) and 0 <= x < len(field_data_clone[0]):
                        field_data_clone[y][x] = 1

                # Tính điểm số cho trạng thái hiện tại
                score = self.evaluate_board(field_data_clone)

                # Lưu trạng thái có điểm số tốt nhất
                if score > best_score:
                    best_score = score
                    best_state = (positions, rotation)  # Lưu cả vị trí và số lần xoay

                # Debug
                # for i in range(ROWS):
                #     for j in range(COLUMNS):
                #         print(field_data_clone[i][j], end='')
                #     print()
                # print()

            # print(f'Best Score: {best_score}')

            if best_state:
                # Di chuyển khối đến vị trí có điểm số cao nhất
                self.move_to_best_position(best_state)
            # print(f'Moving to best position: {best_state}')
            self.timers['calculate score'].activate()

    def move_to_best_position(self, best_state):
        """Di chuyển khối đến vị trí tối ưu đã chọn"""
        best_position, best_rotation = best_state  # Giải nén thông tin
        current_position = [(block.pos.x, block.pos.y) for block in self.tetrominos.blocks]
        target_position = [(block.x, block.y) for block in best_position]

        # Xoay trước
        for _ in range(best_rotation):
            self.tetrominos.rotate()

        # Tính toán số lần di chuyển trái/phải sau khi xoay
        x_offset = target_position[0][0] - self.tetrominos.blocks[0].pos.x

        if x_offset > 0:
            for _ in range(round(x_offset)):
                self.tetrominos.move_horizontal(1)  # Di chuyển sang phải
        elif x_offset < 0:
            for _ in range(abs(round(x_offset))):
                self.tetrominos.move_horizontal(-1)  # Di chuyển sang trái

        # Thả khối xuống vị trí tốt nhất
        self.tetrominos.hard_drop()
    def timer_update(self):
        for timer in self.timers.values():
            timer.update()
    def move_down(self):
        self.tetrominos.move_down()
    def draw_grid(self):
        for col in range(1,COLUMNS):
            x = col * CELL_SIZE
            pygame.draw.line(self.line_surface,LINE_COLOR,(x,0),(x,self.surface.get_height()) )
        for row in range(1,ROWS):
            y = row * CELL_SIZE
            pygame.draw.line(self.line_surface,LINE_COLOR,(0,y),(self.surface.get_width(),y) )

        self.surface.blit(self.line_surface,(0,0))
    def input(self):
        keys = pygame.key.get_pressed()

        if not self.timers['horizontal move'].active:
            if keys[pygame.K_LEFT]:
                self.tetrominos.move_horizontal(-1)
                self.timers['horizontal move'].activate()
            if keys[pygame.K_RIGHT]:
                self.tetrominos.move_horizontal(1)
                self.timers['horizontal move'].activate()

        # hard drop
        if not self.timers['hard drop'].active:
            if keys[pygame.K_SPACE] and not self.game_over:
                self.tetrominos.hard_drop()
                self.timers['hard drop'].activate()
        # check for rotation
        if not self.timers['rotate'].active:
            if keys[pygame.K_UP]:
                self.tetrominos.rotate()
                self.timers['rotate'].activate()
        # down speedup
            # pressing
        if not self.down_pressed and keys[pygame.K_DOWN]:
            self.down_pressed = True
            self.timers['vertical move'].duration = self.down_speed_faster
            # realse
        if self.down_pressed and not keys[pygame.K_DOWN]:
            self.down_pressed = False
            self.timers['vertical move'].duration = self.down_speed
    def check_finished_rows(self):

        # get the full row indexes
        delete_rows = []
        for i,row in enumerate(self.field_data):
            if all(row):
                delete_rows.append(i)
        if delete_rows:
            for delete_row in delete_rows:

                # delete full row
                for block in self.field_data[delete_row]:
                    block.kill()
                # move down blocks
                for row in self.field_data:
                    for block in row:
                        if block and block.pos.y < delete_row:
                            block.pos.y += 1
            # rebuild the filed data
            self.field_data = [[0 for x in range(COLUMNS)] for y in range(ROWS)]
            for block in self.sprites:
                self.field_data[int(block.pos.y)][int(block.pos.x)] = block

            # update score
            self.calculate_score(len(delete_rows))

    def reset(self):
        self.field_data = [[0 for _ in range(COLUMNS)] for _ in range(ROWS)]
        self.sprites.empty()
        self.game_over = False
        self.current_level = 1
        self.current_score = 0
        self.current_lines = 0
        self.timers['vertical move'].duration = UPDATE_START_SPEED
        self.tetrominos = Tetromino(
            self.get_next_shape(),
            self.sprites,
            self.create_new_tetromino,
            self.field_data,
            self.game_over
        )
        self.update_score(self.current_lines, self.current_score, self.current_level)
    def run(self):
        #update

        self.input()
        self.timer_update()
        self.sprites.update()
        if self.bot_enable:
            self.all_possible_move()
        # drawing
        self.surface.fill(GRAY)
        self.sprites.draw(self.surface)
        self.draw_grid()
        self.display_surface.blit(self.surface,(PADDING,PADDING))
        pygame.draw.rect(self.display_surface,LINE_COLOR,self.rect,2,2)


class Tetromino():
    def __init__(self,shape,group, create_new_tetromino, field_data,game_over):
        # setup
        self.shape = shape
        self.block_positions = TETROMINOS[shape]['shape']
        self.color = TETROMINOS[shape]['color']
        self.create_new_tetromino = create_new_tetromino
        self.field_data = field_data
        self.game_over = game_over
        # create blocks
        self.blocks = [Block(group,pos,self.color) for pos in self.block_positions]

    def generate_all_states(self):
        states = []
        original_position = [block.pos.copy() for block in self.blocks]

        for rotation in range(4):  # 4 rotations
            current_blocks = [block.pos.copy() for block in self.blocks]

            left_most = int(min(block.x for block in current_blocks))
            right_most = int(max(block.x for block in current_blocks))

            for shift in range(-left_most, 10 - right_most):  # Xét tất cả vị trí ngang có thể
                moved_blocks = [pygame.math.Vector2(block.x + shift, block.y) for block in current_blocks]
                states.append((moved_blocks, rotation))  # Lưu cả vị trí và số lần xoay

            # Xoay để chuẩn bị cho vòng lặp tiếp theo
            if rotation < 3:  # Không cần xoay sau lần lặp cuối
                self.rotate()

        # Reset về trạng thái ban đầu
        for i, block in enumerate(self.blocks):
            block.pos = original_position[i]

        return states
    # rotate
    def rotate(self):
        if self.shape != 'O':
            pivot_pos = self.blocks[0].pos
            # new block possition
            new_block_positions = [block.rotate(pivot_pos) for block in self.blocks]
            # collision
            for pos in new_block_positions:
                # check horizontal
                if pos.x < 0 or pos.x >= COLUMNS: return
                # check field
                if self.field_data[int(pos.y)][int(pos.x)]: return
                # check floor
                if pos.y >= ROWS: return
            for i,block in enumerate(self.blocks):
                block.pos = new_block_positions[i]
    # collisions
    def next_move_horizontal_collide(self,blocks,amount):
        collision_list = [block.horizontal_collide(int(block.pos.x + amount), self.field_data) for block in self.blocks]
        return True if any(collision_list) else False
    def next_move_vertical_collide(self,blocks,amount):
        collision_list = [block.vertical_collide(int(block.pos.y + amount), self.field_data) for block in self.blocks]
        return True if any(collision_list) else False
    # movement
    def move_down(self):
        if not self.next_move_vertical_collide(self.blocks,1):
            for block in self.blocks:
                block.pos.y += 1
        else:
            for block in self.blocks:
                self.field_data[int(block.pos.y)][int(block.pos.x)] = block
            self.create_new_tetromino()
    def hard_drop(self):
        while not self.next_move_vertical_collide(self.blocks, 1):
            for block in self.blocks:
                block.pos.y += 1

        for block in self.blocks:
            self.field_data[int(block.pos.y)][int(block.pos.x)] = block
        if self.create_new_tetromino:
            self.create_new_tetromino()
    def move_horizontal(self,amount):
        if not self.next_move_horizontal_collide(self.blocks, amount):
            for block in self.blocks:
                block.pos.x += amount

    #endgame
    def check_game_over(self):
        min_height = 30
        for block in self.blocks:
            min_height = min(min_height,block.pos.y)
            if min_height <= 0:
                self.game_over = True
                return True
        return False


class Block(pygame.sprite.Sprite):
    def __init__(self,group,pos,color):
        #general
        super().__init__(group)
        self.image = pygame.Surface((CELL_SIZE,CELL_SIZE))
        self.image.fill(color)
        # position
        self.pos = pygame.Vector2(pos) + BLOCK_OFFSET
        self.rect = self.image.get_rect(topleft = self.pos * CELL_SIZE)

    def horizontal_collide(self,x, filed_data):
        if not 0 <= x < COLUMNS:
            return True
        if filed_data[int(self.pos.y)][x]:
            return True
    def vertical_collide(self,y, filed_data):
        if y >= ROWS:
            return True
        if y >= 0 and filed_data[y][int(self.pos.x)]:
            return True
    def rotate(self,pivot_pos):
        return pivot_pos + (self.pos - pivot_pos).rotate(90)
    def update(self):
        self.rect.topleft = self.pos * CELL_SIZE