from setting import *
from random import choice
from timer import Timer
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

        # bots
        self.bot_enabled = True

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
        self.down_speed_faster = self.down_speed * 0.5
        self.down_pressed = False
        self.timers = {
            'vertical move': Timer(self.down_speed, True,self.move_down),
            'horizontal move': Timer(MOVE_WAIT_TIME),
            'rotate': Timer(ROTATE_WAIT_TIME),
            'hard drop': Timer(200),
            'restart game': Timer(200),
        }
        self.timers['vertical move'].activate()

        # score
        self.current_level = 1
        self.current_score = 0
        self.current_lines = 0

    def evaluate_board(self,field_data):
        simulated_field = [row[:] for row in field_data]
        holes = 0
        bumpiness = 0
        heights = [0] * COLUMNS
        for x in range(COLUMNS):
            block_found = False
            for y in range(ROWS):
                if (simulated_field[y][x] != 0):
                    if not block_found:
                        heights[x] = ROWS - y
                        block_found = True
                    elif block_found:
                        holes += 1
        aggregate_height = sum(heights)
        for idx in range(COLUMNS - 1):
            bumpiness += abs(heights[idx] - heights[idx + 1])
        lines_cleared = sum(1 for row in simulated_field if all(row))

        return lines_cleared*50 - aggregate_height*5 - holes*20 - bumpiness*2

    def new_game(self):
        self.game_over = False
        # Clear the screen
        self.display_surface.fill((0, 0, 0))  # Fill screen with black

        # Reset game variables
        self.field_data = [[0 for x in range(COLUMNS)] for y in range(ROWS)]
        self.sprites.empty()

        self.tetrominos = Tetromino(
            choice(list(TETROMINOS.keys())),
            self.sprites,
            self.create_new_tetromino,
            self.field_data,
            self.game_over
        )

        # Reset timer
        self.down_speed = UPDATE_START_SPEED
        self.down_speed_faster = self.down_speed * 0.5
        self.down_pressed = False
        self.timers = {
            'vertical move': Timer(self.down_speed, True, self.move_down),
            'horizontal move': Timer(MOVE_WAIT_TIME),
            'rotate': Timer(ROTATE_WAIT_TIME),
            'hard drop': Timer(200),
            'restart game': Timer(200),
        }
        self.timers['vertical move'].activate()

        # Reset score
        self.current_level = 1
        self.current_score = 0
        self.current_lines = 0
        self.update_score(self.current_lines,self.current_score,self.current_level)

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

        # reset game
        if not self.timers['restart game'].active:
            if keys[pygame.K_r]:
                self.new_game()
                self.timers['restart game'].activate()
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

    def run(self):
        #update
        self.input()

        # bot
        if self.bot_enabled:
            self.tetrominos.generate_all_moves()

        self.timer_update()
        self.sprites.update()
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



    # collisions
    def next_move_horizontal_collide(self,blocks,amount):
        collision_list = [block.horizontal_collide(int(block.pos.x + amount), self.field_data) for block in self.blocks]
        return True if any(collision_list) else False
    def next_move_vertical_collide(self,blocks,amount):
        collision_list = [block.vertical_collide(int(block.pos.y + amount), self.field_data) for block in self.blocks]
        return True if any(collision_list) else False

    # movement
    def move_down(self):
        if self.game_over:
            return
        if not self.next_move_vertical_collide(self.blocks,1):
            for block in self.blocks:
                block.pos.y += 1
        else:
            for block in self.blocks:
                self.field_data[int(block.pos.y)][int(block.pos.x)] = block

            if self.check_game_over():
                print("Game Over, Press R to restart")
                return
            else: self.create_new_tetromino()
    def move_horizontal(self,amount):
        if not self.next_move_horizontal_collide(self.blocks,amount):
            for block in self.blocks:
                block.pos.x += amount

    def hard_drop(self):
        if self.game_over:
            return
        while not self.next_move_vertical_collide(self.blocks, 1):
            for block in self.blocks:
                block.pos.y += 1

        for block in self.blocks:
            self.field_data[int(block.pos.y)][int(block.pos.x)] = block
        if self.check_game_over():
            print("Game Over, Press R to restart")
            return
        else:
            self.create_new_tetromino()

    def check_game_over(self):
        min_height = 30
        for block in self.blocks:
            min_height = min(min_height,block.pos.y)
            if min_height <= 0:
                self.game_over = True
                return True
        return False

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
                block.pos = new_block_positions [i]

    def generate_all_moves(self):
        # """ Generate all possible moves (rotations + horizontal positions) for the current Tetromino """
        # possible_moves = []
        # original_positions = [block.pos.copy() for block in self.blocks]  # Save original position
        #
        # for rotation in range(4):  # Try 0°, 90°, 180°, 270°
        #     for x_offset in range(-COLUMNS, COLUMNS):  # Try moving left and right
        #         # Move piece horizontally
        #         min_x = min(block.pos.x for block in self.blocks)
        #         move_distance = x_offset - min_x
        #         self.move_horizontal(move_distance)
        #
        #         # Hard drop the piece
        #         self.hard_drop()
        #
        #         # Evaluate the board after placing the Tetromino
        #         score = self.evaluate_board(self.field_data)
        #
        #         # Store move data
        #         move_data = {
        #             "rotation": rotation,
        #             "x_offset": x_offset,
        #             "score": score
        #         }
        #         possible_moves.append(move_data)
        #
        #         # Reset to original position before trying next move
        #         for i, block in enumerate(self.blocks):
        #             block.pos = original_positions[i]
        #
        #     self.rotate()  # Try next rotation
        #
        # return possible_moves  # Return all tested moves
        pass


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