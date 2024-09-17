import  pygame as pg

class Entity:
    def __init__(self):
        # Load emoji images for different game states
        self.emoji = [
            pg.image.load("assets/smile.png"), 
            pg.image.load("assets/dead.png"), 
            pg.image.load("assets/sunglasses.png")
        ]

        # Define the rectangle for the emoji image
        self.emoji_img_rect = pg.Rect(
            int(pg.display.get_window_size()[0] / 2) - 30, 
            22.5,  # 20 + 2.5
            60, 
            60
        )
        
        # Load flag and mine images
        self.flag_img = pg.image.load("assets/flag.png")
        self.mine_img = pg.image.load("assets/bomb.png")

        self.font = pg.font.Font("assets/font.otf", 60)
        self.clue_font = pg.font.Font("assets/font1.ttf", 32)

        # Load sound effects
        self.click_sound = pg.mixer.Sound("assets/sounds/click.wav")
        self.start_sound = pg.mixer.Sound("assets/sounds/start.wav")
        self.lose_sound = pg.mixer.Sound("assets/sounds/lose.wav")
        self.win_sound = pg.mixer.Sound("assets/sounds/win.wav")
        self.flag_sound = pg.mixer.Sound("assets/sounds/flag.wav")