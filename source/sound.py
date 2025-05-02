import os
import pygame

class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.music_landing = pygame.mixer.Sound("../sounds/landing.wav")
        self.line_clear = pygame.mixer.Sound("../sounds/line_clear.mp3")
    def music_landing(self):
        self.music_landing.play()
    def music_line_clear(self):
        self.line_clear.play()
    def music_theme(self):
        pygame.mixer.music.load("../sounds/sounds_theme.mp3")
        pygame.mixer.music.play(-1)  # Lặp vô hạn

    def stop_music(self):
        pygame.mixer.music.stop()