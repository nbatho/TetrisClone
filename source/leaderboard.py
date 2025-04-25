import pygame
import json
import os

LEADERBOARD_FILE = "leaderboard.json"
MAX_ENTRIES = 5

def load_leaderboard(mode):
    if not os.path.exists(LEADERBOARD_FILE):
        return []
    with open(LEADERBOARD_FILE, "r") as file:
        data = json.load(file)
    return data.get(mode, [])

def save_leaderboard(mode, leaderboard):
    if os.path.exists(LEADERBOARD_FILE):
        with open(LEADERBOARD_FILE, "r") as file:
            data = json.load(file)
    else:
        data = {}
    data[mode] = leaderboard[:MAX_ENTRIES]
    with open(LEADERBOARD_FILE, "w") as file:
        json.dump(data, file, indent=4)

def update_leaderboard(mode, name, score):
    leaderboard = load_leaderboard(mode)
    leaderboard.append({"name": name, "score": score})
    leaderboard.sort(key=lambda x: x["score"], reverse=True)
    save_leaderboard(mode, leaderboard)

def draw_leaderboard(screen, font, mode):
    leaderboard = load_leaderboard(mode)
    screen.fill((0, 0, 0))
    title = font.render(f"Leaderboard - {mode}", True, (255, 255, 255))
    screen.blit(title, (50, 50))

    for i, entry in enumerate(leaderboard):
        text = font.render(f"{i + 1}. {entry['name']} - {entry['score']}", True, (255, 255, 255))
        screen.blit(text, (100, 120 + i * 50))
    
    pygame.display.flip()

def record_score(mode, name, score):
    """
    Hàm ghi lại điểm số vào bảng xếp hạng cho một chế độ cụ thể
    """
    update_leaderboard(mode, name, score)  # Cập nhật bảng xếp hạng sau mỗi lần chơi
    print(f"Đã ghi lại điểm số {score} của {name} vào bảng xếp hạng {mode}")

# Ví dụ sử dụng
pygame.init()
screen = pygame.display.set_mode((600, 600))
font = pygame.font.SysFont("Arial", 24)

# Ghi điểm số vào bảng xếp hạng chế độ "solo"
record_score("solo", "Player1", 1500)

# Vẽ bảng xếp hạng sau khi ghi điểm số
draw_leaderboard(screen, font, "solo")

pygame.quit()
