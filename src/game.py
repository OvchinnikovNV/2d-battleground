import sys
import pygame
from first_map import FirstMap
from player import Player
from npc import NPC


class Game:
    def __init__(self, window: pygame.Surface) -> None:
        self.window = window
        self.FPS = 60
        self.NUM_NPC = 100
        self.bg_color = pygame.Color(20, 20, 20)
        self.clock = pygame.time.Clock()
        self.active = True
        
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
        while self.active:
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
                self.active = False

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
