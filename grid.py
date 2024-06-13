import pygame as pg
import random
from entity import Entity

class Grid:
    def __init__(self):
        # Initialize grid properties
        self.num_rows = 9
        self.num_col = 9
        self.cell_size = 40
        self.num_mines = 10

        self.entity = Entity()

        # Load font for displaying clues
        self.font_clue = self.entity.font1

        self.emoji_rect = pg.Rect(self.entity.emoji_img_rect.x - 5, self.entity.emoji_img_rect.y - 5, 
                                  self.entity.emoji_img_rect.width + 10, self.entity.emoji_img_rect.height + 10)

    # Randomly select mine positions
    def selectMinePositions(self):
        i = 0
        while i < self.num_mines:
            x = random.randint(0, self.num_col - 1)
            y = random.randint(0, self.num_rows - 1)
            if (x, y) not in self.mine_pos_list:
                self.grid_list[x][y] = 'x'
                i += 1
                self.mine_pos_list.append((x, y))


    # Draw the main Grid
    def drawGrid(self, win, left_button_clicked, right_button_clicked):
        # Get mouse position
        mouse_x, mouse_y = pg.mouse.get_pos()
        
        # Calculate grid cell indices for the mouse position
        row = (mouse_y - 105) // self.cell_size
        col = (mouse_x - 5) // self.cell_size

        # Checking for gameover (win condition)
        if (self.game_over == False and ((self.num_flags == 0 and self.allFlagPlacedCorrectly()) or self.allNonMinesFound())):
            self.game_over = True
            self.entity.win_sound.play()
            self.game_state = 2

        for i in range(self.num_rows):
            for j in range(self.num_col):
                
                # change the color of the revealed cell
                if (self.grid_list[i][j] == 'r'):
                    self.hidden_color = (30, 30, 46)

                # Mine correctly placed and gameover (either win or loose)
                elif (self.game_over == True and (i, j) in self.mine_pos_list and self.grid_list[i][j] ==  'f'):
                    self.hidden_color = (102, 0 , 0)

                # Check if the mouse is within the grid bounds
                elif (0 <= row < self.num_rows and 0 <= col < self.num_col and row == i and col == j):
                    # Highlight current cell
                    self.hidden_color = (77, 88, 100)

                    if self.game_over == False and (left_button_clicked or right_button_clicked):
                        self.inputHandler(j, i, left_button_clicked, right_button_clicked)

                else:
                    self.hidden_color = (56, 64, 72)

                rect = pg.Rect(5 + j * self.cell_size, 5 + 100 + i * self.cell_size, self.cell_size - 1, self.cell_size - 1)
                pg.draw.rect(win, self.hidden_color, rect)

                # Display all the bombs if gameover
                if (self.game_over and self.grid_list[i][j] == 'x'):
                    win.blit(self.entity.mine, rect)

                # Display clue if revealed
                if (self.grid_list[i][j] == 'r' and self.clue_list[i][j] > 0):
                    clue_text = self.font_clue.render(f"{self.clue_list[i][j]}", True, (0, 0, 255))
                    win.blit(clue_text, pg.Rect(rect.x + (rect.width - clue_text.get_size()[0]) / 2, rect.y + (rect.height - clue_text.get_size()[1]) / 2, rect.width, rect.height))

                # Display flag if cell is flagged
                if (self.grid_list[i][j] == 'f'):
                    win.blit(self.entity.flag, rect)

        # Drawing Display Window on Top (Hollow Rec, emoji rec)
        pg.draw.rect(win, (255, 255, 255), pg.Rect(5, 5, pg.display.get_window_size()[0] - 10, 100 - 5), 2, 3)
        pg.draw.rect(win, self.emoji_rect_color, self.emoji_rect, 0, 3)
        
    # Recursive algorithm to reveal cells
    def dig(self, i, j):
        self.dug.append((i, j))

        # Donot reveal flagged cell while digging
        if (self.grid_list[i][j] != 'f'):
            if self.grid_list[i][j] == "x":
                self.entity.lose_sound.play()
                self.game_state = 1
                self.game_over = True
                return None
            
            # It cannot be -1 for this i, j
            elif self.clue_list[i][j] != 0:
                self.grid_list[i][j] = 'r'
                return None
            
            self.grid_list[i][j] = 'r'
            
        else:
            return None

        for row in range(max(0, i-1), min(self.num_rows-1, i+1) + 1):
            for col in range(max(0, j-1), min(self.num_col-1, j+1) + 1):
                if (row, col) not in self.dug:
                    self.dig(row, col)
        return None

    # Check adjacent cells of the clicked cell
    def checkNeighbours(self, i, j):
        total_mines = 0

        for x_offset in [-1, 0, 1]:
            for y_offset in [-1, 0, 1]:
                new_i, new_j = i + y_offset, j + x_offset

                if ((0 <= new_i < self.num_rows and 0 <= new_j < self.num_col) and self.grid_list[new_i][new_j] == 'x'):
                    total_mines += 1
        
        return total_mines

    # Calculate and place clues for non-mine cells
    def placeClues(self):
        for i in range(self.num_rows):
            for j in range(self.num_col):

                if (self.grid_list[i][j] != 'x'):
                    total_mines = self.checkNeighbours(i, j)
                    if total_mines > 0:
                        self.clue_list[i][j] = total_mines
                else:
                    self.clue_list[i][j] = -1

    def allNonMinesFound(self):
        for i in range(self.num_rows):
            for j in range(self.num_col):
                if self.grid_list[i][j] != 'r' and self.clue_list[i][j] != -1:
                    return False
        return True

    def allFlagPlacedCorrectly(self):
        for i in self.mine_pos_list:
            if (self.grid_list[i[0]][i[1]] != 'f'):
                return False
        return True


    # Handle user input (left and right clicks)
    def inputHandler(self, index_x, index_y, left_button_clicked, right_button_clicked):

        if (left_button_clicked and self.grid_list[index_y][index_x] != 'f'):
            self.entity.click_sound.play()
            self.dig(index_y, index_x)

        if (right_button_clicked):
            self.entity.flag_sound.play()
            if (self.grid_list[index_y][index_x] != 'f'):
                self.num_flags -= 1
                self.grid_list[index_y][index_x] = 'f'

            elif (self.grid_list[index_y][index_x] == 'f'):
                self.num_flags += 1
                if ((index_y, index_x) in self.mine_pos_list):
                    self.grid_list[index_y][index_x] = 'x'
                else:
                    self.grid_list[index_y][index_x] = '-'

    def reset(self):
        self.num_flags = 10
        self.game_over = False
        self.dug = []

        # Initialize grid list
        # '-' = Hidden
        # 'x' = Mine
        # 'r' = Revealed and not mined
        # 'f' = flagged (mined or can be not mined)
        self.hidden_color = (56, 64, 72)
        self.emoji_rect_color = (56, 64, 72)
        self.grid_list = [['-' for i in range(self.num_col)] for j in range(self.num_rows)]

        # Set mine positions and clues
        self.mine_pos_list = []
        self.selectMinePositions()
        print (self.mine_pos_list)
        
        # -1 = "Bomb"
        # 0 = "No Clue(Empty and no nearby bomb)"
        # 1 - 8 = " With Clues"
        self.clue_list = [[0 for i in range(self.num_col)] for j in range(self.num_rows)]
        self.placeClues()

        # 0 - "running"
        # 1 - "loose"
        # 2 - "won"
        self.game_state = 0