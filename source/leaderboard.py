import json
import os
import pygame

LEADERBOARD_FILE = "leaderboard.json"

def load_leaderboard():
    if not os.path.exists(LEADERBOARD_FILE):
        return []
    with open(LEADERBOARD_FILE, "r") as f:
        return json.load(f)

def save_score(name, score):
    leaderboard = load_leaderboard()
    leaderboard.append({"name": name, "score": score})
    leaderboard.sort(key=lambda x: x["score"], reverse=True)
    leaderboard = leaderboard[:10]  # chỉ giữ top 5
    with open(LEADERBOARD_FILE, "w") as f:
        json.dump(leaderboard, f, indent=4)

def draw_leaderboard(surface, font):
    leaderboard = load_leaderboard()
    title = font.render("TOP 10", True, "white")
    surface.blit(title, (30, 30))
    for i, entry in enumerate(leaderboard):
        text = f"{i+1}. {entry['name'][:10]}: {entry['score']}"
        line_surface = font.render(text, True, "white")
        surface.blit(line_surface, (30, 70 + i * 30))



def render_leaderboard_surface(font):
    surface = pygame.Surface((600, 600), pygame.SRCALPHA)
    leaderboard = load_leaderboard()
    title = font.render("TOP 10", True, "white")
    surface.blit(title, (20, 20))
    
    for i, entry in enumerate(leaderboard):
        text = f"{i+1}. {entry['name'][:10]}: {entry['score']}"
        line_surface = font.render(text, True, "white")
        surface.blit(line_surface, (20, 60 + i * 30))
    
    return surface