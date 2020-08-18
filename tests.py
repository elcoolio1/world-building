from hex_functions import *
import sys
from generator_functions import *
import arcade



scale = 20  # size of hexes
size = (66, 66)  # number of hexes

# cluster_points = [(0, 0), (2, -5), (5, -3), (3, 2), (-2, 5), (-3, -2), (-5, 3), (1, 7), (-7, 8),
#                   (-8, 1), (-1, -7), (7, -8), (-6, -4), (6, 4), (8, -1), (10, -6), (4, -10), (-10, 6), (-4, 10)]


display_init(scale, size)
arcade.start_render()

for q in range(-60, 60):
    for r in range(-60, 60):
        if ax_distance((q, r), (0, 0)) < 30:
            loc = (q, r)
            color = elev_color_sections(loc)
            draw_hex(loc, color)
            # elevs.append(elev(loc))
            # draw_hex_outline(loc, (150, 150, 150))


# loc = px2ax((-30,30))

# dark_blue = 5,18,64
# light_blue = 45, 199, 255

# shore = 234, 210, 172
# beach = 234, 186, 107

# undergrowth= 23, 195, 103
# evergreen  = 22, 67, 35

# light_rock = 103, 98, 92
# dark_rock = 170, 167, 161

# off_white = 240, 244, 246
# pure_white = 255,255,255


# color = color_grad(light_blue,dark_blue,0)
# draw_hex(loc, color)
# loc = loc[0]+1,loc[1]
# color = color_grad(light_blue,dark_blue,1)
# draw_hex(loc, color)
# loc = loc[0]+1,loc[1]



# color = color_grad(beach,shore,0)
# draw_hex(loc, color)
# loc = loc[0]+1,loc[1]
# color = color_grad(beach,shore,1)
# draw_hex(loc, color)
# loc = loc[0]+1,loc[1]

# color = color_grad(undergrowth,evergreen,0)
# draw_hex(loc, color)
# loc = loc[0]+1,loc[1]
# color = color_grad(undergrowth,evergreen,1)
# draw_hex(loc, color)
# loc = loc[0]+1,loc[1]

# color = color_grad(light_rock,dark_rock,0)
# draw_hex(loc, color)
# loc = loc[0]+1,loc[1]
# color = color_grad(light_rock,dark_rock,1)
# draw_hex(loc, color)
# loc = loc[0]+1,loc[1]

# color = color_grad(off_white,pure_white,0)
# draw_hex(loc, color)
# loc = loc[0]+1,loc[1]
# color = color_grad(off_white,pure_white,1)
# draw_hex(loc, color)
# loc = loc[0]+1,loc[1]



arcade.finish_render()
arcade.run()

print(max(elevs))
print(min(elevs))