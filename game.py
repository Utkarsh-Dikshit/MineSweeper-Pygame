import pygame as pg
import sys 

from grid import Grid


class Game:
    def __init__(self):
        pg.init()
        pg.display.set_caption('Minesweeper')
        
        self.width = 360 + 10
        self.height = 360 + 110
        self.win = pg.display.set_mode((self.width, self.height))

        self.elapsed_time = 0
        self.clock = pg.time.Clock()
        self.start_tick = pg.time.get_ticks()
        
        self.grid = Grid()

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

            for event in pg.event.get():
                if (event.type == pg.QUIT):
                    pg.quit()
                    sys.exit()

                if event.type == pg.MOUSEBUTTONDOWN and (not self.button_pressed):
                    if (event.button == 1):
                        if self.grid.emoji_rect.collidepoint(mouse_x, mouse_y):
                            self.resetGame()
                        else:
                            self.left_button_clicked = True
                    
                    elif (event.button == 3):
                        self.right_button_clicked = True                        

                    # Mark the click as handled
                    self.button_pressed = True  

                # Handle MOUSEBUTTONUP
                if event.type == pg.MOUSEBUTTONUP:
                    # Reset the flag
                    self.button_pressed = False  

                if event.type == pg.MOUSEMOTION:
                    mouse_x, mouse_y = pg.mouse.get_pos()
                    if self.grid.emoji_rect.collidepoint(mouse_x, mouse_y):
                        self.grid.emoji_rect_color = (77, 88, 100)  # Change color when hovering
                        # want to run rest function here
                    else:
                        self.grid.emoji_rect_color = (56, 64, 72)


            self.win.fill((30, 38, 46))

            self.grid.drawGrid(self.win, self.left_button_clicked, self.right_button_clicked)
            
            self.win.blit(self.grid.entity.emoji[self.grid.game_state], self.grid.entity.emoji_img_rect)

            if self.elapsed_time % 10 == 0:
                self.time_text_rect = self.time_text.get_rect(center = (295, 53))
            
            self.time_text = self.font.render(f"{self.elapsed_time}", True, (255, 0, 0))
            self.win.blit(self.time_text, self.time_text_rect)
            
            self.text_flags = self.font.render (f"{self.grid.num_flags}", True, (255, 0, 0))
            self.win.blit(self.text_flags, self.text_flags_rect)

            pg.display.flip()
            self.clock.tick(60)

    def resetGame(self):
        self.grid.entity.start_sound.play()
        self.grid.reset()

        self.start_tick = pg.time.get_ticks()
        
        self.time_text = self.font.render(f"{self.elapsed_time}", True, (255, 0, 0))
        self.time_text_rect = self.time_text.get_rect(center = (295, 53))

        self.text_flags = self.font.render (f"{self.grid.num_flags}", True, (255, 0, 0))
        self.text_flags_rect = self.text_flags.get_rect(center = (80, 53))

        self.button_pressed = False
        self.left_button_clicked = False
        self.right_button_clicked = False

Game()