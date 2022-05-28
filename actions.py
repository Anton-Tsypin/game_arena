from termcolor import colored
import pickle, os

class Action:
    def __init__(self, action):
        self.action = action

    def do(self, game):
        message = ['Some nonsense']
        if self.action == '':
            message = ['Some nonsense']

        elif self.action in ['a', 'attack', 'd', 'defense']:
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
        
        elif self.action in ['s', 'stat']:
            message = [colored(f"Killed enemies: {str(game.player.killed_enemies)}, stolen {str(game.player.got_maxhealth)} health and {str(game.player.got_power)} power", 'magenta')]

        elif self.action in ['exit', 'quit', '& D:/Python/python.exe d:/Python/Game_arena/main.py']:
            game.main_game_flag = False
            game.fight_run_flag = False
            message = "Вы вышли из игры"

        elif self.action in ['new', 'new game']:
            game.fight_run_flag = False

        elif self.action.split()[0] == 'save':
            message = self.save(game)

        elif self.action.split()[0] == 'load':
            message = self.load(game)

        elif self.action.split()[0] in ['del', 'delete']:
            message = self.delete()

        elif self.action == 'saves':
            saves = ", ".join(map(lambda name: f'{name[0:-5]}', os.listdir("saves/")))
            message = [f"Список сохранений: [{saves}]"]

        return message


    def save(self, game): # сохранение прогресса
        try:
            if not os.path.exists('saves'): os.makedirs('saves') 
            save_name = "fast" if len(self.action.split()) == 1 else self.action.split()[1]
            save_data = {'player' : game.player, 'enemy_list' : game.enemy_list, 'boss_flag' : game.boss_flag}
            with open(f"saves/{save_name}.save", 'wb') as file:
                pickle.dump(save_data, file)
            message = [colored(f'Сохранение "{save_name}" создано', 'yellow')]
        except:
            message = [colored("Не удалось сохранить", 'yellow')]
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
            message = [colored(f'Сохранение "{save_name}" загружено', 'yellow')]
            game.actions = []
        except:
            message = [colored("Не удалось загрузить сохранение", 'yellow')]
        finally:
            return message


    def delete(self): # удаление сохранения
        try:
            save_name = "fast" if len(self.action.split()) == 1 else self.action.split()[1]
            os.remove(f"saves/{save_name}.save")
            message = [colored(f'Сохранение "{save_name}" удалено', 'yellow')]
        except:
            message = [colored("Не удалось удалить сохранение", 'yellow')]
        finally:
            return message


    def fight_action(self, game): # действие в бою
        if self.action in ['a', 'attack']:
            game.player_damage = game.player.attack(game.enemy)
            game.enemy.get_damage(game.player_damage)
            message = [f"You dealt {colored(game.player_damage, 'green')} damage, "]

        elif self.action in ['d', 'defense']:
            game.player_heal = game.player.healing(game.enemy)
            game.player.get_healing(game.player_heal)
            game.player.power_change(-round(game.player.power/100))
            message = [f"You restored {colored(game.player_heal, 'cyan')} health, "]

        message[0] += game.enemy.action(game.player)
        return message
