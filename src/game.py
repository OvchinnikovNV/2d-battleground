import sys
import pygame
from first_map import FirstMap
from player import Player
from npc import NPC


class Game:
    def __init__(self, window: pygame.Surface, settings: dict) -> None:
        self.window = window
        self.FPS = 60
        self.NUM_NPC = settings['num_npc']
        self.bg_color = pygame.Color(20, 20, 20)
        self.clock = pygame.time.Clock()
        self.active = False
        
        # game object init
        self.fmap = FirstMap(self.window)
        self.characters = []

        # Player
        self.player = Player(self.window, self.fmap, settings)
        self.characters.append(self.player)

        # NPC
        for _ in range(self.NUM_NPC):
            self.characters.append(NPC(self.window, self.fmap, settings))

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
        self.active = True
        while self.active:
            for character in self.characters:
                if character.dead:
                    self.characters.pop(self.characters.index(character))
                    if self.player is not None and character.id == self.player.id:
                        self.player = None
                    del character

            for event in pygame.event.get():
                if pygame.mouse.get_pressed()[0]:
                    self.player.shot()

                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.player.shot()
                elif event.type == pygame.MOUSEMOTION:
                    self.player.set_mouse_direction()


            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                self.active = False

            if self.player is not None:
                if keys[pygame.K_a]:
                    self.player.left()

                if keys[pygame.K_d]:
                    self.player.right()

                if keys[pygame.K_w]:
                    self.player.up()

                if keys[pygame.K_s]:
                    self.player.down()

                if keys[pygame.K_SPACE]:
                    self.player.shot()

            self.draw()


    def set_settings(self, settings: dict) -> None:
        for character in self.characters:
            character.set_settings(settings)
