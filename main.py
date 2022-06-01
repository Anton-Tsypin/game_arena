import random, time, os
from termcolor import colored
from body import Player, Enemy
from actions import Action


class Game:
    def __init__(self):
        self.player = Player()
        self.fight_run_flag = False
        self.main_game_flag = True
        self.hub_flag = False
        self.continuation = None
        self.enemy = None
        self.location = "Forest"
        self.aviable_locations = ["Forest", "Greenskin caves", "Mountains"]
        self.enemy_list = []


    def gen_enemy_list(self, n, types=None):
        if types == None:
            types = ['Wolf', 'Goblin', 'Orc', 'Ogre', 'Dragon']
        names = ['Griffin', 'Subarashi', 'David', 'Vladushka', 'Zhek', 'Arkasha', 'Danya', 'Soke']
        enemy_list = []
        for i in range(n):
            enemy_list += [Enemy(random.choice(types), random.choice(names))]
        return enemy_list


    def print_screen(self): # отрисовка текста на экране
        os.system('cls')
        if self.location == "Forgotten city":
            print(f"You have arrived in the {colored('Forgotten city', 'magenta')}.")
            print(f"The city's holy gates have {colored('cleansed', 'yellow')} you of stolen stats.")
            print(f"You can permanently improve your stats. Go to the sacrificial altar. Command: altar")
            print(f"Also you can go to fighting run. Command: fight\n")
            pl_dhl, pl_dpw, pl_le = colored(str(self.player.default_health), 'green'), colored(self.player.default_power, 'yellow'), colored(self.player.life_energy, 'magenta')
            player_stats = f"You have {pl_dhl} health, {pl_dpw} power and {pl_le} life energy.\n"
            print(player_stats)
        else:
            en_hl, en_mhl, en_pw = colored(str(self.enemy.health), 'red'),  colored(str(self.enemy.maxhealth), 'red'), colored(self.enemy.power, 'yellow')
            pl_hl, pl_mhl, pl_pw = colored(str(self.player.health), 'green'), colored(str(self.player.maxhealth), 'green'), colored(self.player.power, 'yellow')
            player_stats = f"You have {pl_hl}/{pl_mhl} health and {pl_pw} power."
            enemy_stats = f"{self.enemy.typ} {self.enemy.name} have {en_hl}/{en_mhl} health and {en_pw} power."
            print(f"Location: {self.location}\n{player_stats}\n{enemy_stats}\n")

        for action in self.actions:
            print(action)


    def fight_run(self, location, enemy_list=None):
        os.system('cls')
        print(f"You have arrived at the {location}")
        time.sleep(2)
        if enemy_list == None:
            if location == 'Forest':
                enemy_list = self.gen_enemy_list(5, ['Wolf', 'Goblin', 'Orc'])
            elif location == 'Greenskin caves':
                enemy_list = self.gen_enemy_list(5, ['Goblin', 'Orc', 'Ogre'])
            elif location == 'Mountains':
                enemy_list = self.gen_enemy_list(5, ['Orc', 'Ogre', 'Dragon'])

        self.enemy_list = enemy_list
        self.actions = []
        self.boss_flag = True
        self.fight_run_flag = True
        self.continuation = True
        while self.enemy_list and self.fight_run_flag:
            self.enemy = self.enemy_list[0]
            self.print_screen()
            if len(self.actions) > 16:
                self.actions.pop(0)
            
            action = Action(input('Your action: '))
            message = action.do(self, 'fight')
            if message:
                self.actions += message

        return self.continuation


    def hub(self):
        self.location = 'Forgotten city'
        self.actions = []
        self.player.maxhealth = self.player.default_health
        self.player.health = self.player.default_health
        self.player.power = self.player.default_power
        self.hub_flag = True

        while self.hub_flag:
            self.print_screen()
            if len(self.actions) > 16:
                self.actions.pop(0)
            action = Action(input("Your action: "))
            message = action.do(self, 'hub')
            self.actions += message
        

    def main(self):
        print('Your task is to defeat all monsters and stay alive, good luck!')
        print('To attack press a, to defend press d\n')
        self.player.name = input('Enter your name, hero: ')
        os.system('cls')
        self.cycle = True
        self.fight_run_flag = True

        while self.main_game_flag:
            if self.fight_run_flag:
                self.fight_run(self.location)
                self.fight_run_flag = False
                self.hub_flag = True
            elif self.hub_flag:
                self.hub()
                self.fight_run_flag = True
                self.hub_flag = False

        return self.cycle
        



os.system('cls')
while Game().main():
    os.system('cls')
os.system('cls')
