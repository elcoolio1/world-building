from hex_functions import *
import arcade


display_init()


arcade.start_render()

loc = 0, 0
draw_hex(loc)
draw_coords(loc)
draw_center(loc)

arcade.finish_render()

arcade.run()
