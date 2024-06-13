# MineSweeper-Pygame
This repository contains a simple Minesweeper game implemented using Pygame. The game features a grid of cells, some of which contain hidden mines. The goal is to reveal all non-mine cells without triggering any mines.

## Features:
- Classic Minesweeper gameplay
- Left-click to reveal cells
- Right-click to flag potential mines
- Emoji-click to restart the game
- Emoji Indicators:
  - 😊 Smiling emoji: Game in progress
  - ☹️ Sad emoji: You lose (triggered a mine)
  - 😎 Sunglasses emoji: You win (all non-mine cells revealed)
  - Clicking on any emoji restarts the game
- Sound Effects:
  - Click sound when revealing cells or flagging mines
  - Restart sound when clicking on an emoji
  - Victory sound when winning
  - Defeat sound when triggering a mine

## Installation:
1. Make sure you have Python and Pygame installed.
2. Clone this repository to your local machine.
3. Run the following command to start the game:
   ```
   python main.py
   ```

## Controls:
- **Left-click**: Reveal a cell
- **Right-click**: Flag a cell as a potential mine

Feel free to contribute or use this code as a starting point for your own Minesweeper project!