from sys import winver
import pygame


class FirstMap:
    def __init__(self, window: pygame.Surface) -> None:
        self.window = window
        self.block_width = 0
        self.block_height = 0
        self.text_map = [
            'WWWWWWWWWWWWWWWWW',
            'W...............W',
            'W...............W',
            'W...............W',
            'W...............W',
            'W...............W',
            'W...............W',
            'W...............W',
            'W...............W',
            'W...............W',
            'W...............W',
            'W...............W',
            'W...............W',
            'WWWWWWWWWWWWWWWWW',
        ]

        self.player_pos = None
        self.map = set()
        self.init_map()


    def init_map(self) -> None:
        self.block_width = int(self.window.get_width() / len(self.text_map[0]))
        self.block_height = int(self.window.get_height() / len(self.text_map))

        for j, row in enumerate(self.text_map):
            for i, char in enumerate(row):
                if char == 'W':
                    self.map.add(('W', (i * self.block_width, j * self.block_height, self.block_width, self.block_height)))


    def check_wall(self, player_rect: pygame.Rect) -> bool:
        for type, block in self.map:
            tmp = pygame.Rect(block[0], block[1], block[2], block[3])
            if type == 'W' and player_rect.colliderect(tmp):
                return False
                
        return True
