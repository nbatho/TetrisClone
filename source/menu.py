import pygame, sys
from button import Button
import os

from setting import *

# pygame.init()

SCREEN = pygame.display.set_mode((WINDOW_WIDTH*2, WINDOW_HEIGHT))
pygame.display.set_caption("Menu")
BG = pygame.transform.scale(pygame.image.load("../graphics/Background.jpg"), (WINDOW_WIDTH*2, WINDOW_HEIGHT))
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


def paused_screen():
    clock = pygame.time.Clock()
    while True:

        # Văn bản và nút
        paused_text = get_font(70).render("PAUSED", True, "white")
        save_text = get_font(30).render("SAVE", True, "white")
        main_text = get_font(30).render("HOME", True, "white")
        reset_text = get_font(30).render("RESET", True, "white")
        paused_rect = paused_text.get_rect(center=(WINDOW_WIDTH , 300))
        main_rect = main_text.get_rect(center=(WINDOW_WIDTH -200, 400))
        save_rect = save_text.get_rect(center=(WINDOW_WIDTH, 400))
        reset_rect = reset_text.get_rect(center=(WINDOW_WIDTH + 200, 400))

        padding = 10
        pygame.draw.rect(SCREEN, (128,128,128,0), (305, 180, 600, 300))
        pygame.draw.rect(SCREEN, "white", (305, 180,600,300), width=2)
        pygame.draw.rect(SCREEN, "white", save_rect.inflate(padding, padding), width=2)
        pygame.draw.rect(SCREEN, "white", main_rect.inflate(padding, padding), width=2)
        pygame.draw.rect(SCREEN, "white", reset_rect.inflate(padding, padding), width=2)
        SCREEN.blit(paused_text, paused_rect)
        SCREEN.blit(save_text, save_rect)
        SCREEN.blit(main_text, main_rect)
        SCREEN.blit(reset_text, reset_rect)


        # Resume bằng ESC
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "resume"

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if save_rect.collidepoint(event.pos):
                    return "save"
                elif main_rect.collidepoint(event.pos):
                    return "home"
                elif reset_rect.collidepoint(event.pos):
                    return "reset"

        pygame.display.update()
        clock.tick(60)

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
