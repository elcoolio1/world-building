import arcade
from hex_functions import *
from generator_functions import *

initial_window_size = init_width,init_height = 1000,1000 #size of arcade window when not full screen

window_size = width,height = init_width,init_height #dynamic window size. Changes on fullscreen
global zoom
zoom=4 #scaling factor for size of hexagons and distance apart (min 4, if it goes to close to 0 it crashes)

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
		map_size = 80
		rain_vol = 0.0001


		space_level = 0.3
		sea_level = 0.33
		beach_line = 0.6
		tree_line = 0.6
		snow_line = 0.65

		elevation_break_points = [sea_level,beach_line,tree_line,snow_line,space_level]

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
					color = elev_color_sections(elevation,elevation_break_points)
					hx = hexagon('hexagon.png',(zoom*1.2/(100))) #create hex sprite
					hx.center_x = coord_px[0] #set sprite coordinates to current place in loop
					hx.center_y = coord_px[1]
					hx.elevation = elevation
					hx.color = color 
					hx.water = 0.001
					hx.volume = rain_vol




					self.hex_list.append(hx) #add to sprite list
					self.hex_grid[row].append(hx)
				else:
					# self.hex_list.append([]) #add to sprite list
					self.hex_grid[row].append(None)



		#water stuff
		flow_array = []
		for row in range(len(self.hex_grid)):
			flow_array.append([])
			for column in range(len(self.hex_grid)):
				flow_array[row].append(1)

		




		for row in range(len(self.hex_grid)):
			for column in range(len(self.hex_grid)):

				this = self.hex_grid[row][column]
				if this is not None:
					if this.elevation < space_level:
						this.elevation =- 1000
					#cellular automata rules for water
					neighbours = grid_neighbours(row,column)
					n_elev = []
					n_water = []
					n_eff_elev =[]
					for n in range(0,6):
						n_row = neighbours[n][0]
						n_col = neighbours[n][1]
						if self.hex_grid[n_row][n_col] is not None:
								this_n = self.hex_grid[n_row][n_col]
								n_elev.append(this_n.elevation)
								n_water.append(this_n.water)
								n_eff_elev.append(this_n.elevation+this_n.water)
					if min(n_eff_elev) <= this.elevation+this.water:
						ind = n_eff_elev.index(min(n_eff_elev))
						this.water = this.water - (abs((this.water+this.elevation)-n_eff_elev[ind]))/2
					print(this.water)























					color  = color_grad((255,255,255),(0,0,255),this.water)
					this.color = color

		
		# flow_iterations = map_size*2
		
		# vol_array = []
		# for i in range(len(self.hex_grid)):
		# 	vol_array.append([])
		# 	for j in range(len(self.hex_grid)):
		# 		if self.hex_grid[i][j] is not None:
		# 			vol_array[i].append(0)
		# 		else:
		# 			vol_array[i].append(None)

		# for iteration in range(flow_iterations):
		# 	for row in range(len(self.hex_grid)): 
		# 		for column in range(len(self.hex_grid)):
		# 			if self.hex_grid[row][column] is not None:

		# 				q = row-map_size
		# 				r = column-map_size
		# 				ax_dist=ax_distance(round_ax((q,r)),(0,0))
		# 				if ax_dist < map_size:

		# 					adjacent = grid_neighbours(row,column)
		# 					adjacent_rows = []
		# 					adjacent_cols = []
		# 					for i in range(0,6):
		# 						# print(i)
		# 						adjacent_rows.append(adjacent[i][0])
		# 						adjacent_cols.append(adjacent[i][1])
		# 					d_elevs = []
		# 					total_d_elev = 0
		# 					for i in range(0,6):
		# 						check_row = adjacent_rows[i]
		# 						check_col = adjacent_cols[i]
								
		# 						if check_row >= 0 and check_row <= len(self.hex_grid):
		# 							if check_col >= 0 and check_col <= len(self.hex_grid):
		# 								if self.hex_grid[row][column].elevation < space_level:
		# 									self.hex_grid[row][column].elevation = self.hex_grid[row][column].elevation - 1000
		# 								if self.hex_grid[check_row][check_col] is not None:

		# 									to_append = (self.hex_grid[row][column].elevation + self.hex_grid[row][column].volume) - (self.hex_grid[check_row][check_col].elevation )
		# 									d_elevs.append(to_append)
		# 									# print('delta',to_append)
		# 									if to_append > 0:
		# 										total_d_elev = total_d_elev + to_append
		# 								else:
		# 									d_elevs.append(-1)
		# 							else:
		# 								d_elevs.append(-1)
		# 						else:
		# 							d_elevs.append(-1)
		# 					for i in range(0,6):
		# 						check_row = adjacent_rows[i]
		# 						check_col = adjacent_cols[i]
		# 						if d_elevs[i] > 0:

		# 							flow_amount = d_elevs[i]/total_d_elev * self.hex_grid[row][column].volume
		# 							# print(d_elevs[i]/total_d_elev)
		# 							vol_array[check_row][check_col] = vol_array[check_row][check_col] + flow_amount
		# 							vol_array[row][column] = vol_array[row][column] - flow_amount

		# 							self.hex_grid[check_row][check_col].flow_through = self.hex_grid[check_row][check_col].flow_through + flow_amount

		# 					# vol_array[row][column] = vol_array[row][column] - self.hex_grid[row][column].volume
							



		# 	for row in range(len(vol_array)): 
		# 		for column in range(len(vol_array)):
		# 			if self.hex_grid[row][column] is not None:
		# 				# print(vol_array[row][column])
		# 				self.hex_grid[row][column].volume = vol_array[row][column]

		# 	for i in range(len(vol_array)):
		# 		for j in range(len(vol_array)):
		# 			if self.hex_grid[i][j] is not None:
		# 				vol_array[i][j] = vol_array[i][j] +rain_vol




		# #color water
		# flow_val_list = []
		# vol_val_list = []
		# for row in range(len(self.hex_grid)): 
		# 	for column in range(len(self.hex_grid[row])):
		# 		if self.hex_grid[row][column] is not None : #and self.hex_grid[row][column].elevation > space_level and self.hex_grid[row][column].flow_through > 0.3:
		# 			print(self.hex_grid[row][column].flow_through)
		# 			flow_val_list.append(self.hex_grid[row][column].flow_through)
		# 			vol_val_list.append(self.hex_grid[row][column].volume)
		# 			self.hex_grid[row][column].color = color_grad((255,255,255),(0,0,255),self.hex_grid[row][column].flow_through/12)

		# print('Max flow',max(flow_val_list))
		# print('Max volume',max(vol_val_list))
						


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
		old_zoom = zoom
		#stops zoom from going below 3 (4 in practicality because it moves in units of 2 [scroll_y*2])
		if zoom >2:
			if zoom+scroll_y*2>2:
				zoom = zoom+scroll_y*2
				for i in range(len(self.hex_list)):
					self.hex_list[i].center_x = self.hex_list[i].center_x*zoom/old_zoom
					self.hex_list[i].center_y = self.hex_list[i].center_y*zoom/old_zoom
					self.hex_list[i].scale = zoom*1.2/(100)
		print(zoom)
		global_display(zoom,0,0)

		# self.create_map()

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