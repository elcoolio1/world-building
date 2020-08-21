import arcade
from hex_functions import *
from generator_functions import *




window_size = width,height = 1000,1000

hx_scale=20
grid_thickness=1


# global origin_X
# origin_x = int(width / 2)
# global origin_y
# origin_y = int(height / 2)
# global origin
# origin = (origin_x, origin_y)
global zoom
zoom = 0.0001

px_grid_thickness = int(grid_thickness)  # thickness of lines around hex

global_display(hx_scale,0,0)





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
		super().__init__(width, height, "Map Viewer")

		# Variables that will hold sprite lists
		self.hex_list = []
		self.cursor = cursor(0, 0, 5, arcade.color.WHITE)
		self.set_mouse_visible(False)
		# self.viewport = arcade.set_viewport()
		# self.draw_map()
		global dragging
		dragging = False

		arcade.set_background_color(arcade.color.BLACK)
		


	def draw_map(self):
		# global origin_y
		# global origin_x
		# global origin
		self.hex_list = arcade.SpriteList(use_spatial_hash=False,)
		hx_radius = 24
		vp = arcade.get_viewport()
		origin_ax=round_ax(px2ax((vp[0]+width/2,vp[2]+height/2)))


		for q in range(origin_ax[0]-40,origin_ax[0]+40):
			for r in range(origin_ax[1]-40,origin_ax[1]+40):
				coord_px = ax2px((q,r))
				# vp = [origin_x-width/2,origin_x+width/2,origin_y-height/2,origin_y+height/2]
				# vp = arcade.get_viewport()

				if coord_px[0] >= vp[0]-100 and coord_px[0] <= vp[1]+100:
					if coord_px[1] >= vp[2]-100 and coord_px[1] <= vp[3]+100:
						
						# coord_px = ax2px((q,r))
		
						
						global zoom

						color = elev_color_sections(coord_px,zoom,[0.1,0.15,0.5,0.7])
						hx = hexagon('hexagon.png',(hx_scale*1.2/(100))) #25% scaling
						hx.center_x = coord_px[0]
						hx.center_y = coord_px[1]
						hx.color = color

						self.hex_list.append(hx)




	def setup(self):
		""" Set up the game and initialize the variables. """

		# Sprite lists
		# screen_origin_x = 0
		# screen_origin_y = 0
		# arcade.set_viewport(origin_x-width/2,origin_x+width/2,origin_y-height/2,origin_y+height/2)
		self.hex_list = arcade.SpriteList(use_spatial_hash=False,)
		hx_radius = 24
		vp = arcade.get_viewport()
		origin_ax=round_ax(px2ax((vp[0]+width/2,vp[2]+height/2)))


		for q in range(origin_ax[0]-40,origin_ax[0]+40):
			for r in range(origin_ax[1]-40,origin_ax[1]+40):
				coord_px = ax2px((q,r))
				# vp = [origin_x-width/2,origin_x+width/2,origin_y-height/2,origin_y+height/2]
				# vp = arcade.get_viewport()

				if coord_px[0] >= vp[2] and coord_px[0] <= vp[3]:
					if coord_px[1] >= vp[0] and coord_px[1] <= vp[1]:
						
						# coord_px = ax2px((q,r))
		
						
						global zoom

						color = elev_color_sections(coord_px,zoom,[0.1,0.15,0.5,0.7])
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

		
		

	def on_mouse_release(self, x, y, button, modifiers):
		global dragging
		dragging = False


	def on_mouse_motion(self, x, y, dx, dy):
		""" Called to update our objects. Happens approximately 60 times per second."""
		self.cursor.position_x = x
		self.cursor.position_y = y
		global dragging
		# dx_ax = ax2px(round_ax(px2ax((dx,dy))))
		if dragging:
			# vp = arcade.get_viewport()
			# new_vp = [vp[0]-dx,vp[1]-dx,vp[2]-dy,vp[3]-dy]
			vp = arcade.get_viewport()
			arcade.set_viewport(vp[0]-dx,vp[1]-dx,vp[2]-dy,vp[3]-dy)
			





			# global origin_x
			# origin_x = origin_x-dx#_ax[0]#hx_scale
			
			# global origin_y
			# origin_y = origin_y-dy#x_ax[1]#hx_scale
			
			# global origin
			# origin = origin_x,origin_y

			# rounded_origin = ax2px(round_ax(px2ax(origin)))
			# origin_x = rounded_origin[0]
			# origin_y = rounded_origin[1]

			# origin = origin_x,origin_y
			


			# print(origin)

	def on_mouse_scroll(self,x,y,scroll_x,scroll_y):
		global zoom
		zoom = zoom+scroll_y*0.0001
		print(zoom)


	def update(self, delta_time):

		
		self.hex_list.update()
		self.draw_map()


		



def main():
	""" Main method """
	window = MyGame()
	window.setup()
	arcade.run()


if __name__ == "__main__":
	main()