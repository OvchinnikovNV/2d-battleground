import pygame
import math


class Bullet:
    def __init__(self, window: pygame.Surface, x, y, dir) -> None:
        self.radius = 4
        self.speed = 6
        self.color = (255, 255, 100)

        self.window = window
        self.size = (self.radius*2, self.radius*2)
        self.x = x - self.radius
        self.y = y - self.radius
        self.direction = dir
        
        

    def draw(self) -> None:
        pygame.draw.ellipse(self.window, self.color, pygame.Rect((self.x, self.y), self.size))
        self.x += self.speed * math.sin(self.direction)
        self.y += self.speed * math.cos(self.direction)


    def in_window(self) -> bool:
        if 0 < self.x < self.window.get_width() and 0 < self.y < self.window.get_height():
            return True
        return False

    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(self.x, self.y, self.size[0], self.size[1])
