import arcade
from hex_functions import *
from generator_functions import *

initial_window_size = init_width,init_height = 1000,1000

window_size = width,height = init_width,init_height
global zoom
zoom=20
hx2px_scale = 20
grid_thickness=1

global noise_freq
noise_freq = 0.01

px_grid_thickness = int(grid_thickness)  # thickness of lines around hex


class hexagon(arcade.Sprite):
	def update(self):
		pass


class cursor:
	def __init__(self, position_x, position_y, radius, color):
		self.position_x = position_x
		self.position_y = position_y
		self.radius = radius
		self.color = color

	def draw(self):
		arcade.draw_circle_filled(self.position_x, self.position_y, self.radius, self.color)


class MyGame(arcade.Window):
	def __init__(self):
		super().__init__(width, height, "Map Viewer")
		global zoom
		global_display(zoom,0,0)
		global dragging
		dragging = False


		self.hex_list = []
		self.cursor = cursor(0, 0, 5, arcade.color.WHITE)
		self.set_mouse_visible(False)
		arcade.set_background_color(arcade.color.BLACK)
		
	def draw_map(self):
		self.hex_list = arcade.SpriteList(use_spatial_hash=False,)

		hx_radius = 24
		vp = arcade.get_viewport()
		# print(vp)

		origin_ax=round_ax(px2ax((vp[0]+width/2,vp[2]+height/2)))
		cover_screen = int(max(width,height)/(zoom)+5)
		edge_buffer = zoom/2

		for q in range(origin_ax[0]-cover_screen,origin_ax[0]+cover_screen):
			for r in range(origin_ax[1]-cover_screen,origin_ax[1]+cover_screen):

				coord_px = ax2px((q,r))
				if coord_px[0] >= vp[0]-edge_buffer and coord_px[0] <= vp[1]+edge_buffer:
					if coord_px[1] >= vp[2]-edge_buffer and coord_px[1] <= vp[3]+edge_buffer:

						global noise_freq
						coords=[]
						for i in range(0,2):
							coords.append(coord_px[i]/zoom)

						color = elev_color_sections(coords,noise_freq,[0.1,0.15,0.5,0.7])
						hx = hexagon('hexagon.png',(zoom*1.2/(100)))
						hx.center_x = coord_px[0]
						hx.center_y = coord_px[1]
						hx.color = color

						self.hex_list.append(hx)

	def setup(self):
		self.hex_list = arcade.SpriteList(use_spatial_hash=False,)
		global fs
		fs = False

	def on_draw(self):
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
		global zoom
		self.cursor.position_x = x*zoom
		self.cursor.position_y = y*zoom

		global dragging
		if dragging:
			vp = arcade.get_viewport()
			arcade.set_viewport(vp[0]-dx,vp[1]-dx,vp[2]-dy,vp[3]-dy)
			
	def on_mouse_scroll(self,x,y,scroll_x,scroll_y):
		global zoom
		if zoom >2:
			if zoom+scroll_y*2>2:
				zoom = zoom+scroll_y*2
		print(zoom)

	def on_key_press(self,key,modifiers):
		vp = arcade.get_viewport()
		global width
		global height
		global fs
		if key == arcade.key.ESCAPE:
			if fs:
				self.set_fullscreen(False)
				screen_size = self.get_size()
				width = screen_size[0]
				height = screen_size[1]
				arcade.set_viewport(vp[0],vp[0]+init_width,vp[2],vp[2]+init_height)
				print('Windowed')
				fs = False
			else:
				self.set_fullscreen()
				screen_size = self.get_size()
				width = screen_size[0]
				height = screen_size[1]
				arcade.set_viewport(vp[0],vp[0]+screen_size[0],vp[2],vp[2]+screen_size[1])
				print('Fullscreen')
				fs = True


	def update(self, delta_time):
		self.hex_list.update()
		self.draw_map()
		global zoom
		global_display(zoom,0,0)


def main():
	window = MyGame()
	window.setup()
	arcade.run()


if __name__ == "__main__":
	main()