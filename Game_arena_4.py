import random, time, os
from termcolor import colored, cprint
import ctypes
kernel32 = ctypes.windll.kernel32
kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)

class Enemy:
    def __init__(self, typ, name=''):
        self.typ = typ
        self.name = name
        if self.typ == 'Skeleton':
            x, y = 5, 10
        elif self.typ == 'Goblin':
            x, y = 10, 20
        elif self.typ == 'Orc':
            x, y = 25, 50
        elif self.typ == 'Ogre':
            x, y = 50, 90
        elif self.typ == 'Dragon':
            x, y = 80, 150
        elif self.typ == 'Boss':
            x, y = 200, 400

        self.health = 10 * random.randint(x, y)
        self.power = 2 * random.randint(x, y)
        self.maxhealth = self.health

    def is_dead(self):
        return self.health <= 0

    def get_damage(self, damage):
        self.health -= damage
        if self.health < 0:
            self.health = 0
        if self.health > self.maxhealth:
            self.health = self.maxhealth

    def power_change(self, points):
        self.power += points
        if self.power < self.maxhealth//10:
            self.power = self.maxhealth//10

    def attack(self, dodge=0.1):
        r = random.random()
        if r >= 0.95:
            self.power_change(+round(self.power/20))
            return 5 * self.power + random.randint(int(-self.power * 0.2), int(self.power * 0.2))
        if r >= dodge:
            return self.power + random.randint(int(-self.power * 0.2), int(self.power * 0.2))
        elif r <= 0.1:
            self.power_change(-round(self.power/20))
        return 0

    def talk(self):
        pass

    def death(self):
        print(self.typ, self.name, colored('is defeated!', 'cyan'))

class Player:
    def __init__(self, name=''):
        self.name = name
        self.health = 500
        self.maxhealth = self.health
        self.power = 100
        
        self.killed_enemies = 0
        self.get_maxhealth = 0
        self.get_power = 0
        return

    def get_damage(self, damage):
        self.health -= damage
        if self.health < 0:
            self.health = 0
        if self.health > self.maxhealth:
            self.health = self.maxhealth

    def power_change(self, points):
        self.power += points
        if self.power < self.maxhealth//10:
            self.power = self.maxhealth//10

    def attack(self, dodge=0.1):
        r = random.random()
        if r >= 0.95:
            self.power_change(+round(self.power/20))
            return 5 * self.power + random.randint(int(-self.power * 0.2), int(self.power * 0.2))
        if r >= dodge:
            return self.power + random.randint(int(-self.power * 0.2), int(self.power * 0.2))
        elif r <= 0.1:
            self.power_change(-round(self.power/20))
        return 0

    def level_up():
        pass
        
    def talk(self):
        pass

    def is_dead(self):
        return self.health <= 0

def gen_enemy_list(n):
    types = ['Skeleton', 'Goblin', 'Orc', 'Ogre', 'Dragon']
    names = ['Griffin', 'Subarashi', 'David', 'Vladushka', 'Zhek', 'Arkasha', 'Danya', 'Soke']
    enemy_list = []
    for i in range(n):
        enemy_list += [Enemy(random.choice(types), random.choice(names))]
    return enemy_list

def print_screen(stats, actions):
    print(*stats, '\n')
    for i in actions:
        print(*i)

def main():
    global actions, action
    player = Player(input('Enter the name of your hero: '))
    print('Your task is to defeat all monsters and stay alive, good luck!')
    print('To attack press a, to block press b\n')
    input('Print anything to start: ')
    enemy_list = gen_enemy_list(15)
    actions = []
    flag = False
    time.sleep(1)
    os.system('cls')
    while enemy_list:
        enemy = enemy_list[0]
        stats = (enemy.typ, enemy.name, 'have', colored(str(enemy.health), 'red') + '/' + colored(str(enemy.maxhealth), 'red'), 'health and', colored(enemy.power, 'yellow'),
                 'power, \nYou have', colored(str(player.health), 'green') + '/' + colored(str(player.maxhealth), 'green'), 'health and', colored(player.power, 'yellow'), 'power')
        print_screen(stats, actions)
        if len(actions) > 20:
            actions.pop(0)

        if player.is_dead():
            print(colored('Death.', 'red'))
            time.sleep(2)
            os.system('cls')
            print(colored('\n\n\tYou died', 'red'))
            break
        
        if enemy.is_dead():
            enemy.death()
            enemy_list.pop(0)
            
            player.maxhealth += enemy.maxhealth//3
            player.get_damage(-2*enemy.maxhealth//3)
            player.power_change(enemy.power//3)
            
            player.get_maxhealth += enemy.maxhealth//3
            player.get_power += enemy.power//3
            player.killed_enemies += 1
            
            time.sleep(2)
            actions = []
            if len(enemy_list) != 0:
                os.system('cls')
            else:
                if flag == False:
                    flag == True
                    enemy = Enemy('Boss', 'Mirror of ' + player.name)
                    enemy_list += [enemy]
                    enemy.health, enemy.maxhealth, enemy.power = player.health, player.maxhealth, player.power
                    os.system('cls')
            continue
        
        action = input('Your action: ')
        if action == 'a' or action == 'attack':
            player_damage = player.attack()
            enemy.get_damage(player_damage)
            actions += [['You dealt', colored(player_damage, 'green'), 'damage,']]
            
        elif action == 'b' or action == 'block':
            player_damage = int(2 * (2*player.attack()+enemy.attack())/3)
            player.get_damage(-player_damage)
            player.power_change(-round(player.power/100))
            actions += [['You restored', colored(player_damage, 'cyan'), 'health,']]
            
        elif action == 'cheat':
            actions += [(colored('Cheater', 'yellow'), '')]
            player.maxhealth += 10000
            player.health += 10000
            player.power += 1000
            os.system('cls')
            continue

        elif action == 'death':
            actions += [(colored('Death', 'red'), '')]
            player.health = 0
            os.system('cls')
            continue

        elif action == 'win':
            actions += [(colored('Win', 'cyan'), '')]
            break
        
        elif action == 's' or action == 'stat':
            actions += [(colored('(Killed enemies ' + str(player.killed_enemies) + ', stolen ' + str(player.get_maxhealth) +
                    ' health and ' + str(player.get_power) + ' power)', 'magenta'), '')]
            os.system('cls')
            continue
        
        else:
            actions += [(colored('Some nonsense', 'white'), '')]
            os.system('cls')
            continue

        if enemy.health > 0 and (enemy.health/enemy.maxhealth) <= 0.5 and random.random() <= 0.5:
            enemy_damage = int(2 * (player.attack() + 2*enemy.attack())/3)
            enemy.power_change(-round(enemy.power/100))
            enemy.get_damage(-enemy_damage)
            actions[-1] += ['enemy restored', colored(enemy_damage, 'cyan'), 'health.']
        else:
            enemy_damage = enemy.attack()
            player.get_damage(enemy_damage)
            actions[-1] += ['enemy deal you', colored(enemy_damage, 'red'), 'damage.']
            
        os.system('cls')
        
    if not player.is_dead():
        time.sleep(1)
        os.system('cls')
        print(colored('\n\n\tYou win!', 'cyan'))
    time.sleep(4)
    return None

while True:
    os.system('cls')
    main()
