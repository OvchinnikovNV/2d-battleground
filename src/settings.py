import pygame


class Settings:
    def __init__(self, window: pygame.Surface) -> None:
        self.window = window
        self.bg_color = pygame.Color(0, 0, 0)
        self.clock = pygame.time.Clock()
        self.active = False

        self.settings = {
            'num_npc': 1,
            'music_vol': 1.0,
            'sound_vol': 1.0
        }

        # Title
        padding = 200
        self.title = pygame.Rect(padding, 0, window.get_width() - 2 * padding, window.get_height() / 4)

        # Buttons
        self.btn_close = pygame.Rect(10, 10, 40, 40)

        # Settings
        self.s_font = pygame.font.Font(None, 50)
        self.border_width = 4
        self.s_rect_color = pygame.Color(200, 200, 200)
        self.s_pct_color = pygame.Color(125, 125, 125)

        size = (window.get_width() / 2, 100)
        x = window.get_width() / 2 - size[0] / 2

        y_arr = [y for y in range(int(self.title.height), window.get_height(), int(size[1] * 1.2))]

        self.num_npc = pygame.Rect((x, y_arr[0]), size)
        self.music_vol = pygame.Rect((x, y_arr[1]), size)
        self.sound_vol = pygame.Rect((x, y_arr[2]), size)


    def draw(self) -> None:
        self.clock.tick(30)

        self.window.fill(self.bg_color)

        # Back button
        self.draw_close_button()

        # Title
        msg_title = pygame.font.Font(None, 100).render('SETTINGS', True, (255, 255, 255))
        self.window.blit(msg_title, (self.title.centerx - msg_title.get_width() / 2, \
                                    self.title.centery - msg_title.get_height() / 2))

        # Setting rects
        self.draw_setting(self.num_npc, 'num_npc')
        self.draw_setting(self.music_vol, 'music_vol')
        self.draw_setting(self.sound_vol, 'sound_vol')

        pygame.display.update()


    def open(self) -> None:
        self.active = True
        while self.active:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.btn_close.collidepoint(event.pos):
                            self.active = False

                if event.type == pygame.MOUSEWHEEL:
                    if self.num_npc.collidepoint(pygame.mouse.get_pos()):
                        self.settings['num_npc'] += event.y
                        self.settings['num_npc'] %= 20

                    if self.music_vol.collidepoint(pygame.mouse.get_pos()):
                        self.settings['music_vol'] += event.y / 100
                        self.settings['music_vol'] %= 1.0

                    if self.sound_vol.collidepoint(pygame.mouse.get_pos()):
                        self.settings['sound_vol'] += event.y / 100
                        self.settings['sound_vol'] %= 1.0

            self.draw()


    def draw_setting(self, s_rect: pygame.Rect, name: str) -> None:
        # setting_rect
        pygame.draw.rect(self.window, self.s_rect_color, s_rect, self.border_width)

        # setting name
        tmp = self.s_font.render(name, True, (255, 255, 255))
        self.window.blit(tmp, (s_rect.centerx - tmp.get_width() / 2, s_rect.top + tmp.get_height() / 2))

        if name == 'num_npc':
            tmp = self.s_font.render(str(self.settings[name]), True, (255, 255, 255))
            self.window.blit(tmp, (s_rect.centerx - tmp.get_width() / 2, \
                                   s_rect.top + s_rect.height / 2 + tmp.get_height() / 3))
            return

        # percent rect
        padding = 10
        percent = self.settings[name] - 1.0
        tmp = pygame.Rect(s_rect.left + padding, s_rect.top + s_rect.height / 2 + padding, \
                          s_rect.width - padding * 2, s_rect.height / 2 - padding * 2)
        pygame.draw.rect(self.window, self.s_pct_color, tmp.inflate(tmp.width * percent, 0)
                   .move(tmp.width / 2 * percent, 0))
        pygame.draw.rect(self.window, self.s_pct_color, tmp, self.border_width)


    def draw_close_button(self) -> None:
        pygame.draw.rect(self.window, (255, 255, 255), self.btn_close)


    def export(self) -> dict:
        return self.settings
