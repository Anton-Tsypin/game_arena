import random, time, os
from termcolor import colored, cprint
from body import Player, Enemy

def gen_enemy_list(n, types=None):
	if types == None:
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
	player = Player(input('Enter the name of your hero: '))
	print('Your task is to defeat all monsters and stay alive, good luck!')
	print('To attack press a, to block press d\n')
	input('Print anything to start: ')
	enemy_list = gen_enemy_list(5, types=['Skeleton', 'Goblin', 'Orc'])
	enemy_list += gen_enemy_list(5, types=['Goblin', 'Orc', 'Ogre'])
	enemy_list += gen_enemy_list(5, types=['Orc', 'Ogre', 'Dragon'])
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
			
			player.steal_stats(enemy)
			
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
			
		elif action == 'd' or action == 'defense':
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
			player.health = 0
			os.system('cls')
			continue

		elif action == 'win':
			break
		
		elif action == 's' or action == 'stat':
			actions += [(colored('(Killed enemies ' + str(player.killed_enemies) + ', stolen ' + str(player.got_maxhealth) +
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
