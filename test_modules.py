from hex_functions import *
import arcade

"""
Sanity check for all the draw functions. Should see:

- White hex center screen with red center point and coordinates (0,0,0)

- diagonal line of grey hexes bottom left. Straight line drawn over them with evenly spaced circles equal to the number of grey hexes

- Cluster of red hexes center right. Should have white dot at center and black outlines

"""

p0 = 0, 0
p1 = 5, -3
p3 = -2, 4
p4 = -4, 8

display_init()
arcade.start_render()


# functions tested
draw_hex(p0)
draw_coords(p0)
draw_center(p0)

draw_line(p3, p4)
draw_cluster(p1)

draw_cluster_center(p1)


arcade.finish_render()
arcade.run()
