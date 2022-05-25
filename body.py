import random
from termcolor import colored

class Body:
	def __init__(self):
		pass

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

	def is_dead(self):
		return self.health <= 0


class Enemy(Body):
	def __init__(self, typ, name=''):
		self.typ = typ
		self.name = name
		if self.typ == 'Skeleton':
			x, y = 10, 15
		elif self.typ == 'Goblin':
			x, y = 15, 25
		elif self.typ == 'Orc':
			x, y = 30, 60
		elif self.typ == 'Ogre':
			x, y = 60, 90
		elif self.typ == 'Dragon':
			x, y = 100, 170
		elif self.typ == 'Boss':
			x, y = 200, 400

		self.health = 10 * random.randint(x, y)
		self.power = 2 * random.randint(x, y)
		self.maxhealth = self.health

	def death(self):
		print(self.typ, self.name, colored('is defeated!', 'cyan'))


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
		self.maxhealth += defeated_enemy.maxhealth//3
		self.get_damage(-2*defeated_enemy.maxhealth//3)
		self.power_change(defeated_enemy.power//3)
		
		self.got_maxhealth += defeated_enemy.maxhealth//3
		self.got_power += defeated_enemy.power//3
		self.killed_enemies += 1
