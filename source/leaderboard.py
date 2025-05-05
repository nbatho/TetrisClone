import pygame
import json
import os

LEADERBOARD_FILE = "leaderboard.json"
MAX_ENTRIES = 5
MODE = "single"  # chỉ hỗ trợ chế độ single

def load_leaderboard():
    if not os.path.exists(LEADERBOARD_FILE):
        return []
    with open(LEADERBOARD_FILE, "r") as file:
        try:
            data = json.load(file)
            return data.get(MODE, [])
        except json.JSONDecodeError:
            return []

def save_leaderboard(leaderboard):
    data = {MODE: leaderboard[:MAX_ENTRIES]}
    with open(LEADERBOARD_FILE, "w") as file:
        json.dump(data, file, indent=4)

def update_leaderboard(name, score):
    leaderboard = load_leaderboard()
    leaderboard.append({"name": name, "score": score})
    leaderboard.sort(key=lambda x: x["score"], reverse=True)
    save_leaderboard(leaderboard)

def draw_leaderboard(screen, font):
    leaderboard = load_leaderboard()
    # screen.fill((0, 0, 0))
    title = font.render("Top 5 - Single Mode", True, (255, 255, 255))
    screen.blit(title, (50, 50))

    for i, entry in enumerate(leaderboard):
        text = font.render(f"{i + 1}. {entry['name']} - {entry['score']}", True, (255, 255, 255))
        screen.blit(text, (100, 120 + i * 50))

    pygame.display.update()

def record_score(name, score):
    update_leaderboard(name, score)
    #debug
    print(f"Đã ghi {score} điểm cho {name} vào bảng xếp hạng chế độ Single.")