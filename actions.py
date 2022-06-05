from termcolor import colored
import pickle, os, time
from body import Enemy


class Action:
    def __init__(self, action):
        self.action = action


    def do(self, game):
        message = ['Some nonsense']
        if self.action == '':
            message = ['Some nonsense']

        if game.place == 'hub':
            av_loc = ', '.join([f"{i+1}) {game.aviable_locations[i]}" for i in range(len(game.aviable_locations))])
            if self.action == 'fight':
                print(f"Choose number of a location for a fighting run: \n{av_loc}")
                choice = input()
                while not choice.isnumeric():
                    choice = input()
                choice = int(choice)-1
                while not (choice >= 0 and choice < len(game.aviable_locations)):
                    print("You are mistaken. Try again.")
                    choice = input()
                    while not choice.isnumeric():
                        choice = input()
                    choice = int(choice)-1
                game.location = game.aviable_locations[choice]
                game.place = "fight"

            elif self.action == 'altar':
                message = ["You donate all the accumulated life energy to the sacrificial altar.\nThe gods liked your sacrifice, but it's not enough"]
                count = (game.player.life_energy * 4) // 5
                game.player.life_energy = 0
                game.player.default_health += count
                game.player.maxhealth = game.player.health = game.player.default_health
                game.player.default_power += count // 4
                game.player.power = game.player.default_power

        elif game.place == 'fight':
            if self.action in ['a', 'attack', 'd', 'defense']:
                message = self.fight_action(game)

            elif self.action == 'cheat':
                game.player.maxhealth += 10000
                game.player.health += 10000
                game.player.power += 1000
                message = [colored('Cheater', 'yellow')]

            elif self.action == 'death':
                message = [(colored('Death.', 'red'))]
                game.player.health = 0

            elif self.action == 'win':
                message = ["Победа!"]
                game.enemy_list = []
                game.fight_run_flag = False


        if self.action == '':
            message = ['Some nonsense']

        elif self.action in ['exit', 'quit', '& D:/Python/python.exe d:/Python/Game_arena/main.py']:
            self.exit(game, True)

        elif self.action in ['new', 'new game', 'start new game']:
            self.exit(game, False)

        elif self.action.split()[0] == 'save':
            message = self.save(game)

        elif self.action.split()[0] == 'load':
            message = self.load(game)

        elif self.action.split()[0] in ['del', 'delete']:
            message = self.delete()

        elif self.action == 'saves':
            saves = ", ".join(map(lambda name: f'{name[0:-5]}', os.listdir("saves/")))
            message = [f"Save list: [{saves}]"]

        elif self.action in ['s', 'stat']:
            message = [colored(f"Killed enemies: {str(game.player.killed_enemies)}, stolen {str(game.player.got_maxhealth)} health and {str(game.player.got_power)} power", 'magenta')]

        return message


    def save(self, game): # сохранение прогресса
        try:
            if not os.path.exists('saves'): os.makedirs('saves') 
            save_name = "fast" if len(self.action.split()) == 1 else self.action.split()[1]

            if save_name in os.listdir("saves/"): mes = "updated"
            else: mes = "created"
        
            save_data = {
                'player' : game.player, 
                'enemy_list' : game.enemy_list, 
                'boss_flag' : game.boss_flag,
                'place' : game.place,
                'location' : game.location
                }
            with open(f"saves/{save_name}.save", 'wb') as file:
                pickle.dump(save_data, file)
            message = [colored(f'Save "{save_name}" {mes}', 'yellow')]
        except:
            message = [colored("Failed to save", 'red')]
        finally:
            return message


    def load(self, game): # загрузка сохранения
        try:
            save_name = "fast" if len(self.action.split()) == 1 else self.action.split()[1]
            with open(f"saves/{save_name}.save", 'rb') as file:
                save_data = pickle.load(file)
                game.player = save_data['player']
                game.enemy_list = save_data['enemy_list']
                game.boss_flag = save_data['boss_flag']
                game.place = save_data['place']
                game.location = save_data['location']
            message = [colored(f'Save "{save_name}" loaded', 'yellow')]
            game.actions = []
            game.print_screen()
        except:
            message = [colored("Failed to load save", 'red')]
        finally:
            return message


    def delete(self): # удаление сохранения
        try:
            save_name = "fast" if len(self.action.split()) == 1 else self.action.split()[1]
            os.remove(f"saves/{save_name}.save")
            message = [colored(f'Save "{save_name}" deleted', 'yellow')]
        except:
            message = [colored("Failed to delete save", 'red')]
        finally:
            return message


    def fight_action(self, game): # действие в бою
        if self.action in ['a', 'attack']:
            game.player_damage = game.player.attack(game.enemy)
            game.enemy.get_damage(game.player_damage)
            message = [f"You dealt {colored(game.player_damage, 'green')} damage."]                        

        elif self.action in ['d', 'defense']:
            game.player_heal = game.player.healing(game.enemy)
            game.player.get_healing(game.player_heal)
            game.player.power_change(-round(game.player.power/100))
            message = [f"You restored {colored(game.player_heal, 'cyan')} health."]

        if game.enemy.is_dead():
            game.print_screen()
            print(message[0])
            print(game.enemy.death())
            game.enemy_list.pop(0)
            
            game.player.steal_stats(game.enemy)
            
            time.sleep(2)
            game.actions = []
            return
            if not game.enemy_list and game.player.killed_enemies >= 20:
                if game.boss_flag:
                    game.boss_flag = False
                    game.enemy = Enemy('Boss', f"Mirror of {game.player.name}")
                    game.enemy_list += [game.enemy]
                    game.enemy.health, game.enemy.maxhealth, game.enemy.power = game.player.health, game.player.maxhealth, game.player.power

        message[0] += game.enemy.action(game.player)

        if game.player.is_dead():
            game.print_screen()
            print(message[0])
            time.sleep(2)
            os.system('cls')
            print(f"{colored('You are defeated', 'red')}, you can {colored('load', 'cyan')} a save, start {colored('new', 'green')} game or {colored('die', 'yellow')} with dignity")
            attempts = 0
            while attempts < 3:
                attempts += 1
                action = Action(input('Your choice: '))
                if action.action[0:4] == "load":
                    message = action.do(game)
                    break
                elif action.action in ['new', 'new game', 'start new game']:
                    self.exit(game, False)
                    break
                elif action.action in ['die', 'exit', 'quit', 'dignity', 'die with dignity']:
                    self.exit(game, True)
                    break
            else:
                self.exit(game, True)
            game.actions = []
                    
        return message


    def exit(self, game, break_cycle=True):
        game.main_game_flag = False
        game.place = None
        game.cycle = not break_cycle
