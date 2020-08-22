import arcade
from hex_functions import *
from generator_functions import *

initial_window_size = init_width,init_height = 1000,1000 #size of arcade window when not full screen

window_size = width,height = init_width,init_height #dynamic window size. Changes on fullscreen
global zoom
zoom=20 #scaling factor for size of hexagons and distance apart (min 4, if it goes to close to 0 it crashes)

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

		self.hex_list = [] #will be list of hex sprites on screen
		self.cursor = cursor(0, 0, 5, arcade.color.WHITE) #mouse as white circle
		self.set_mouse_visible(False)
		arcade.set_background_color(arcade.color.BLACK)
		
	def draw_map(self):
		"""
		updates list of hex sprites
		"""
		self.hex_list = arcade.SpriteList(use_spatial_hash=False,)

		vp = arcade.get_viewport() #returns current viewport as tuple (lef,right,bottom,top)

		origin_ax=round_ax(px2ax((vp[0]+width/2,vp[2]+height/2))) #finds axial coords of hex closest to center screen
		cover_screen = int(max(width,height)/(zoom)+5) #gets dimension of parallelogram that will cover rectangular screen at minimum
		edge_buffer = zoom/2 #adds to parallelogram so hexes are rendered this far off screen. Now they can be dragged on and never show empty space

		#for each hex in parallelogram defined by cover_screen
		for q in range(origin_ax[0]-cover_screen,origin_ax[0]+cover_screen): 
			for r in range(origin_ax[1]-cover_screen,origin_ax[1]+cover_screen):

				coord_px = ax2px((q,r)) #current pixel coordinates

				#check if coordinates are within edge_buffer of viewport edge
				if coord_px[0] >= vp[0]-edge_buffer and coord_px[0] <= vp[1]+edge_buffer:
					if coord_px[1] >= vp[2]-edge_buffer and coord_px[1] <= vp[3]+edge_buffer:
						#axial distance from origin
						ax_dist=ax_distance(round_ax((q,r)),(0,0))
						#maximum map is cenerated as 120 radius hexagon
						if ax_dist<120:

							global noise_freq
							coords=[]
							for i in range(0,2):
								coords.append(coord_px[i]/zoom)

							#calles elev() in generator_functions to return center hex value of noise function
							elevation = elev(coords,noise_freq)
							#slopes elevation down towards outer edge of map
							elevation = (elevation-ax_dist/120)/2+0.5
							
							#color based on elevation
							color = elev_color_sections(elevation,[0.48,0.6,0.74,0.77,0.45])
							hx = hexagon('hexagon.png',(zoom*1.2/(100))) #create hex sprite
							hx.center_x = coord_px[0] #set sprite coordinates to current place in loop
							hx.center_y = coord_px[1]
							hx.color = color 

							self.hex_list.append(hx) #add to sprite list

	def setup(self):
		"""
		Shhhhhh this is necessary
		"""
		self.hex_list = arcade.SpriteList(use_spatial_hash=False,) #inits sprite list for hexes. It might be fine to delete this as it is also done elsewhere
		global fs
		fs = False #global status of whether program is fullscreen or not

	def on_draw(self):
		"""
		Draws map components
		"""
		arcade.start_render()
		self.hex_list.draw() #draw hex sprites
		self.cursor.draw() #draw mouse

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
		self.hex_list.update()#don't really know if this is still relevant. self.draw_map() probably does this already
		self.draw_map()
		global zoom
		global_display(zoom,0,0) #passes zoom to hex_functions.py because it can change on mouse scroll


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