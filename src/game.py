import sys
import pygame
from first_map import FirstMap
from player import Player
from npc import NPC
from menu import Menu


class Game:
    def __init__(self) -> None:
        self.FPS = 60
        self.NUM_NPC = 2
        self.bg_color = pygame.Color(20, 20, 20)
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('My PUBG')

        pygame.init()
        pygame.font.init()
        self.window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        #self.window = pygame.display.set_mode((800, 600))

        self.menu = Menu(self.window)
        
        # game object init
        self.fmap = FirstMap(self.window)
        self.characters = []

        # Player
        self.player = Player(self.window, self.fmap)
        self.characters.append(self.player)

        # NPC
        for _ in range(self.NUM_NPC):
            self.characters.append(NPC(self.window, self.fmap))

        for character in self.characters:
            character.init_enemies(self.characters)


    def draw(self) -> None:
        self.clock.tick(self.FPS)

        self.window.fill(self.bg_color)

        for character in self.characters:
            character.draw()

        for type, block in self.fmap.map:
            if type == 'W':
                wall = pygame.image.load('../rsc/snow_wall.png')
                wall = pygame.transform.scale(wall, (block[2], block[3]))
                self.window.blit(wall, (block[0], block[1]))

        pygame.display.update()


    def start(self) -> None:
        while True:
            if self.menu.active:
                self.menu.open()

            for character in self.characters:
                if character.dead:
                    self.characters.pop(self.characters.index(character))
                    if self.player is not None and character.id == self.player.id:
                        self.player = None
                    del character

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                self.menu.active = not self.menu.active

            if self.player is not None:
                if keys[pygame.K_LEFT]:
                    self.player.lturn()

                if keys[pygame.K_RIGHT]:
                    self.player.rturn()

                if keys[pygame.K_UP]:
                    self.player.forward()

                if keys[pygame.K_DOWN]:
                    self.player.backward()

                if keys[pygame.K_SPACE]:
                    self.player.shot()

            self.draw()
