import pygame
import math
import random
from first_map import FirstMap
from player import Player


class NPC(Player):
    def __init__(self, window: pygame.Surface, fmap: FirstMap, settings: dict) -> None:
        super().__init__(window, fmap, settings)
        self.type = 'npc'
        self.color = (255, 0, 0)
        self.turning_speed = 0.1
        self.enemy_rect = None
        self.action = 'start'
        self.actions = {
            'start': self.start,
            'turn_to_enemy': self.turn_to_enemy,
            'fire': self.fire,
            'move': self.move,
            'up': self.up,
            'down': self.down,
            'right': self.right,
            'left': self.left,
            'rturn': self.rturn,
            'lturn': self.lturn
        }
        self.movements = ('up', 'down', 'left', 'right', 'rturn', 'lturn')
        self.current_movement = None
        self.movement_counter = 0
        self.movement_number = 0
        self.prev_move_is_turn = False
    

    def __del__(self):
        return super().__del__()


    def draw(self) -> None:
        super().draw()
        self.actions[self.action]()


    def start(self) -> None:
        self.enemy_rect = self.see_enemy(self.enemies)
        if self.enemy_rect is not None:
            self.movement_counter = 0
            self.movement_number = 0
            self.action = 'turn_to_enemy'
        else:
            self.action = 'move'
        

    def see_enemy(self, players: list[Player]) -> pygame.Rect:
        vision_rect = pygame.Rect(self.x + self.radius - self.vision, self.y + self.radius - self.vision, \
                                  self.vision * 2, self.vision * 2)

        try:
            for player in players:
                if vision_rect.colliderect(player.rect):
                    return player.rect
        except TypeError:
            return None

        return None


    def turn_to_enemy(self) -> None:
        try:
            # (x, y) - direction line point
            dir_point = (
                self.rect.centerx + self.vision * math.sin(self.direction),
                self.rect.centery + self.vision * math.cos(self.direction)
            )

            # direction vector
            me_dx = self.rect.centerx - (dir_point[0])
            me_dy = self.rect.centery - (dir_point[1])

            # vector to enemy
            enemy_dx = self.rect.centerx - self.enemy_rect.centerx
            enemy_dy = self.rect.centery - self.enemy_rect.centery

            cos_angle = ((me_dx * enemy_dx) + (me_dy * enemy_dy)) \
                / math.sqrt(me_dx ** 2 + me_dy ** 2) / math.sqrt(enemy_dx ** 2 + enemy_dy ** 2)

            # from "Cross product"
            sign = me_dx * enemy_dy - me_dy * enemy_dx
            sign = 1 if sign < 0 else -1

            accurancy = random.random() if random.randint(0,1) == 0 else random.random() * -1
            accurancy /= 4
            
            self.direction += sign * math.acos(round(cos_angle, 5)) + accurancy
            self.action = 'fire'
        except Exception:
            self.action = 'start'


    def fire(self) -> None:
        self.shot()
        self.action = 'start'


    def move(self) -> None:
        if self.movement_counter == 0:
            # продолжительность движения
            self.movement_number = random.randint(5, random.randint(20, 30))
            self.current_movement = self.movements[random.randint(0, len(self.movements) - 1)]


        if self.movement_counter > self.movement_number:
            self.movement_number = 0
            self.movement_counter = 0
            self.action = 'start'
            return
        
        self.movement_counter += 1
        self.action = self.current_movement


    def up(self) -> None:
        super().up()
        self.action = 'start'


    def down(self) -> None:
        super().down()
        self.action = 'start'


    def left(self) -> None:
        super().left()
        self.action = 'start'


    def right(self) -> None:
        super().right()
        self.action = 'start'


    def lturn(self) -> None:
        self.direction += self.turning_speed
        self.action = 'start'


    def rturn(self) -> None:
        self.direction -= self.turning_speed
        self.action = 'start'
