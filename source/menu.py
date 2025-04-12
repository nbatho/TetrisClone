import pygame, sys
from button import Button
import os

# pygame.init()

SCREEN = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Menu")

BG = pygame.transform.scale(pygame.image.load("../graphics/Background.jpg"), (1280, 720))
def play_mode_menu():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        TITLE_TEXT = get_font(70).render("Game Mode", True, "#b68f40")
        TITLE_RECT = TITLE_TEXT.get_rect(center=(640, 100))
        SCREEN.blit(TITLE_TEXT, TITLE_RECT)

        SINGLE_BUTTON = Button(
            image=pygame.image.load("../graphics/Play Rect.png"),
            pos=(640, 220), text_input="SINGLE", font=get_font(40),
            base_color="#d7fcd4", hovering_color="White"
        )
        BOT_BUTTON = Button(
            image=pygame.image.load("../graphics/BattleAI Rect.png"),
            pos=(640, 340), text_input="vsBOT", font=get_font(40),
            base_color="#d7fcd4", hovering_color="White"
        )
        PLAYER_BUTTON = Button(
            image=pygame.image.load("../graphics/BattleAI Rect.png"),
            pos=(640, 460), text_input="vsPLAYER", font=get_font(40),
            base_color="#d7fcd4", hovering_color="White"
        )
        BACK_BUTTON = Button(
            image=pygame.image.load("../graphics/Quit Rect.png"),
            pos=(640, 580), text_input="BACK", font=get_font(40),
            base_color="#d7fcd4", hovering_color="White"
        )

        for button in [SINGLE_BUTTON, BOT_BUTTON, PLAYER_BUTTON, BACK_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if SINGLE_BUTTON.checkForInput(MENU_MOUSE_POS):
                    return "single"
                if BOT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    return "vsBot"
                if PLAYER_BUTTON.checkForInput(MENU_MOUSE_POS):
                    return "vsPlayer"
                if BACK_BUTTON.checkForInput(MENU_MOUSE_POS):
                    return "menu"

        pygame.display.update()

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("../graphics/font.ttf", size)

def play():
    pass

def options():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("white")

        # OPTIONS_BACK = Button(
        #     image=None, pos=(100, 50), 
        #     text_input="BACK", font=get_font(30), 
        #     base_color="Black", hovering_color="Green"
        # )

        # OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        # OPTIONS_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # elif event.type == pygame.MOUSEBUTTONDOWN:
            #     if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
            #         return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                
        pygame.display.update()

def main_menu():
    selected_index = 0
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        PLAY_BUTTON = Button(
            image=pygame.image.load("../graphics/Play Rect.png"), 
            pos=(640, 250), text_input="PLAY", font=get_font(50), 
            base_color="#d7fcd4", hovering_color="White"
            )
        OPTIONS_BUTTON = Button(
            image=pygame.image.load("../graphics/BattleAI Rect.png"), 
            pos=(640, 400), text_input="OPTIONS", font=get_font(50), 
            base_color="#d7fcd4", hovering_color="White"
            )
        QUIT_BUTTON = Button(
            image=pygame.image.load("../graphics/Quit Rect.png"), 
            pos=(640, 550), text_input="QUIT", font=get_font(50), 
            base_color="#d7fcd4", hovering_color="White"
            )

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    return play_mode_menu()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    return "options"
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
