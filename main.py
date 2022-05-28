import random, time, os
from termcolor import colored
from body import Player, Enemy
from actions import Action


class Game:
    def __init__(self):
        self.player = Player()
        self.fight_run_flag = True
        self.main_game_flag = True
        self.enemy = None

    def gen_enemy_list(self, n, types=None):
        if types == None:
            types = ['Skeleton', 'Goblin', 'Orc', 'Ogre', 'Dragon']
        names = ['Griffin', 'Subarashi', 'David', 'Vladushka', 'Zhek', 'Arkasha', 'Danya', 'Soke']
        enemy_list = []
        for i in range(n):
            enemy_list += [Enemy(random.choice(types), random.choice(names))]
        return enemy_list

    def print_screen(self, stats, actions): # отрисовка текста на экране
        os.system('cls')
        print(stats, '\n')
        for action in actions:
            print(action)

    def main(self):
        print('Your task is to defeat all monsters and stay alive, good luck!')
        print('To attack press a, to defend press d\n')
        self.player.name = input('Enter your name, hero: ')
        self.enemy_list = self.gen_enemy_list(5, types=['Skeleton', 'Goblin', 'Orc'])
        self.enemy_list += self.gen_enemy_list(5, types=['Goblin', 'Orc', 'Ogre'])
        self.enemy_list += self.gen_enemy_list(5, types=['Orc', 'Ogre', 'Dragon'])
        actions = []
        self.boss_flag = True
        
        time.sleep(1)
        os.system('cls')
        while self.enemy_list and self.fight_run_flag:
            self.enemy = self.enemy_list[0]
            en_hl, en_mhl, en_pw = colored(str(self.enemy.health), 'red'),  colored(str(self.enemy.maxhealth), 'red'), colored(self.enemy.power, 'yellow')
            pl_hl, pl_mhl, pl_pw = colored(str(self.player.health), 'green'), colored(str(self.player.maxhealth), 'green'), colored(self.player.power, 'yellow')
            stats = f"{self.enemy.typ} {self.enemy.name} have {en_hl}/{en_mhl} health and {en_pw} power \nYou have {pl_hl}/{pl_mhl} health and {pl_pw} power"
            self.print_screen(stats, actions)
            if len(actions) > 16:
                actions.pop(0)

            if self.player.is_dead():
                os.system('cls')
                print(colored('\n\n\tYou died', 'red'))
                time.sleep(4)
                break
            
            if self.enemy.is_dead():
                self.enemy.death()
                self.enemy_list.pop(0)
                
                self.player.steal_stats(self.enemy)
                
                time.sleep(2)
                actions = []
                if not self.enemy_list:
                    if self.boss_flag:
                        self.boss_flag = False
                        self.enemy = Enemy('Boss', f"Mirror of {self.player.name}")
                        self.enemy_list += [self.enemy]
                        self.enemy.health, self.enemy.maxhealth, self.enemy.power = self.player.health, self.player.maxhealth, self.player.power
                continue
            
            action = Action(input('Your action: '))
            message = action.do(self)
            actions += message
            
        if not (self.enemy_list or self.player.is_dead()):
            os.system('cls')
            print(colored('\n\n\tYou win!', 'cyan'))
            time.sleep(4)
        return self.main_game_flag

os.system('cls')
while Game().main():
    os.system('cls')
os.system('cls')
