import pygame
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
        
        self.radius = 16
        self.size = (self.radius*2, self.radius*2)
        self.color = (0, 0, 255)
        self.x = random.randint(0, self.window.get_width() - self.radius * 2)
        self.y = random.randint(0, self.window.get_height() - self.radius * 2)

        while not fmap.check_wall(self.get_rect()):
            self.reposition()

        self.view_range = 150  # длина линии прицела
        self.direction = 2 * math.pi / random.randint(2, 10) # направление прицела
        self.vision = 150 # радиус обзора (прицелы увеичивают)
        self.turning_speed = 0.05
        self.speed = 3
        self.shot_cd = 0.5
        self.last_shoot_time = time.time()
        
        self.health = 100
        self.health_width = 4
        self.dead = False

        self.vision_rect = None
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

        pygame.draw.rect(self.window, self.color, self.vision_rect, 1)
        pygame.draw.aaline(self.window, (0, 255, 0), (self.x + self.radius, self.y + self.radius), 
                           (self.x + self.radius + self.view_range * math.sin(self.direction),
                            self.y + self.radius + self.view_range * math.cos(self.direction))
                          )
        pygame.draw.ellipse(self.window, self.color, self.get_rect())
        pygame.draw.arc(self.window, (255 - self.health * 2.5, self.health * 2.5, 0), \
                        (self.x - self.health_width, self.y - self.health_width, \
                         self.size[0] + 2 * self.health_width, self.size[1] + 2 * self.health_width), \
                        0, 2 * math.pi * self.health / 100, self.health_width)

        # health_msg = pygame.font.Font(None, 24).render(str(self.health), True, (255, 255, 255))
        # self.window.blit(health_msg, (self.x, self.y))

        for enemy in self.enemies:
            if enemy.dead:
                self.enemies.pop(self.enemies.index(enemy))
                del enemy

        for bullet in self.bullets:
            for enemy in self.enemies:
                if bullet.get_rect().colliderect(enemy.get_rect()):
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


    def check_forward(self) -> tuple[float, float]:
        dx = self.speed * math.sin(self.direction)
        dy = self.speed * math.cos(self.direction)

        return (
            dx if self.fmap.check_wall(self.get_rect().move(dx, 0)) else 0,
            dy if self.fmap.check_wall(self.get_rect().move(0, dy)) else 0
        )


    def check_backward(self) -> pygame.Rect:
        return pygame.Rect( self.x - self.speed * math.sin(self.direction), self.y - self.speed * math.cos(self.direction), self.size[0], self.size[1])


    def forward(self) -> None:
        dx = self.speed * math.sin(self.direction)
        dy = self.speed * math.cos(self.direction)

        if self.fmap.check_wall(self.get_rect().move(dx, 0)):
            self.x += dx

        if self.fmap.check_wall(self.get_rect().move(0, dy)):
            self.y += dy


    def backward(self) -> None:
        if self.fmap.check_wall(self.check_backward()):
            self.x -= self.speed * math.sin(self.direction)
            self.y -= self.speed * math.cos(self.direction)


    def rturn(self) -> None:
        self.direction -= self.turning_speed


    def lturn(self) -> None:
        self.direction += self.turning_speed


    def shot(self) -> Bullet:
        if time.time() - self.last_shoot_time > self.shot_cd:
            self.last_shoot_time = time.time()
            self.bullets.append(Bullet(self.window, self.x + self.radius, self.y + self.radius, self.direction))
            self.sound_shot.play()


    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(self.x, self.y, self.size[0], self.size[1])


    def reposition(self) -> None:
        self.x = random.randint(0, self.window.get_width() - self.radius * 2)
        self.y = random.randint(0, self.window.get_height() - self.radius * 2)

    
    def update_vision_rect(self) -> None:
        self.vision_rect = pygame.Rect(self.x + self.radius - self.vision, self.y + self.radius - self.vision,
                                       self.vision * 2, self.vision * 2)


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
