import random, time, os
import pickle
from termcolor import colored
from body import Player, Enemy

def gen_enemy_list(n, types=None):
    if types == None:
        types = ['Skeleton', 'Goblin', 'Orc', 'Ogre', 'Dragon']
    names = ['Griffin', 'Subarashi', 'David', 'Vladushka', 'Zhek', 'Arkasha', 'Danya', 'Soke']
    enemy_list = []
    for i in range(n):
        enemy_list += [Enemy(random.choice(types), random.choice(names))]
    return enemy_list

def print_screen(stats, actions): # отрисовка текста на экране
    os.system('cls')
    print(stats, '\n')
    for action in actions:
        print(action)

def main():
    print('Your task is to defeat all monsters and stay alive, good luck!')
    print('To attack press a, to defend press d\n')
    player = Player(input('Enter your name, hero: '))
    enemy_list = gen_enemy_list(5, types=['Skeleton', 'Goblin', 'Orc'])
    enemy_list += gen_enemy_list(5, types=['Goblin', 'Orc', 'Ogre'])
    enemy_list += gen_enemy_list(5, types=['Orc', 'Ogre', 'Dragon'])
    actions = []
    boss_flag = True
    time.sleep(1)
    os.system('cls')
    while enemy_list:
        enemy = enemy_list[0]
        en_hl, en_mhl, en_pw = colored(str(enemy.health), 'red'),  colored(str(enemy.maxhealth), 'red'), colored(enemy.power, 'yellow')
        pl_hl, pl_mhl, pl_pw = colored(str(player.health), 'green'), colored(str(player.maxhealth), 'green'), colored(player.power, 'yellow')
        stats = f"{enemy.typ} {enemy.name} have {en_hl}/{en_mhl} health and {en_pw} power \nYou have {pl_hl}/{pl_mhl} health and {pl_pw} power"
        print_screen(stats, actions)
        if len(actions) > 16:
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
            
            player.steal_stats(enemy)
            
            time.sleep(2)
            actions = []
            if not enemy_list:
                if boss_flag:
                    boss_flag = False
                    enemy = Enemy('Boss', f"Mirror of {player.name}")
                    enemy_list += [enemy]
                    enemy.health, enemy.maxhealth, enemy.power = player.health, player.maxhealth, player.power
            continue
        
        action = input('Your action: ')
        if action in ['a', 'attack']:
            player_damage = player.attack(enemy)
            enemy.get_damage(player_damage)
            actions += [f"You dealt {colored(player_damage, 'green')} damage, "]
            
        elif action in ['d', 'defense']:
            player_heal = player.healing(enemy)
            player.get_healing(player_heal)
            player.power_change(-round(player.power/100))
            actions += [f"You restored {colored(player_heal, 'cyan')} health, "]
            
        elif action == 'cheat':
            actions += [colored('Cheater', 'yellow')]
            player.maxhealth += 10000
            player.health += 10000
            player.power += 1000

        elif action == 'death':
            player.health = 0

        elif action == 'win':
            break
        
        elif action in ['s', 'stat']:
            actions += [colored(f"Killed enemies: {str(player.killed_enemies)}, stolen {str(player.got_maxhealth)} health and {str(player.got_power)} power", 'magenta')]

        elif action in ['exit', 'quit', '& D:/Python/python.exe d:/Python/Game_arena/main.py']:
            return False
        
        elif action == 'save':
            try:
                save_data = {'player' : player, 'enemy_list' : enemy_list}
                with open('save.save', 'wb') as file:
                    pickle.dump(save_data, file)
                actions += [colored("Сохранение создано", 'yellow')]
            except:
                actions += [colored("Не удалось сохранить", 'yellow')]

        elif action == 'load':
            try:
                with open('save.save', 'rb') as file:
                    save_data = pickle.load(file)
                    player = save_data['player']
                    enemy_list = save_data['enemy_list']
                actions += [colored("Сохранение загружено", 'yellow')]
            except:
                actions += [colored("Не удалось загрузить сохранение", 'yellow')]

        else:
            actions += ["Some nonsense"]

        if action in ['a', 'attack', 'd', 'defense']:
            actions[-1] += enemy.action(player)
        
    if not (enemy_list or player.is_dead()):
        os.system('cls')
        print(colored('\n\n\tYou win!', 'cyan'))
    time.sleep(4)
    return True

os.system('cls')
while main():
    os.system('cls')
os.system('cls')
