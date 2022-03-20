import pygame
import math
import random
from first_map import FirstMap
from player import Player


class NPC(Player):
    def __init__(self, window: pygame.Surface, fmap: FirstMap) -> None:
        super().__init__(window, fmap)
        self.color = (255, 0, 0)
        self.enemy_rect = None
        self.action = 'start'
        self.actions = {
            'start': self.start,
            'turn_to_enemy': self.turn_to_enemy,
            'fire': self.fire,
            'move': self.move,
            'forward': self.forward,
            'backward': self.backward,
            'rturn': self.rturn,
            'lturn': self.lturn
        }
        self.movements = ('forward', 'backward', 'rturn', 'lturn')
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
                if vision_rect.colliderect(player.get_rect()):
                    return player.get_rect()
        except TypeError:
            return None

        return None


    def turn_to_enemy(self) -> None:
        try:
            m_rect = self.get_rect()

            # (x, y) - direction line point
            dir_point = (
                m_rect.centerx + self.view_range * math.sin(self.direction),
                m_rect.centery + self.view_range * math.cos(self.direction)
            )

            # direction vector
            me_dx = m_rect.centerx - (dir_point[0])
            me_dy = m_rect.centery - (dir_point[1])

            # vector to enemy
            enemy_dx = m_rect.centerx - self.enemy_rect.centerx
            enemy_dy = m_rect.centery - self.enemy_rect.centery

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
            self.movement_number = random.randint(5, random.randint(20, 50))
            # если был поворот, то следующее - движение
            if self.prev_move_is_turn:
                self.current_movement = self.movements[random.randint(0, 1)]
                self.prev_move_is_turn = False
            else:
                self.current_movement = self.movements[random.randint(0, len(self.movements) - 1)]
                if self.current_movement.find('turn') != -1:
                    self.prev_move_is_turn = True

        if self.movement_counter > self.movement_number:
            self.movement_number = 0
            self.movement_counter = 0
            self.action = 'start'
            return
        
        self.movement_counter += 1
        self.action = self.current_movement


    def forward(self) -> None:
        super().forward()
        self.action = 'start'


    def backward(self) -> None:
        super().backward()
        self.action = 'start'


    def lturn(self) -> None:
        super().lturn()
        self.action = 'start'


    def rturn(self) -> None:
        super().rturn()
        self.action = 'start'
