import numpy as np
import matplotlib.pyplot as plt

import matplotlib.colors
from matplotlib.animation import FuncAnimation, ArtistAnimation

from random import choice

import time, os

current_time = lambda: time.time()

#Define map colorsy  
levels = [-1, 0, 1]
colors = ['w', 'k']

cmap, norm = matplotlib.colors.from_levels_and_colors(levels, colors)

ppal_dir = os.getcwd()

class FCW(object):
	"""docstring for FCW"""
	def __init__(self, l):
		
		self.l = l

		self.pos = np.zeros((l,2))

		self.head = self.pos[0]
		self.tail = self.pos[-1]

	def set_pos(self, positions):

		for i in range(self.l):

			self.pos[i] =  positions[i]

#Flexible Chainlike Walker model
class FCW_model(object):
	"""docstring for FCW_Model"""
	def __init__(self, L, l, rho):
		
		self.L = L #Lattice length
		self.l = l #FCW length
		self.rho = rho #Density of FCW's

		self.N = int(round(self.rho * self.L**2 / self.l, 0)) #Number of FCW

		self.grid = np.zeros((self.L, self.L))

		self.FCWS = [] #list of lists of positions for each FCW

		self.directions = [np.array([0,1]), np.array([0,-1]), np.array([1,0]), np.array([-1,0])] #Directions to choose for the FCWs

	def init_lattice(self):
		#Initialisation

		if self.N > self.L**2 / self.l:

			raise ValueError('Max number of FCW\'s achieved!')

		taken_pos = []

		while len(self.FCWS) < self.N:

			x_head = np.random.randint(0, self.L - 1)

			x_tail = x_head + self.l

			row = np.random.randint(0, self.L)

			positions = [[row, j % self.L] for j in range(x_head, x_tail)]

			validator = True

			#Check if any of these positions have been taken
			for pos in positions:

				if pos in taken_pos:

					validator = False

			#if any position has been taken don't do anything
			if validator == False:

				pass


			#If all the positions are free then take it
			else:

				for j in range(x_head, x_tail):

					self.grid[row][j % self.L] = 1

				FCW_i = FCW(self.l)
				FCW_i.set_pos(positions)

				taken_pos += positions

				#self.FCWS += positions
				
				self.FCWS.append(FCW_i)

	def plot_lattice(self):

		plt.imshow(self.grid, cmap=cmap)
		plt.show()
		
	def move_walkers(self):
		
		new_pos = np.zeros((self.l, 2))

		mobility = 0

		for fcw in self.FCWS:

			'''
				PROBABLY NOT PYTHON EFFICIENT
			'''
			
			#Choose 1 nearest neighbours poisition
			direction = choice(self.directions)

			#Move the head to the chosen position
			move_to = (fcw.head + direction) % (self.L, self.L)

			#Only move if not occupied
			if self.grid[int(move_to[0])][int(move_to[1])] != 1:

				mobility += 1

				#Update lattice for the tail
				self.grid[int(fcw.tail[0])][int(fcw.tail[1])] = 0

				#Move the other particles following the head
				for i in range(1, self.l):

					new_pos[i] = fcw.pos[i-1]

				#Move the head
				new_pos[0] = move_to

				#Update FCW position
				fcw.set_pos(new_pos)

				#Update lattice for head
				self.grid[int(fcw.head[0])][int(fcw.head[1])] = 1

		return mobility / self.N

	def animate(self, t, save_anim=False):

		self.init_lattice()

		def update(t, lines):

			self.move_walkers()

			lines.set_data(self.grid)

			return lines,

		fig, ax = plt.subplots()

		plt.title('Self assembling chains')

		lines = ax.matshow(self.grid, cmap=cmap)

		anim = FuncAnimation(fig, update, fargs=(lines, ), frames=t,
		                    blit=True, interval=0.1, repeat=False)

		if save_anim == False:

			plt.show()

		else:

			anim.save('FCW_l_%i_rho_%.2f.mp4' % (self.l, self.rho), fps=100, writer="ffmpeg")

	def simulate(self, t, folder="Data"):

		#Use for a single density simulation and store the output data in a folder

		t0 = current_time()

		data_folder = ppal_dir + '/' + folder

		if not os.path.exists(data_folder): os.mkdir(data_folder)

		self.init_lattice()

		#Write data to folder
		os.chdir(data_folder)

		np.save('init_config.npy', self.grid)

		mobility_arr = np.zeros(t)

		for k in range(t):

			print(round(k/t * 100, 2), '%', 'done')

			mobility = self.move_walkers()

			mobility_arr[k] = mobility

		ET = round(current_time() - t0, 2)

		print('\nElapsed time:', ET, 's')

		np.save('mobility.npy', mobility_arr)
		np.save('final_config.npy', self.grid)

		#Write parameters used
		f = open('parameters_used.txt', 'w')

		f.write('L: %i' % self.L)
		f.write('\nl: %i' % self.l)
		f.write('\nDensity: %i' % self.rho)

		f.write('\n\nt: %i' % t)

		f.write('\n\nE.T: %i' % ET)

		f.close()

		return mobility_arr, self.grid

#Smart Flexible Chainlike Walker
class SFCW_model(object):
	"""docstring for FCW_Model"""
	def __init__(self, L, l, rho):
		
		self.L = L #Lattice length
		self.l = l #FCW length
		self.rho = rho #Density of FCW's

		self.N = int(round(self.rho * self.L**2 / self.l, 0)) #Number of FCW

		self.grid = np.zeros((self.L, self.L))

		self.FCWS = [] #list of lists of positions for each FCW

	def init_lattice(self):
		#Initialisation

		if self.N > self.L**2 / self.l:

			raise ValueError('Max number of FCW\'s achieved!')

		taken_pos = []

		while len(self.FCWS) < self.N:

			x_head = np.random.randint(0, self.L - 1)

			x_tail = x_head + self.l

			row = np.random.randint(0, self.L)

			positions = [[row, j % self.L] for j in range(x_head, x_tail)]

			validator = True

			#Check if any of these positions have been taken
			for pos in positions:

				if pos in taken_pos:

					validator = False

			#if any position has been taken don't do anything
			if validator == False:

				pass


			#If all the positions are free then take it
			else:

				for j in range(x_head, x_tail):

					self.grid[row][j % self.L] = 1

				FCW_i = FCW(self.l)
				FCW_i.set_pos(positions)

				taken_pos += positions

				#self.FCWS += positions
				
				self.FCWS.append(FCW_i)

	def plot_lattice(self):

		plt.imshow(self.grid, cmap=cmap)
		plt.show()
		
	def move_walkers(self):
		
		new_pos = np.zeros((self.l, 2))

		mobility = 0

		for fcw in self.FCWS:

			'''
				PROBABLY NOT PYTHON EFFICIENT
			'''
			
			#Choose 1 free nearest neighbours poisition
			i = fcw.head[0]
			j = fcw.head[1]

			lattice_pos = [((i - 1) % self.L, j), ((i + 1) % self.L, j), (i, (j - 1) % self.L), (i, (j + 1) % self.L)]

			free_pos = []

			for pos in lattice_pos:

				if self.grid[int(pos[0])][int(pos[1])] == 0:

					free_pos.append(np.array(pos))

			#Only move to not occupied positions if available
			if len(free_pos) != 0:

				move_to = choice(free_pos)

				mobility += 1

				#Update lattice for the tail
				self.grid[int(fcw.tail[0])][int(fcw.tail[1])] = 0

				#Move the other particles following the head
				for i in range(1, self.l):

					new_pos[i] = fcw.pos[i-1]

				#Move the head
				new_pos[0] = move_to

				#Update FCW position
				fcw.set_pos(new_pos)

				#Update lattice for head
				self.grid[int(fcw.head[0])][int(fcw.head[1])] = 1

		return mobility / self.N

	def animate(self, t, save_anim=False):

		self.init_lattice()

		def update(t, lines):

			self.move_walkers()

			lines.set_data(self.grid)

			return lines,

		fig, ax = plt.subplots()

		plt.title('Self assembling chains')

		lines = ax.matshow(self.grid, cmap=cmap)

		anim = FuncAnimation(fig, update, fargs=(lines, ), frames=t,
		                    blit=True, interval=0.1, repeat=False)

		if save_anim == False:

			plt.show()

		else:

			anim.save('FCW_l_%i_rho_%.2f.mp4' % (self.l, self.rho), fps=100, writer="ffmpeg")

	def simulate(self, t, folder="Data"):

		#Use for a single density simulation and store the output data in a folder

		t0 = current_time()

		data_folder = ppal_dir + '/' + folder

		if not os.path.exists(data_folder): os.mkdir(data_folder)

		self.init_lattice()

		#Write data to folder
		os.chdir(data_folder)

		np.save('init_config.npy', self.grid)

		mobility_arr = np.zeros(t)

		for k in range(t):

			print(round(k/t * 100, 2), '%', 'done')

			mobility = self.move_walkers()

			mobility_arr[k] = mobility

		ET = round(current_time() - t0, 2)

		print('\nElapsed time:', ET, 's')

		np.save('mobility.npy', mobility_arr)
		np.save('final_config.npy', self.grid)

		#Write parameters used
		f = open('parameters_used.txt', 'w')

		f.write('L: %i' % self.L)
		f.write('\nl: %i' % self.l)
		f.write('\nDensity: %i' % self.rho)

		f.write('\n\nt: %i' % t)

		f.write('\n\nE.T: %i' % ET)

		f.close()

		return mobility_arr, self.grid

#Double-Head Flexible Chainlike Walker model
class DHFCW_model(object):
	"""docstring for FCW_Model"""
	def __init__(self, L, l, rho):
		
		self.L = L #Lattice length
		self.l = l #FCW length
		self.rho = rho #Density of FCW's

		self.N = int(round(self.rho * self.L**2 / self.l, 0)) #Number of FCW

		self.grid = np.zeros((self.L, self.L))

		self.FCWS = [] #list of lists of positions for each FCW

		self.directions = [np.array([0,1]), np.array([0,-1]), np.array([1,0]), np.array([-1,0])] #Directions to choose for the FCWs

	def init_lattice(self):
		#Initialisation

		if self.N > self.L**2 / self.l:

			raise ValueError('Max number of FCW\'s achieved!')

		taken_pos = []

		while len(self.FCWS) < self.N:

			x_head = np.random.randint(0, self.L - 1)

			x_tail = x_head + self.l

			row = np.random.randint(0, self.L)

			positions = [[row, j % self.L] for j in range(x_head, x_tail)]

			validator = True

			#Check if any of these positions have been taken
			for pos in positions:

				if pos in taken_pos:

					validator = False

			#if any position has been taken don't do anything
			if validator == False:

				pass


			#If all the positions are free then take it
			else:

				for j in range(x_head, x_tail):

					self.grid[row][j % self.L] = 1

				FCW_i = FCW(self.l)
				FCW_i.set_pos(positions)

				taken_pos += positions

				#self.FCWS += positions
				
				self.FCWS.append(FCW_i)

	def plot_lattice(self):

		plt.imshow(self.grid, cmap=cmap)
		plt.show()
		
	def move_walkers(self):
		
		new_pos = np.zeros((self.l, 2))

		mobility = 0

		for fcw in self.FCWS:

			'''
				PROBABLY NOT PYTHON EFFICIENT
			'''

			#Reverse randomly head-tail
			dice = np.random.rand()

			if dice < 0.5:

				#Choose 1 nearest neighbours poisition
				direction = choice(self.directions)

				#Move the head to the chosen position
				move_to = (fcw.tail + direction) % (self.L, self.L)

				#Only move if not occupied
				if self.grid[int(move_to[0])][int(move_to[1])] != 1:

					mobility += 1

					#Update lattice for the head (new tail)
					self.grid[int(fcw.head[0])][int(fcw.head[1])] = 0

					#Move the other particles following the tail (new head)
					for i in range(self.l - 1):

						new_pos[i] = fcw.pos[i+1]

					#Move the head
					new_pos[-1] = move_to

					#Update FCW position
					fcw.set_pos(new_pos)

					#Update lattice for tail
					self.grid[int(fcw.tail[0])][int(fcw.tail[1])] = 1

				
			else:

				#Choose 1 nearest neighbours poisition
				direction = choice(self.directions)

				#Move the head to the chosen position
				move_to = (fcw.head + direction) % (self.L, self.L)

				#Only move if not occupied
				if self.grid[int(move_to[0])][int(move_to[1])] != 1:

					mobility += 1

					#Update lattice for the tail
					self.grid[int(fcw.tail[0])][int(fcw.tail[1])] = 0

					#Move the other particles following the head
					for i in range(1, self.l):

						new_pos[i] = fcw.pos[i-1]

					#Move the head
					new_pos[0] = move_to

					#Update FCW position
					fcw.set_pos(new_pos)

					#Update lattice for head
					self.grid[int(fcw.head[0])][int(fcw.head[1])] = 1

		return mobility / self.N

	def animate(self, t, save_anim=False):

		self.init_lattice()

		fig, ax = plt.subplots()

		plt.title('Self assembling chains')

		lines = ax.matshow(self.grid, cmap=cmap)

		def update(k, lines):

			self.move_walkers()

			lines.set_data(self.grid)

			#ax.set_title('Timestep: ' + str(k))

			return lines,


		anim = FuncAnimation(fig, update, fargs=(lines, ), frames=t,
		                    blit=True, interval=0.1, repeat=False)

		if save_anim == False:

			plt.show()

		else:

			anim.save('FCW_l_%i_rho_%.2f.mp4' % (self.l, self.rho), fps=100, writer="ffmpeg")

	def simulate(self, t, folder="Data"):

		#Use for a single density simulation and store the output data in a folder

		t0 = current_time()

		data_folder = ppal_dir + '/' + folder

		if not os.path.exists(data_folder): os.mkdir(data_folder)

		self.init_lattice()

		#Write data to folder
		os.chdir(data_folder)

		np.save('init_config.npy', self.grid)

		mobility_arr = np.zeros(t)

		for k in range(t):

			print(round(k/t * 100, 2), '%', 'done')

			mobility = self.move_walkers()

			mobility_arr[k] = mobility

		ET = round(current_time() - t0, 2)

		print('\nElapsed time:', ET, 's')

		np.save('mobility.npy', mobility_arr)
		np.save('final_config.npy', self.grid)

		#Write parameters used
		f = open('parameters_used.txt', 'w')

		f.write('L: %i' % self.L)
		f.write('\nl: %i' % self.l)
		f.write('\nDensity: %i' % self.rho)

		f.write('\n\nt: %i' % t)

		f.write('\n\nE.T: %i' % ET)

		f.close()

		return mobility_arr, self.grid

