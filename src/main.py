import pygame
from menu import Menu


if __name__ == '__main__':
    pygame.init()
    pygame.font.init()
    pygame.display.set_caption('My PUBG')
    Menu().open()
