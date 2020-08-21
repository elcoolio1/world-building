import arcade
from hex_functions import *
from generator_functions import *


hx_scale=20
grid_thickness=1
# hx_width = 66
# hx_height = 66
px_size = width, height = 50*hx_scale, 50*hx_scale

global origin_X
origin_x = int(width / 2)
global origin_y
origin_y = int(height / 2)
global origin
origin = (origin_x, origin_y)

px_grid_thickness = int(grid_thickness)  # thickness of lines around hex




global_display(hx_scale,origin_x,origin_y)





class hexagon(arcade.Sprite):

	def update(self):
		pass


class cursor:
	def __init__(self, position_x, position_y, radius, color):

		# Take the parameters of the init function above, and create instance variables out of them.
		self.position_x = position_x
		self.position_y = position_y
		self.radius = radius
		self.color = color

	def draw(self):
		""" Draw the cursors with the instance variables we have. """
		arcade.draw_circle_filled(self.position_x, self.position_y, self.radius, self.color)

	


class MyGame(arcade.Window):
	
	def __init__(self):
		""" Initializer """
		# Call the parent class initializer
		super().__init__(width, height, "Fucking Work")



		# Variables that will hold sprite lists
		self.hex_list = []
		self.cursor = cursor(origin_x, origin_y, 2, arcade.color.WHITE)
		self.set_mouse_visible(False)
		self.draw_map()
		global dragging
		dragging = False

		arcade.set_background_color(arcade.color.BLACK)
		


	def draw_map(self):

		self.new_list = arcade.SpriteList(use_spatial_hash=False,is_static=True)
		for i in range(len(self.hex_list)):
			sprite = self.hex_list[i]
			coord_px = sprite._get_position()

		# for q in range(-30,30):
		# 	for r in range(-30,30):
		# 		if ax_distance((q, r), (0,0)) < hx_radius:
					
		# 			coord_px = ax2px((q,r))

			elevation_xy=[]
			for i in range(0,2):
				elevation_xy.append(coord_px[i]+origin[i])

			color = elev_color_sections(elevation_xy,.01,[0.1,0.15,0.5,0.7])
			hx = hexagon('hexagon.png',(hx_scale*1.2/(100))) #25% scaling
			hx.center_x = coord_px[0]
			hx.center_y = coord_px[1]
			hx.color = color 

			self.new_list.append(hx)
		self.hex_list = arcade.SpriteList(use_spatial_hash=False,is_static=True)
		self.hex_list = self.new_list



	def setup(self):
		""" Set up the game and initialize the variables. """

		# Sprite lists
		self.hex_list = arcade.SpriteList(use_spatial_hash=False,is_static=True)
		hx_radius = 24
		for q in range(-30,30):
			for r in range(-30,30):
				if ax_distance((q, r), (0,0)) < hx_radius:
					
					coord_px = ax2px((q,r))
	
					elevation_xy=[]
					for i in range(0,2):
						elevation_xy.append(coord_px[i]+origin[i])

					color = elev_color_sections(elevation_xy,.01,[0.1,0.15,0.5,0.7])
					hx = hexagon('hexagon.png',(hx_scale*1.2/(100))) #25% scaling
					hx.center_x = coord_px[0]
					hx.center_y = coord_px[1]
					hx.color = color

					self.hex_list.append(hx)


	def on_draw(self):
		""" Draw everything """
		# arcade.set_background_color(arcade.color.BLACK)
		arcade.start_render()
		self.hex_list.draw()
		
		self.cursor.draw()

	def on_mouse_press(self, x, y, button, modifiers):
		global dragging
		dragging = True

		self.draw_map()
		

	def on_mouse_release(self, x, y, button, modifiers):
		global dragging
		dragging = False


	def on_mouse_motion(self, x, y, dx, dy):
		""" Called to update our objects. Happens approximately 60 times per second."""
		self.cursor.position_x = x
		self.cursor.position_y = y
		global dragging
		if dragging:
			global origin_x
			origin_x = origin_x-dx#hx_scale
			global origin_y
			origin_y = origin_y-dy#hx_scale
			global origin
			origin = origin_x,origin_y


			# print(origin)




	def update(self, delta_time):
		
		self.hex_list.update()

		



def main():
	""" Main method """
	window = MyGame()
	window.setup()
	arcade.run()


if __name__ == "__main__":
	main()