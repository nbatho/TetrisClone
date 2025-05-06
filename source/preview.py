from setting import *
from pygame.image import load
class Preview:
    def __init__(self,x_offset = 0):
        # general
        self.display_surface = pygame.display.get_surface()
        self.surface = pygame.Surface((SIDEBAR_WIDTH,GAME_HEIGHT * SCORE_HEIGHT_FRACTION - PADDING))
        self.rect = self.surface.get_rect(topright = (x_offset + WINDOW_WIDTH - PADDING,PADDING))

        # shapes
        self.shape_surfaces = {shape:load(f'C:/Users/Dell/Desktop/TetrisClone/TetrisClone/graphics/{shape}.png').convert_alpha() for shape in TETROMINOS.keys()}

        # image position data
        self.increment_height = self.surface.get_height()
    def display_pieces(self,shapes):
        for i,shape in enumerate(shapes):
            shape_surface = self.shape_surfaces[shape]
            x = self.surface.get_width() // 2
            y =  self.increment_height // 2 + i*self.increment_height
            rect = shape_surface.get_rect(center = (x,y))
            self.surface.blit(shape_surface,rect)
    def run(self, next_shapes):
        self.surface.fill(GRAY)
        self.display_pieces(next_shapes)
        self.display_surface.blit(self.surface,self.rect)
        pygame.draw.rect(self.display_surface, LINE_COLOR, self.rect,2,2)