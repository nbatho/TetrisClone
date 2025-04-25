import os
import pygame

class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.music_landing = pygame.mixer.Sound("E:/Code/Python/Project/TetrisClone/sounds/landing.wav")
        # self.gameover_sound = pygame.mixer.Sound("F:/Project/[Python] Lap trinh game/TetrisClone/sounds/gameover.wav")

    # def music_gameover(self):
    #     self.gameover_sound.play()

    def music_landing(self):
        self.music_landing.play()

    def music_theme(self):
        pygame.mixer.music.load("E:/Code/Python/Project/TetrisClone/sounds/sounds_theme.mp3")
        pygame.mixer.music.play(-1)  # Lặp vô hạn

    def stop_music(self):
        pygame.mixer.music.stop()
