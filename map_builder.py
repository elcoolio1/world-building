import arcade
from hex_functions import *
from generator_functions import *

initial_window_size = init_width,init_height = 1000,1000 #size of arcade window when not full screen

window_size = width,height = init_width,init_height #dynamic window size. Changes on fullscreen
global zoom
zoom=12 #scaling factor for size of hexagons and distance apart (min 4, if it goes to close to 0 it crashes)

global noise_freq
noise_freq = 0.03 #determines scale of largest bumps in elevation map


class hexagon(arcade.Sprite):
	"""
	Only a class so we can instance many hex's as sprites to draw fast
	"""
	def update(self):
		pass


class cursor:
	"""
	Circle that marks mouse over window. 
	Currently kinda fucked and disappears if you go too far
	"""
	def __init__(self, position_x, position_y, radius, color):
		self.position_x = position_x
		self.position_y = position_y
		self.radius = radius
		self.color = color

	def draw(self):
		arcade.draw_circle_filled(self.position_x, self.position_y, self.radius, self.color)


class map_gen(arcade.Window):
	"""
	Main class for running the map
	"""
	def __init__(self):
		super().__init__(width, height, "Map Viewer") #calls init for parent class (arcade.window)
		global zoom
		global_display(zoom,0,0) #workaround to pass scaling factor to hex_functions.py
		global dragging
		dragging = False #inits vairable that marks if mouse button is depressed

		# self.hex_list = [] #will be list of hex sprites on screen
		self.cursor = cursor(0, 0, 5, arcade.color.WHITE) #mouse as white circle
		# self.set_mouse_visible(False)
		arcade.set_background_color(arcade.color.BLACK)
		
	def create_map(self):
		"""
		updates list of hex sprites
		"""
		self.hex_list = arcade.SpriteList()#use_spatial_hash=False,
		self.hex_grid = []
				

		vp = arcade.get_viewport() #returns current viewport as tuple (lef,right,bottom,top)

		origin_ax=round_ax(px2ax((vp[0]+width/2,vp[2]+height/2))) #finds axial coords of hex closest to center screen
		cover_screen = int(max(width,height)/(zoom)+5) #gets dimension of parallelogram that will cover rectangular screen at minimum
		edge_buffer = zoom/2 #adds to parallelogram so hexes are rendered this far off screen. Now they can be dragged on and never show empty space

		#for each hex in parallelogram defined by cover_screen
		map_size = 40
		for row in range(0,2*map_size+1): 
			self.hex_grid.append([])
			for column in range(0,2*map_size+1):
				q = row-map_size
				r = column-map_size
				coord_px = ax2px((q,r)) #current pixel coordinates

				#check if coordinates are within edge_buffer of viewport edge
				# if coord_px[0] >= vp[0]-edge_buffer and coord_px[0] <= vp[1]+edge_buffer:
				# 	if coord_px[1] >= vp[2]-edge_buffer and coord_px[1] <= vp[3]+edge_buffer:
						#axial distance from origin
				ax_dist=ax_distance(round_ax((q,r)),(0,0))
				#maximum map is cenerated as radius hexagon
				if ax_dist<map_size:

					global noise_freq
					coords=[]
					for i in range(0,2):
						coords.append(coord_px[i]/zoom)

					#calles elev() in generator_functions to return center hex value of noise function
					elevation = elev(coords,noise_freq)
					#slopes elevation down towards outer edge of map
					px_dist = px_distance(coord_px, (0,0))
					elevation = (elevation-px_dist/(map_size*zoom))/2+0.5
					# print(px_dist)
					
					#color based on elevation
					color = elev_color_sections(elevation,[0.48,0.6,0.74,0.77,0.45])
					hx = hexagon('hexagon.png',(zoom*1.2/(100))) #create hex sprite
					hx.center_x = coord_px[0] #set sprite coordinates to current place in loop
					hx.center_y = coord_px[1]
					hx.elevation = elevation
					hx.color = color 
					hx.flow = 0
					hx.flow_cut = 0


					self.hex_list.append(hx) #add to sprite list
					self.hex_grid[row].append(hx)
				else:
					# self.hex_list.append([]) #add to sprite list
					self.hex_grid[row].append(None)

		# calc water flow direction
		flow_iterations = 10
		flow_array = []
		for i in range(len(self.hex_grid)):
			flow_array.append([])
			for j in range(len(self.hex_grid)):
				if self.hex_grid[i][j] is not None:
					flow_array[i].append(1)
				else:
					flow_array[i].append(None)

		for iteration in range(flow_iterations):
			for row in range(len(self.hex_grid)): 
				for column in range(len(self.hex_grid)):
					if self.hex_grid[row][column] is not None:

						q = row-map_size
						r = column-map_size
						ax_dist=ax_distance(round_ax((q,r)),(0,0))
						if ax_dist < map_size:

							adjacent = grid_neighbours(row,column)
							adjacent_rows = []
							adjacent_cols = []
							for i in range(0,6):
								# print(i)
								adjacent_rows.append(adjacent[i][0])
								adjacent_cols.append(adjacent[i][1])
							d_elevs = []
							total_d_elev = 0
							for i in range(0,6):
								check_row = adjacent_rows[i]
								check_col = adjacent_cols[i]
								
								if check_row >= 0 and check_row <= len(self.hex_grid):
									if check_col >= 0 and check_col <= len(self.hex_grid):
										if self.hex_grid[check_row][check_col] is not None:

											to_append = self.hex_grid[row][column].elevation - self.hex_grid[check_row][check_col].elevation
											d_elevs.append(to_append)
											# print('delta',to_append)
											if to_append>0:
												total_d_elev = total_d_elev + to_append
										else:
											d_elevs.append(-1)
									else:
										d_elevs.append(-1)
								else:
									d_elevs.append(-1)
							for i in range(0,6):
								check_row = adjacent_rows[i]
								check_col = adjacent_cols[i]
								if d_elevs[i] > 0:
									# print('before',flow_array[check_row][check_col])
									flow_array[check_row][check_col] = flow_array[check_row][check_col] + d_elevs[i]/total_d_elev * self.hex_grid[row][column].flow
									# print(total_d_elev)
									# print('after',flow_array[check_row][check_col])
			
			


			for row in range(len(flow_array)): 
				for column in range(len(flow_array)):
					if self.hex_grid[row][column] is not None:
						# print(flow_array[row][column])
						self.hex_grid[row][column].flow = flow_array[row][column]
			for i in range(len(flow_array)):
				for j in range(len(flow_array)):
					if self.hex_grid[i][j] is not None:
						flow_array[i][j] = flow_array[i][j] + 1




		#color water
		for row in range(len(self.hex_grid)): 
			for column in range(len(self.hex_grid[row])):
				if self.hex_grid[row][column] is not None:
					print(self.hex_grid[row][column].flow/100)
					self.hex_grid[row][column].color = color_grad((255,255,255),(0,0,255),self.hex_grid[row][column].flow/10000)
		#color elevation
		# for row in range(len(self.hex_grid)): 
		# 	for column in range(len(self.hex_grid[row])):
		# 		if self.hex_grid[row][column] is not None:
		# 			print(math.log(self.hex_grid[row][column].flow))
		# 			self.hex_grid[row][column].color = color_grad((0,0,0),(255,255,255),self.hex_grid[row][column].elevation)


						


	def setup(self):
		"""
		Shhhhhh this is necessary
		"""
		self.hex_list = arcade.SpriteList() #inits sprite list for hexes. It might be fine to delete this as it is also done elsewhere
		global fs
		self.create_map()
		fs = False #global status of whether program is fullscreen or not

	def on_draw(self):
		"""
		Draws map components
		"""
		arcade.start_render()
		# for i in range(len(self.hex_list)):

		self.hex_list.draw() #draw hex sprites
		# self.cursor.draw() #draw mouse

	def on_mouse_press(self, x, y, button, modifiers):
		"""
		you know what this means
		"""
		global dragging
		dragging = True

	def on_mouse_release(self, x, y, button, modifiers):
		"""
		you know what this means
		"""
		global dragging
		dragging = False

	def on_mouse_motion(self, x, y, dx, dy):
		"""
		you know what this means
		"""
		global zoom
		self.cursor.position_x = x*zoom
		self.cursor.position_y = y*zoom

		global dragging
		if dragging:
			#Moves viewport with mouse while mouse button is down
			vp = arcade.get_viewport()
			arcade.set_viewport(vp[0]-dx,vp[1]-dx,vp[2]-dy,vp[3]-dy)
			
	def on_mouse_scroll(self,x,y,scroll_x,scroll_y):
		"""
		you know what this means
		"""
		global zoom
		#stops zoom from going below 3 (4 in practicality because it moves in units of 2 [scroll_y*2])
		if zoom >2:
			if zoom+scroll_y*2>2:
				zoom = zoom+scroll_y*2
		print(zoom)
		global_display(zoom,0,0)
		self.create_map()

	def on_key_press(self,key,modifiers):
		"""
		you know what this means
		"""
		vp = arcade.get_viewport()
		global width
		global height
		global fs

		#escape key toggles fullscreen
		if key == arcade.key.ESCAPE:
			if fs: #go to windows if in fullscreen
				self.set_fullscreen(False)
				screen_size = self.get_size()
				width = screen_size[0]
				height = screen_size[1]
				arcade.set_viewport(vp[0],vp[0]+init_width,vp[2],vp[2]+init_height) #scales viewport from bottom left to monitor size
				print('Windowed')
				fs = False
			else:
				self.set_fullscreen()
				screen_size = self.get_size()
				width = screen_size[0]
				height = screen_size[1]
				arcade.set_viewport(vp[0],vp[0]+screen_size[0],vp[2],vp[2]+screen_size[1])#scales viewport from bottom left to original window size
				print('Fullscreen')
				fs = True

	def update(self, delta_time):
		"""
		Called as fast as possible
		"""
		# self.hex_list.update()#don't really know if this is still relevant. self.create_map() probably does this already
		# self.create_map()
		# global zoom
		 #passes zoom to hex_functions.py because it can change on mouse scroll


def main():
	"""
	just part of startup. the point is to call map_gen()
	"""
	window = map_gen()
	window.setup()
	arcade.run()


if __name__ == "__main__":
	#game loop starts here
	main()