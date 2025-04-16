import os
import pygame

class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.winning_sound = pygame.mixer.Sound("F:/Project/[Python] Lap trinh game/TetrisClone/sounds/success.wav")
        self.gameover_sound = pygame.mixer.Sound("F:/Project/[Python] Lap trinh game/TetrisClone/sounds/gameover.wav")

    def music_win(self):
        self.winning_sound.play()
    def music_gameover(self):
        self.gameover_sound.play()

    def music_theme(self):
        pygame.mixer.music.load("F:/Project/[Python] Lap trinh game/TetrisClone/sounds/theme.mp3")
        pygame.mixer.music.play(-1)  # Lặp vô hạn

    def stop_music(self):
        pygame.mixer.music.stop()