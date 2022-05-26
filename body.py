import random
from termcolor import colored

class Body:
    def __init__(self):
        pass

    def attack(self, dodge=0.1): # определение нанесённого урона
        r = random.random()
        if r >= 0.95:
            self.power_change(+round(self.power/20))
            return 3 * self.power + random.randint(int(-self.power * 0.2), int(self.power * 0.2))
        if r >= dodge:
            return self.power + random.randint(int(-self.power * 0.2), int(self.power * 0.2))
        elif r <= 0.05:
            self.power_change(-round(self.power/20))
        return 0

    def healing(self, opponent):
        return int(1.5 * (2 * self.attack() + opponent.attack()) / 3)

    def get_damage(self, damage): # получение урона
        self.health -= damage
        if self.health < 0:
            self.health = 0

    def get_healing(self, heal):
        self.health += heal
        if self.health > self.maxhealth:
            self.health = self.maxhealth
                    
    def power_change(self, points): # изменение силы
        self.power += points
        if self.power < self.maxhealth//10:
            self.power = self.maxhealth//10

    def is_dead(self):
        return self.health <= 0


class Enemy(Body):
    def __init__(self, typ, name=''):
        self.typ = typ
        self.name = name
        global types_of_enemies

        x = types_of_enemies[self.typ]['x']
        y = types_of_enemies[self.typ]['y']

        self.health = 10 * random.randint(x, y)
        self.power = 2 * random.randint(x, y)
        self.maxhealth = self.health

    def death(self):
        print(f"{self.typ} {self.name} {colored('is defeated!', 'cyan')}")

    def action(self, player):
        if (self.health/self.maxhealth) < 0.5 and random.random() < 0.5:
            self_heal = self.healing(player)
            self.power_change(-round(self.power/100))
            self.get_healing(self_heal)
            return f"self restored {colored(self_heal, 'cyan')} health."
            
        else:
            self_damage = self.attack()
            player.get_damage(self_damage)
            return f"self deal you {colored(self_damage, 'red')} damage."


class Player(Body):
    def __init__(self, name=''):
        self.name = name
        self.health = 500
        self.maxhealth = self.health
        self.power = 100
        
        self.killed_enemies = 0
        self.got_maxhealth = 0
        self.got_power = 0
        return

    def steal_stats(self, defeated_enemy):
        self.maxhealth += defeated_enemy.maxhealth // 3
        self.get_healing(defeated_enemy.maxhealth // 3 * 2)
        self.power_change(defeated_enemy.power // 3)
        
        self.got_maxhealth += defeated_enemy.maxhealth//3
        self.got_power += defeated_enemy.power//3
        self.killed_enemies += 1

types_of_enemies = {
    'Skeleton': {'x': 10, 'y': 15}, 
    'Goblin': {'x': 15, 'y': 25}, 
    'Orc': {'x': 30, 'y': 60}, 
    'Ogre': {'x': 60, 'y': 90}, 
    'Dragon': {'x': 100, 'y': 170}, 
    'Boss': {'x': 200, 'y': 400}
    } 
