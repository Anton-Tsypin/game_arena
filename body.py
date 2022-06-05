import random
from termcolor import colored


class Body:
    def __init__(self):
        pass


    def __lt__(self, other):
        return (self.health + self.power * 5) < (other.health + other.power * 5)


    def attack(self, opponent, dodge=0.1): # определение нанесённого урона
        r = random.random()
        standart_damage = random.randint(int(self.power * 0.8), int(self.power * 1.2))
        damage = 0
        
        if r >= 0.95: # крит
            self.power_change(self.power//20)
            critical_damage = standart_damage * 2
            critical_damage = int(opponent.maxhealth * 0.5) if critical_damage > int(opponent.maxhealth * 0.5) else critical_damage
            damage = standart_damage + critical_damage
            
        if r >= dodge: # обычный удар
            damage =  standart_damage

        elif r <= 0.05: # очень неудачный удар
            self.power_change(-self.power//20)

        return damage


    def healing(self, opponent): # определение полученного лечения
        heal = int(1.5 * (2 * self.attack(opponent) + opponent.attack(self)) / 3)
        return heal


    def get_damage(self, damage): # получение урона
        self.health -= damage
        if self.health < 0:
            self.health = 0


    def get_healing(self, heal): # получение лечения
        self.health += heal
        if self.health > self.maxhealth:
            self.health = self.maxhealth


    def power_change(self, points): # изменение силы
        self.power += points
        if self.power < self.maxhealth//10:
            self.power = self.maxhealth//10


    def is_dead(self): # проверка на смерть
        return self.health <= 0




class Enemy(Body):
    def __init__(self, typ, name=''):
        self.name = name
        
        # начальные характеристики берутся из глобального словаря по типу моба, затем преобразуются
        self.typ = typ
        global types_of_enemies
        x = types_of_enemies[self.typ]['x']
        y = types_of_enemies[self.typ]['y']

        self.health = 10 * random.randint(x, y)
        self.power = 2 * random.randint(x, y)
        self.maxhealth = self.health
        self.life_energy = 1 + self.health // 100 + self.power // 20

        if random.random() < 0.05: # осквернённый противник имеет меньше здоровья, но больше силы
            self.typ = f"{colored('Desecrated', 'magenta')} {typ}"
            r = (random.random()/2) + 0.1
            self.get_damage(int(self.maxhealth * r))
            self.power_change(int(self.power * r))


    def death(self):
        return f"{self.typ} {self.name} {colored('is defeated!', 'cyan')}"


    def action(self, player): # действие моба
        if (self.health/self.maxhealth) < 0.5 and random.random() < 0.5: # шанс лечения при низком здоровье
            self_heal = self.healing(player)
            self.power_change(-round(self.power/100))
            self.get_healing(self_heal)
            return f" Enemy restored {colored(self_heal, 'cyan')} health."
            
        else: # атака
            self_damage = self.attack(player)
            player.get_damage(self_damage)
            return f" Enemy deal you {colored(self_damage, 'red')} damage."




class Player(Body):
    def __init__(self, name=''):
        self.name = name
        self.default_health = 300
        self.health = self.default_health
        self.maxhealth = self.health
        self.default_power = 60
        self.power = self.default_power
        self.life_energy = 0
        
        self.killed_enemies = 0
        self.got_maxhealth = 0
        self.got_power = 0
        return


    def steal_stats(self, defeated_enemy): # кража характеристик игроком у поверженного врага
        self.maxhealth += defeated_enemy.maxhealth // 3
        self.get_healing(defeated_enemy.maxhealth // 3 * 2)
        self.power_change(defeated_enemy.power // 3)
        self.life_energy += defeated_enemy.life_energy
        
        self.got_maxhealth += defeated_enemy.maxhealth//3
        self.got_power += defeated_enemy.power//3
        self.killed_enemies += 1


    def set_default_stats(self):
        self.maxhealth = self.default_health
        self.health = self.default_health
        self.power = self.default_power


# словарь характеристик мобов по их типу
types_of_enemies = {
    'Wolf': {'x': 10, 'y': 15}, 
    'Goblin': {'x': 15, 'y': 25}, 
    'Orc': {'x': 30, 'y': 60}, 
    'Ogre': {'x': 60, 'y': 90}, 
    'Dragon': {'x': 100, 'y': 170}, 
    'Boss': {'x': 200, 'y': 400}
    } 
