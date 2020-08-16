from hex_functions import *
import pygame
import sys



screen = display_init()
p1 = (0,0)
p2 = (2,-5)
p3 = (5,-3)
p4 = (3,2)
p5 = (-2,5)
p6 = (-3,-2)
p7 = (-5,3)
p8 = (1,7)
p9 = (-7,8)
p10 = (-8,1)
p11 = (-1,-7)
p12 = (7,-8)
p13 = (-6,-4)
p14 = (6,4)
p15 = (8,-1)
p16 = (10,-6)
p17 = (4,-10)
p18 = (-10,6)
p19 = (-4,10)
screen.fill((255,255,255))
white = 255,255,255
green = 0,255,0
blue = 0,0,255
draw_cluster(p1,(random.randint(0,255),random.randint(0,255),random.randint(0,255)))
draw_cluster(p2,(random.randint(0,255),random.randint(0,255),random.randint(0,255)))
draw_cluster(p3,(random.randint(0,255),random.randint(0,255),random.randint(0,255)))
draw_cluster(p4,(random.randint(0,255),random.randint(0,255),random.randint(0,255)))
draw_cluster(p5,(random.randint(0,255),random.randint(0,255),random.randint(0,255)))
draw_cluster(p6,(random.randint(0,255),random.randint(0,255),random.randint(0,255)))
draw_cluster(p7,(random.randint(0,255),random.randint(0,255),random.randint(0,255)))
draw_cluster(p8,(random.randint(0,255),random.randint(0,255),random.randint(0,255)))
draw_cluster(p9,(random.randint(0,255),random.randint(0,255),random.randint(0,255)))
draw_cluster(p10,(random.randint(0,255),random.randint(0,255),random.randint(0,255)))
draw_cluster(p11,(random.randint(0,255),random.randint(0,255),random.randint(0,255)))
draw_cluster(p12,(random.randint(0,255),random.randint(0,255),random.randint(0,255)))
draw_cluster(p13,(random.randint(0,255),random.randint(0,255),random.randint(0,255)))
draw_cluster(p14,(random.randint(0,255),random.randint(0,255),random.randint(0,255)))
draw_cluster(p15,(random.randint(0,255),random.randint(0,255),random.randint(0,255)))
draw_cluster(p16,(random.randint(0,255),random.randint(0,255),random.randint(0,255)))
draw_cluster(p17,(random.randint(0,255),random.randint(0,255),random.randint(0,255)))
draw_cluster(p18,(random.randint(0,255),random.randint(0,255),random.randint(0,255)))
draw_cluster(p19,(random.randint(0,255),random.randint(0,255),random.randint(0,255)))

#grid
for q in range(-20,20):
	for r in range(-20,20):
		if ax_distance((q,r),(0,0)) < 12:
			loc = (q,r)
			# draw_hex_outline(loc)
			draw_coords(loc)



pygame.display.flip()


while 1:

	for event in pygame.event.get():
		if event.type == pygame.QUIT: sys.exit()





