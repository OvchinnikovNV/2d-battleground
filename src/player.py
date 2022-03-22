import pygame
import sys
import math
import random
import time
from first_map import FirstMap
from bullet import Bullet


class Player:
    def __init__(self, window: pygame.Surface, fmap: FirstMap, settings: dict) -> None:
        self.id = id(self)
        self.window = window
        self.fmap = fmap
        self.type = 'player'
        
        self.radius = 15
        self.color = (0, 0, 255)
        self.x = random.randint(0, self.window.get_width() - self.radius * 2)
        self.y = random.randint(0, self.window.get_height() - self.radius * 2)
        self.rect = pygame.Rect(self.x, self.y, self.radius * 2, self.radius * 2)

        while not fmap.check_wall(self.rect):
            self.reposition()

        self.direction = 2 * math.pi / random.randint(2, 10) # направление прицела
        self.vision = 150 # радиус обзора (прицелы увеичивают)
        self.speed = 3
        self.shot_cd = 0.5
        self.last_shoot_time = time.time()
        
        self.health = 100
        self.health_width = 4
        self.dead = False

        self.vision_rect = pygame.Rect(self.rect.centerx - self.vision, self.rect.centery - self.vision,
                                       self.vision * 2, self.vision * 2)
        self.bullets = []
        self.enemies = []

        # Sounds
        self.sound_shot = pygame.mixer.Sound('../audio/prostoy-vyistrel.wav')
        self.sound_shot.set_volume(settings['sound_vol'])


    def __del__(self):
        #print('Dead', self.id)
        pass


    def draw(self) -> None:
        if self.health < 1:
            if not self.dead:
                self.kill()
            return

        self.update_vision_rect()
        self.rect.update((self.x, self.y), self.rect.size)

        if self.type == 'player':
            self.set_mouse_direction()

        pygame.draw.rect(self.window, self.color, self.vision_rect, 1)
        pygame.draw.aaline(
            self.window,
            (0, 255, 0),
            self.rect.center, 
            (
                self.rect.centerx + self.vision * math.sin(self.direction),
                self.rect.centery + self.vision * math.cos(self.direction)
            )
        )
        pygame.draw.ellipse(self.window, self.color, self.rect)
        pygame.draw.arc(
            self.window,
            (255 - self.health * 2.5, self.health * 2.5, 0),
            self.rect.inflate(2 * self.health_width, 2 * self.health_width),
            0,
            2 * math.pi * self.health / 100,
            self.health_width
        )

        for enemy in self.enemies:
            if enemy.dead:
                self.enemies.pop(self.enemies.index(enemy))
                del enemy

        for bullet in self.bullets:
            for enemy in self.enemies:
                if bullet.get_rect().colliderect(enemy.rect):
                    enemy.health -= 10
                    try:
                        self.bullets.pop(self.bullets.index(bullet))
                    except ValueError:
                        pass

            if bullet.in_window() and self.fmap.check_wall(bullet.get_rect()):
                bullet.draw()
            else:
                try:
                    self.bullets.pop(self.bullets.index(bullet))
                except ValueError:
                    pass


    def up(self) -> None:
        if self.fmap.check_wall(self.rect.move(0, -self.speed)):
            self.y -= self.speed


    def down(self) -> None:
        if self.fmap.check_wall(self.rect.move(0, self.speed)):
            self.y += self.speed


    def left(self) -> None:
        if self.fmap.check_wall(self.rect.move(-self.speed, 0)):
            self.x -= self.speed


    def right(self) -> None:
        if self.fmap.check_wall(self.rect.move(self.speed, 0)):
            self.x += self.speed


    def shot(self) -> Bullet:
        if time.time() - self.last_shoot_time > self.shot_cd:
            self.last_shoot_time = time.time()
            self.bullets.append(Bullet(self.window, self.x + self.radius, self.y + self.radius, self.direction))
            self.sound_shot.play()


    def reposition(self) -> None:
        self.x = random.randint(0, self.window.get_width() - self.radius * 2)
        self.y = random.randint(0, self.window.get_height() - self.radius * 2)
        self.rect.move_ip(self.x, self.y)

    
    def update_vision_rect(self) -> None:
        self.vision_rect.update((self.rect.centerx - self.vision, self.rect.centery - self.vision), self.vision_rect.size)


    def init_enemies(self, characters: list) -> None:
        for character in characters:
            if character.id != self.id:
                self.enemies.append(character)


    def kill(self) -> None:
        self.dead = True
        self.bullets.clear()
        self.enemies.clear()


    def set_settings(self, settings: dict) -> None:
        self.sound_shot.set_volume(settings['sound_vol'])


    def set_mouse_direction(self) -> None:
        default_v = pygame.Vector2(
            self.rect.centerx,
            self.rect.centery + sys.maxsize
        )

        direction_v = pygame.Vector2(
            pygame.mouse.get_pos()[0] - self.rect.centerx,
            pygame.mouse.get_pos()[1] - self.rect.centery
        )

        self.direction = -1 * default_v.angle_to(direction_v) * math.pi / 180
