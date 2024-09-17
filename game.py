import pygame as pg
import sys 

from grid import Grid


class Game:
    def __init__(self):
        pg.init()
        pg.display.set_caption('Minesweeper')
        
        # Set the window icon
        icon = pg.image.load("assets/icon/icon.png")
        pg.display.set_icon(icon)

        # Define window dimensions
        window_width = 360 + 10
        window_height = 360 + 110
        self.window = pg.display.set_mode((window_width, window_height))

        # Initialize game variables
        self.elapsed_time = 0
        self.clock = pg.time.Clock() # Creates a Clock object to help manage time and control the frame rate
        self.start_tick = pg.time.get_ticks() # Returns the number of milliseconds since Pygame was initialized.
        
        # Initialize the game grid
        self.grid = Grid()

        # Set the font
        self.font = self.grid.entity.font
        
        self.resetGame()
        self.gameLoop()

    def gameLoop(self):
        while True:
            if (self.grid.game_over == False):
                # Calculate elapsed time in seconds
                self.elapsed_time = (pg.time.get_ticks() - self.start_tick) // 1000
            
            self.left_button_clicked = False
            self.right_button_clicked = False

            self.mouse_x, self.mouse_y = pg.mouse.get_pos()

            for event in pg.event.get():
                if (event.type == pg.QUIT):
                    pg.quit()
                    sys.exit()

                if event.type == pg.MOUSEMOTION:
                    if self.grid.emoji_rect.collidepoint(self.mouse_x, self.mouse_y):
                        # Change color when hovering
                        self.grid.emoji_rect_color = (77, 88, 100)
                        
                    else:
                        self.grid.emoji_rect_color = (56, 64, 72)
                
                if event.type == pg.MOUSEBUTTONDOWN and (not self.button_pressed):
                    # Left mouse button
                    if (event.button == 1):
                        if self.grid.emoji_rect.collidepoint(self.mouse_x, self.mouse_y):
                            self.resetGame()
                        else:
                            self.left_button_clicked = True
                    
                    # Right mouse button
                    elif (event.button == 3):
                        self.right_button_clicked = True                        

                    # Mark the click as handled
                    self.button_pressed = True

                # Handling MOUSEBUTTONUP
                if event.type == pg.MOUSEBUTTONUP:
                    # Reset the flag
                    self.button_pressed = False

            # Fill the window with a background color
            self.window.fill((30, 38, 46))

            # Draw the game grid
            self.grid.drawGrid(self.window, self.left_button_clicked, self.right_button_clicked, self.mouse_x, self.mouse_y)
            
            # Draw the emoji based on the game state
            if (self.grid.game_state == "lose"):
                emoji_idx = 1
            elif (self.grid.game_state == "won"):
                emoji_idx = 2
            else:
                emoji_idx = 0
            self.window.blit(self.grid.entity.emoji[emoji_idx], self.grid.entity.emoji_img_rect)

            # Update the timer position every 10 seconds
            if self.elapsed_time % 10 == 0:
                self.time_text_rect = self.time_text.get_rect(center = (295, 53))
            
            # Render the timer
            self.time_text = self.font.render(f"{self.elapsed_time}", True, (255, 0, 0))
            self.window.blit(self.time_text, self.time_text_rect)

            # Render the number of flags
            self.text_flags = self.font.render (f"{self.grid.num_flags}", True, (255, 0, 0))
            self.window.blit(self.text_flags, self.text_flags_rect)
            
            # Update the display
            pg.display.flip()
            self.clock.tick(60)

    def resetGame(self):
        # Play the start sound and reset the grid
        self.grid.entity.start_sound.play()
        self.grid.reset()

        # Reset the start time
        self.start_tick = pg.time.get_ticks()
        
        # Initialize the timer and flags display
        self.time_text = self.font.render(f"{self.elapsed_time}", True, (255, 0, 0))
        self.time_text_rect = self.time_text.get_rect(center = (295, 53))

        self.text_flags = self.font.render (f"{self.grid.num_flags}", True, (255, 0, 0))
        self.text_flags_rect = self.text_flags.get_rect(center = (80, 53))

        # Reset mouse button states
        self.button_pressed = False

Game()