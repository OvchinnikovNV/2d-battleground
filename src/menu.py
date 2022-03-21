import sys
import pygame
from game import Game
from settings import Settings


class Menu:
    def __init__(self) -> None:
        #self.window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.window = pygame.display.set_mode((800, 600))
        self.bg_color = pygame.Color(0, 0, 0)
        self.clock = pygame.time.Clock()
        self.active = True
        self.current_game = None

        # Settings
        self.settings = Settings(self.window)

        # Music
        pygame.mixer.music.load('../audio/tunetank.com_5394_rock-spot_by_nuclear-wave.mp3')

        # Font
        self.font_size = 50
        self.font_color = (255, 255, 255)

        # Title
        self.title_font_size = int(0.1 * self.window.get_width())
        self.title_font_color = (255, 0, 0)
        self.title = pygame.Rect(0, 0, self.window.get_width(), self.window.get_height() / 2)

        # Buttons
        self.btns_width = int(self.window.get_width() / 4)
        self.btns_height = int(self.window.get_height() / 12)
        self.btns_x = int(self.window.get_width() / 2) - self.btns_width / 2

        y_array = [y for y in range(
                        int(self.window.get_height() / 2 + 50), 
                        self.window.get_height() - self.btns_height, 
                        int(self.btns_height * 1.1)
                    )]

        self.btn_play = pygame.Rect(self.btns_x, y_array[0], self.btns_width, self.btns_height)
        self.btn_new_game = pygame.Rect(self.btns_x, y_array[1], self.btns_width, self.btns_height)
        self.btn_settings = pygame.Rect(self.btns_x, y_array[2], self.btns_width, self.btns_height)
        self.btn_exit = pygame.Rect(self.btns_x, y_array[3], self.btns_width, self.btns_height)


    def open(self) -> None:
        self.set_settings()
        pygame.mixer.music.play(100)

        while True:
            pygame.mixer.music.unpause()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.btn_play.collidepoint(event.pos):
                            pygame.mixer.music.pause()
                            if self.current_game is None:
                                self.current_game = Game(self.window, self.settings.export())
                                self.current_game.start()
                            else:
                                self.current_game.start()
                        
                        if self.btn_new_game.collidepoint(event.pos):
                            pygame.mixer.music.pause()
                            self.current_game = Game(self.window, self.settings.export())
                            self.current_game.start()

                        if self.btn_settings.collidepoint(event.pos):
                            self.settings.open()
                            self.set_settings()

                        if self.btn_exit.collidepoint(event.pos):
                            sys.exit()

            self.draw()


    def draw(self) -> None:
        self.clock.tick(30)

        self.window.fill(self.bg_color)

        # Title
        msg_title = pygame.font.Font(None, self.title_font_size).render('BATTLEGROUND', True, self.title_font_color)
        self.window.blit(msg_title, (self.title.centerx - msg_title.get_width() / 2, \
                                    self.title.centery - msg_title.get_height() / 2))

        # Buttons
        self.draw_btn(self.btn_play, 'Play')
        self.draw_btn(self.btn_new_game, 'New Game')
        self.draw_btn(self.btn_settings, 'Settings')
        self.draw_btn(self.btn_exit, 'Exit')

        pygame.display.update()


    def draw_btn(self, btn_rect: pygame.Rect, btn_name: str) -> None:
        pygame.draw.rect(self.window, (0, 0, 200), btn_rect, 4)
        text = pygame.font.Font(None, self.font_size).render(btn_name, True, self.font_color)
        self.window.blit(text, (btn_rect.centerx - text.get_width() / 2, \
                                btn_rect.centery - text.get_height() / 2))


    def set_settings(self) -> None:
        tmp = self.settings.export()
        pygame.mixer.music.set_volume(tmp['music_vol'])
