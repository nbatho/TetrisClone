import pygame, sys
from button import Button
import os

SCREEN = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Menu")

BG = pygame.transform.scale(pygame.image.load("E:/Code/Python/Project/TetrisClone/graphics/Background.jpg"), (1280, 720))
def play_mode_menu():
    selected_index = 0
    buttons = []

    SINGLE_BUTTON = Button(
        image=pygame.image.load("E:/Code/Python/Project/TetrisClone/graphics/Play Rect.png"),
        pos=(640, 220), text_input="SINGLE", font=get_font(40),
        base_color="#d7fcd4", hovering_color="White"
    )
    BOT_BUTTON = Button(
        image=pygame.image.load("E:/Code/Python/Project/TetrisClone/graphics/BattleAI Rect.png"),
        pos=(640, 340), text_input="vsBOT", font=get_font(40),
        base_color="#d7fcd4", hovering_color="White"
    )
    PLAYER_BUTTON = Button(
        image=pygame.image.load("E:/Code/Python/Project/TetrisClone/graphics/BattleAI Rect.png"),
        pos=(640, 460), text_input="vsPLAYER", font=get_font(40),
        base_color="#d7fcd4", hovering_color="White"
    )
    BACK_BUTTON = Button(
        image=pygame.image.load("E:/Code/Python/Project/TetrisClone/graphics/Quit Rect.png"),
        pos=(640, 580), text_input="BACK", font=get_font(40),
        base_color="#d7fcd4", hovering_color="White"
    )

    buttons = [SINGLE_BUTTON, BOT_BUTTON, PLAYER_BUTTON, BACK_BUTTON]

    while True:
        SCREEN.blit(BG, (0, 0))
        TITLE_TEXT = get_font(70).render("Game Mode", True, "#b68f40")
        TITLE_RECT = TITLE_TEXT.get_rect(center=(640, 100))
        SCREEN.blit(TITLE_TEXT, TITLE_RECT)

        for i, button in enumerate(buttons):
            if i == selected_index:
                button.text = button.font.render(button.text_input, True, button.hovering_color)
            else:
                button.text = button.font.render(button.text_input, True, button.base_color)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_index = (selected_index - 1) % len(buttons)
                elif event.key == pygame.K_DOWN:
                    selected_index = (selected_index + 1) % len(buttons)
                elif event.key == pygame.K_RETURN:
                    selected_button = buttons[selected_index].text_input
                    if selected_button == "SINGLE":
                        return "single"
                    elif selected_button == "vsBOT":
                        return "vsBot"
                    elif selected_button == "vsPLAYER":
                        return "vsPlayer"
                    elif selected_button == "BACK":
                        return "menu"
        pygame.display.update()

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("E:/Code/Python/Project/TetrisClone/graphics/font.ttf", size)

def play():
    pass

def options():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("white")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                
        pygame.display.update()

def main_menu():
    selected_index = 0
    buttons = []

    PLAY_BUTTON = Button(
        image=pygame.image.load("E:/Code/Python/Project/TetrisClone/graphics/Play Rect.png"), 
        pos=(640, 250), text_input="PLAY", font=get_font(50), 
        base_color="#d7fcd4", hovering_color="White"
    )
    OPTIONS_BUTTON = Button(
        image=pygame.image.load("E:/Code/Python/Project/TetrisClone/graphics/BattleAI Rect.png"), 
        pos=(640, 400), text_input="OPTIONS", font=get_font(50), 
        base_color="#d7fcd4", hovering_color="White"
    )
    QUIT_BUTTON = Button(
        image=pygame.image.load("E:/Code/Python/Project/TetrisClone/graphics/Quit Rect.png"), 
        pos=(640, 550), text_input="QUIT", font=get_font(50), 
        base_color="#d7fcd4", hovering_color="White"
    )

    buttons = [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]

    while True:
        SCREEN.blit(BG, (0, 0))
        MENU_TEXT = get_font(100).render("MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))
        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for i, button in enumerate(buttons):
            if i == selected_index:
                button.text = button.font.render(button.text_input, True, button.hovering_color)
            else:
                button.text = button.font.render(button.text_input, True, button.base_color)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_index = (selected_index - 1) % len(buttons)
                elif event.key == pygame.K_DOWN:
                    selected_index = (selected_index + 1) % len(buttons)
                elif event.key == pygame.K_RETURN:
                    selected_button = buttons[selected_index].text_input
                    if selected_button == "PLAY":
                        return play_mode_menu()
                    elif selected_button == "OPTIONS":
                        return "options"
                    elif selected_button == "QUIT":
                        pygame.quit()
                        sys.exit()
        pygame.display.update()
