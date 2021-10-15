# Ramon Asuncion and Quan Nguyen
# Monday, September 13, 11:00 PM
# CSCI 204 - Dancy
# Project 1, Phase 1
from River import River
from hashlib import new
import random

class Ecosystem:
	def __init__(self, filename):
		'''
		Constructor that reads the file data and stores it in a list.
			Arguments:
			Arg1: [String] Receives the file name.
			...
		'''
		self.river_list = []
		new_river_list = []
		self.filename = filename
		try:
			with open(filename) as file:
				#Strip blank lines
				self.river_list = [line.split() for line in file if line.strip() != ""]

				for j in range(len(self.river_list)):
					#Generate Object
					name_dict = {'B':Bear(),'F':Fish(),'N':None}
					self.river_list[j][0] = name_dict[self.river_list[j][0]]
					if self.river_list[j][0] is not None:
						#Change shorten sex name to full name
						name_dict = {'M':'Male','F':'Female'}
						self.river_list[j][1] = name_dict[self.river_list[j][1]]
						
						#Assign stats to characters
						setattr(self.river_list[j][0], 'sex', self.river_list[j][1])
						setattr(self.river_list[j][0], 'strength', float(self.river_list[j][2]))
						
						# Create a new 1D list instead of 2D
						new_river_list.append(self.river_list[j][0])
					
					else:
						new_river_list.append(self.river_list[j][0])
				
				#update river_list
				self.river_list = new_river_list
				
				#print original input to output file
				self.save_to_output(self.river_list)
		
		except FileNotFoundError:
			print("File {} not found!".format(filename))
			self.quit()

	def get_size(self):
		''' Returns the size of the river '''
		return len(self.river_list) 

	def collision(self,i1,i2):
		'''Determine the type of interaction'''
		if isinstance(i1, Bear) and isinstance(i2,Fish):
			return 'eat'
		elif isinstance(i1,Fish) and isinstance(i2,Bear):
			return 'scared'
		elif isinstance(i1,Fish) and isinstance(i2,Fish):
			if i1.sex != i2.sex:
				return 'mate'
			else:
				return 'fight'
		elif isinstance(i1,Bear) and isinstance(i2,Bear):
			if i1.sex != i2.sex:
				return 'mate'
			else:
				return 'fight'
	def step(self):
		''' Moves the whole river one step forward in time.
		At the end, it should also print the state of the river
		to an output file at the end of the each step
		'''
		old_river = self.river_list[:]
		self.river_list.insert(0,self.river_list.pop()) 
		new_river = self.river_list
		for i in range(self.get_size()-1):
			# Bear eats fish. 
			if self.collision(old_river[i],old_river[i+1]) == 'eat':
				old_river[i].eating(old_river[i+1])
				index = new_river.index(old_river[i+1])
				new_river[index] = None
			# Fish does not move when interacts with a bear. 
			elif self.collision(old_river[i],old_river[i+1]) == 'scared':
					new_river[i] = old_river[i]
					new_river[i+1] = None	
			# If fish/bear collies with fish/bear the left one does the move.
			elif self.collision(old_river[i],old_river[i+1]) == 'mate':
				new_river[i] = old_river[i]
				new_river[i+1] = None
				# Spawns a baby randomly. 
				none_indices = [i for i, x in enumerate(new_river) if x == None]
				if len(none_indices) > 0:
					new_river[random.choice(none_indices)] = Animal.mating(old_river[i],old_river[i+1])
			# If bear collides with bear the left one does not move
			elif self.collision(old_river[i],old_river[i+1]) == "fight":
					loser= Animal.fighting(old_river[i],old_river[i+1])[1]
					index = new_river.index(loser)
					new_river[index] = None
		return self.save_to_output(self.river_list)

	def get_inhabitant(self, index):
		''' Returns the item at this index of the river.
		It should either be a Bear, Fish, or None
		'''
		return self.river_list[index]

	def save_to_output(self, data):
		# TODO:the original list needs to be saved to output probably call the save_to_output function it in the constructor
		with open('output.txt', 'a') as f:
			f.write('\n'.join([str(index) for index in data])+ '\n\n')

	def quit(self):
		'''Called when program quits. Close your output file.'''
		print ('Exiting program.')
		exit(0)
    
    
class Animal(Ecosystem):
	def __init__(self):
		self.strength = float()
		self.sex = str()
				
	def eating(self,i2):
		self.strength += i2.strength

	def mating(i1,i2):
		'''Creating a new Animal object as a child for i1 and i2 with random sex and mean strength'''
		if isinstance(i1,Fish):
			i3 = Fish()
		else:
			i3 = Bear()
		i3.strength = (i1.strength + i2.strength)/2
		i3.sex = random.choice(['Male','Female'])
		return i3

	def fighting(i1, i2):
		'''Determine if i1 or i2 won and return the (victor,loser) tuple with the victor's reduced strength, if both are the same then both get destroyed'''
		if i1.strength > i2.strength:
			i1.strength -= i2.strength
			return (i1,i2)
		elif i2.strength > i1.strength:
			i2.strength -= i1.strength
			return (i2,i1)
		else:
			return None
	
	def get_strength(self):
		return str(self.strength)

	def get_sex(self):
		return str(self.sex)
# Create class for Bear
class Bear(Animal):
	def __init__(self):
		super().__init__()
		self.NAME = 'bear'
		
	def get_image(self):
		return  self.NAME + '.ppm'
	
	
	def __str__(self):
		return '{} {} {}'.format('Bear',self.sex,self.strength)
		
# Create class for Fish
class Fish(Animal):
	def __init__(self):
		super().__init__()
		self.NAME = 'salmon'

	def __str__(self):
		return '{} {} {}'.format('Fish',self.sex,self.strength)

	def get_image(self):
		return self.NAME + '.ppm'


