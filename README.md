# 🎮 TetrisClone

A full-featured Tetris game implementation built with Python and Pygame, featuring single-player, AI battle, and online multiplayer modes.

## ✨ Features

- **Single Player Mode**: Classic Tetris gameplay with progressive difficulty
- **VS Bot Mode**: Challenge an AI opponent in head-to-head battles
- **VS Player Mode**: Online multiplayer support via network play
- **Leaderboard System**: Track and save high scores
- **Sound Effects & Music**: Immersive audio experience with background music and sound effects
- **Modern UI**: Clean menu system with custom graphics
- **Level Progression**: Increasing difficulty as you clear more lines
- **Preview System**: See upcoming Tetromino pieces

## 📋 Requirements

- Python 3.7 or higher
- Pygame 2.5.0 or higher

## 🚀 Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/TetrisClone.git
cd TetrisClone
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

Or install Pygame directly:
```bash
pip install pygame>=2.5.0
```

## 🎯 How to Run

### Single Player / VS Bot Mode

Simply run the main game file:
```bash
cd source
python main.py
```

Or from the project root:
```bash
python source/main.py
```

### Multiplayer Mode (VS Player)

For multiplayer, you need to run a server first:

**On the host machine:**
```bash
cd source
python server.py
```

**On each player's machine:**
```bash
cd source
python main.py
```

Then select "VS Player" from the menu and enter the host's IP address when prompted.

## 🎮 Game Controls

| Key | Action |
|-----|--------|
| ← (Left Arrow) | Move piece left |
| → (Right Arrow) | Move piece right |
| ↓ (Down Arrow) | Soft drop (move piece down faster) |
| ↑ (Up Arrow) | Rotate piece |
| SPACE | Hard drop (instantly drop piece) |
| ESC | Pause / Return to menu |

## 📁 Project Structure

```
TetrisClone/
├── source/              # Source code directory
│   ├── main.py         # Main game entry point
│   ├── game.py         # Core game logic
│   ├── menu.py         # Menu system
│   ├── score.py        # Score tracking
│   ├── preview.py      # Tetromino preview
│   ├── leaderboard.py  # Leaderboard management
│   ├── network.py      # Network/multiplayer support
│   ├── server.py       # Multiplayer server
│   ├── sound.py        # Sound manager
│   ├── setting.py      # Game settings and configurations
│   ├── timer.py        # Game timer
│   └── button.py       # UI button component
├── graphics/           # Graphics and image assets
│   ├── Background.jpg
│   ├── font.ttf
│   └── [Tetromino images]
├── sounds/             # Sound effects and music
│   ├── theme.mp3
│   ├── line_clear.mp3
│   └── landing.wav
├── leaderboard.json    # Saved high scores
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## 🎲 Game Modes

### 🟢 Single Player
Classic Tetris experience where you clear lines and try to achieve the highest score. The game speed increases as you level up.

### 🤖 VS Bot
Battle against an AI opponent. Both you and the bot play simultaneously on split screens. Highest score wins!

### 🌐 VS Player
Play against other players over the network. Requires a server to be running and players to connect to the same host.

## 📊 Scoring System

- **1 Line Clear**: 40 points × level
- **2 Lines Clear**: 100 points × level
- **3 Lines Clear**: 300 points × level
- **4 Lines Clear (Tetris)**: 1200 points × level

## 🛠️ Configuration

You can modify game settings in [source/setting.py](source/setting.py):
- Grid dimensions (COLUMNS, ROWS)
- Cell size and window dimensions
- Game speed and controls
- Colors for each Tetromino
- Volume levels (MASTER_VOLUME, EFFECT_VOLUME)

## 🐛 Troubleshooting

**Issue: "pip install pygame" fails**
- Try: `python -m pip install --upgrade pip`
- Then: `pip install pygame`

**Issue: No sound is playing**
- Check that your audio device is working
- Adjust volume in [source/setting.py](source/setting.py)

**Issue: Cannot connect in multiplayer mode**
- Ensure the server is running on the host machine
- Check firewall settings
- Verify the correct IP address is entered
- Both players must be on the same network or have port forwarding configured

## 📝 License

This project is open source and available for educational purposes.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

---

**Enjoy playing Tetris! 🎉**
 
