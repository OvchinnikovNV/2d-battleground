import sys
import pygame


class Menu:
    def __init__(self, window: pygame.Surface) -> None:
        self.window = window
        self.clock = pygame.time.Clock()
        self.FPS = 30
        self.active = True

        # Font
        self.font_size = 50
        self.font_color = (255, 255, 255)

        # Title
        self.title_font_size = int(0.1 * self.window.get_width())
        self.title_font_color = (255, 0, 0)
        self.title = pygame.Rect(0, 0, self.window.get_width(), self.window.get_height() / 2)

        # Buttons
        self.btns_width = int(self.window.get_width() / 4)
        self.btns_height = int(self.window.get_height() / 10)
        self.btns_x = int(self.window.get_width() / 2) - self.btns_width / 2

        y_array = [y for y in range(
                        int(self.window.get_height() / 2 + 50), 
                        self.window.get_height() - self.btns_height, 
                        int(self.btns_height * 1.1)
                    )]

        self.btn_play = pygame.Rect(self.btns_x, y_array[0], self.btns_width, self.btns_height)
        self.btn_settings = pygame.Rect(self.btns_x, y_array[1], self.btns_width, self.btns_height)
        self.btn_exit = pygame.Rect(self.btns_x, y_array[2], self.btns_width, self.btns_height)


    def open(self) -> None:
        while self.active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.btn_play.collidepoint(event.pos):
                            self.active = False
                        
                        if self.btn_exit.collidepoint(event.pos):
                            sys.exit()

            self.draw()


    def draw(self) -> None:
        self.clock.tick(self.FPS)

        self.window.fill((0,0,0))

        # Title
        msg_title = pygame.font.Font(None, self.title_font_size).render('BATTLEGROUND', True, self.title_font_color)
        self.window.blit(msg_title, (self.title.centerx - msg_title.get_width() / 2, \
                                    self.title.centery - msg_title.get_height() / 2))

        # Buttons
        pygame.draw.rect(self.window, (0, 0, 200), self.btn_play, 4)
        pygame.draw.rect(self.window, (0, 0, 200), self.btn_settings, 4)
        pygame.draw.rect(self.window, (0, 0, 200), self.btn_exit, 4)

        msg_play = pygame.font.Font(None, self.font_size).render('Play', True, self.font_color)
        self.window.blit(msg_play, (self.btn_play.centerx - msg_play.get_width() / 2, \
                                    self.btn_play.centery - msg_play.get_height() / 2))

        msg_settings = pygame.font.Font(None, self.font_size).render('Settings', True, self.font_color)
        self.window.blit(msg_settings, (self.btn_settings.centerx - msg_settings.get_width() / 2, \
                                    self.btn_settings.centery - msg_settings.get_height() / 2))

        msg_exit = pygame.font.Font(None, self.font_size).render('Exit', True, self.font_color)
        self.window.blit(msg_exit, (self.btn_exit.centerx - msg_exit.get_width() / 2, \
                                    self.btn_exit.centery - msg_exit.get_height() / 2))

        pygame.display.update()
