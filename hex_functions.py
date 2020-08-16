
from typing import List, Set, Dict, Tuple, Optional
import math
import pygame
pygame.init()


def hx2ax(hx: Tuple[int, int, int]):
	#converts hex xyz coordinates to axial qr coordinates
	x = hx[0]
	y = hx[1]
	z = hx[2]

	#hx = axial with extra redundant coordinate
	q = x
	r = y
	axial = (q,r)
	return axial


def ax2hx(axial: Tuple[int, int]):
	#converts axial qr coordinates to hex xyz coordinates
	q = axial[0]
	r = axial[1]
	#hex = axial with extra redundant coordinate
	#sum of coordinates must be 0. ie x+y+z = 0
	x = q
	y = r
	#solve x+y+z = 0 for 'z'
	z = -(x+y)
	hx = (x,y,z)
	return hx

def ax2px(axial: Tuple[int, int]) -> Tuple[int, int]:
	#converts axial qr coordinates to pixel xy coordinates
	q = axial[0]
	r = axial[1]
	#use triangle to break down into vector movement from 1 r and 1 q.
	#special 30-60-90 triangle gives sqrt(3)/2 x in the positive direction for every 1 q. 
	#x = x1, x1 = sqrt(3)/2*q
	x = q*math.sqrt(3)/2

	#same special triangle gives -1/2 y for every 1 q. 1r directly results in 1y
	#y = y1 + y2, y1 = r, y2 = -1/2*q
	y = -(r+q/2)
	pixel = (x,y)
	return pixel

def px2ax(pixel: Tuple[int, int]):
	#converts pixel xy coordinates to axial qr coordinates
	x = pixel[0]
	y = pixel[1]
	#solve equations in ax2bx for q and r
	q = x*2/math.sqrt(3)
	r = -y-q/2
	axial = (q,r)
	return axial

def hx2px(hx: Tuple[int, int, int]):
	#converts hex xyz coordinates to pixel xy coordinates
	x = hx[0]
	y = hx[1]
	z = hx[2]

	#hex = axial with extra redundant coordinate
	#convert to axial, then call ax2px
	axial = hx2ax((x,y,z))
	pixel = ax2px(axial)
	return pixel


def px2hx(pixel: Tuple[int, int]):
	#converts pixel xy coordinates to hex xyz coordinates
	x = pixel[0]
	y = pixel[1]

	#hx = axial with extra redundant coordinate
	#call px2ax then convert to hex
	axial = px2ax((x,y))
	hx = ax2hx(axial)
	return hx


def hx_dist(start: Tuple[int, int, int], stop: Tuple[int, int, int]):
	#calculates distance between 2 xyz hex points
	dx = abs(stop[0]-start[0])
	dy = abs(stop[1]-start[1])
	dz = abs(stop[2]-start[2])

	#x+y+z=0 is always true for hex coordinates
	#the largest translation will equal and opposite to the sum of the other 2, but we don't care about sign for absolute distance
	#translation is on any 2 axis so largest counts same as other 2
	distance = max(dx,dy,dz)
	return distance

def ax_distance(start: Tuple[int, int], stop: Tuple[int, int]):
	#calculates distance between 2 qr axial points
	#converts to hex for calculation
	hx_start = ax2hx(start)
	hx_stop = ax2hx(stop)
	hx_distance = hx_dist(hx_start,hx_stop)
	ax_distance = hx_distance
	return ax_distance


def round_hx(hx: Tuple[int, int, int]):
	#rounds hex coordinates to nearest whole integer coordinate
	x = hx[0]
	y = hx[1]
	z = hx[2]

	round_x = round(x)
	round_y = round(y)
	round_z = round(z)

	#hex coordinates must always satisfy x+y+z=0
	#discard largest rounding and calculate from other coordinates
	dx = abs(x-round_x)
	dy = abs(y-round_y)
	dz = abs(z-round_z)
	diffs = [dx,dy,dz]
	# print('diffs',diffs)
	if max(diffs) == dx:
		round_x = -(round_y+round_z)
	elif  max(diffs) == dy:
		round_y = -(round_x+round_z)
	else:
		round_z = -(round_x+round_y)

	rounded_hx = (round_x,round_y,round_z)
	# print('raw',hx)
	# print('rounded',rounded_hx)
	return rounded_hx


def round_ax(axial: Tuple[int, int]):
	#convert to hex then round to take advantage of always discarding worst rounding amount
	hx = ax2hx(axial)
	rounded_hx = round_hx(hx)
	rounded_ax = hx2ax(rounded_hx)
	return rounded_ax


def scale_output(point: Tuple[int, int], scale, origin: Tuple[int, int]):
	x = point[0]*scale+origin[0]
	y = point[1]*scale+origin[1]
	scaled_coords = (int(x),int(y))
	return scaled_coords


def hex_on_center(center: Tuple[int, int]):
	x = center[0]
	y = center[1]

	x1 = x - 1/(2*math.sqrt(3))
	y1 = y + 0.5
	x2 = x + 1/(2*math.sqrt(3))
	y2 = y + 0.5
	x3 = x + 1/math.sqrt(3)
	y3 = y
	x4 = x + 1/(2*math.sqrt(3))
	y4 = y - 0.5
	x5 = x - 1/(2*math.sqrt(3))
	y5 = y - 0.5
	x6 = x - 1/math.sqrt(3)
	y6 = y

	xy_points = [
		(x1,y1),
		(x2,y2),
		(x3,y3),
		(x4,y4),
		(x5,y5),
		(x6,y6)]
	return xy_points

def display_init(hx_scale=50, hx_size=(20,20), grid_thickness = 0.1):

	hx_width = hx_size[0]
	hx_height = hx_size[1]
	px_size = width, height = (hx_width+2)*hx_scale, (hx_height+2)*hx_scale

	center_x = int(width/2)
	center_y = int(height/2)
	origin = (center_x,center_y)

	global screen
	screen = pygame.display.set_mode(px_size)
	global textscreen
	textscreen = pygame.display.set_mode(px_size)
	global px_origin
	px_origin = origin
	global scale
	scale = hx_scale
	global px_grid_thickness
	px_grid_thickness = int(grid_thickness)
	global opensans_reg
	opensans_reg = pygame.font.Font('OpenSans-Regular.ttf', 8) 
	global opensans_bold
	opensans_bold = pygame.font.Font('OpenSans-SemiBold.ttf', 12) 

	screen.fill((0,0,0))
	pygame.display.set_caption('Hexmapper')

	return screen


def draw_hex(center,color=(255,255,255)):

	points = hex_on_center(ax2px(center))
	shape = []
	for i in range(len(points)):
		shape.append(
			scale_output(
				points[i],
				scale,
				px_origin
			)
		)

	pygame.draw.polygon(screen, color, shape)

def draw_hex_outline(center,color=(0,0,0)):

	points = hex_on_center(ax2px(center))
	shape = []
	for i in range(len(points)):
		shape.append(
			scale_output(
				points[i],
				scale,
				px_origin
			)
		)

	pygame.draw.aalines(screen, color, True, shape, px_grid_thickness)

def draw_center(center, color=(255,0,0), size=2):
	location = scale_output(
		ax2px(center), 
		scale, 
		px_origin
	)
	pygame.draw.circle(screen,color,location,int(size))

def draw_coords(center,color = (0,0,128)):
	string_to_print = str(
		round_hx(
			ax2hx(
				center
			)
		)
	)
	text = opensans_reg.render(string_to_print, True, color)
	textRect = text.get_rect()

	position = scale_output(ax2px(center), scale, px_origin)

	textRect.center = (position[0],position[1]+10)
	textscreen.blit(text, textRect)
	pygame.display.update() 


def draw_line(start,stop,color = (100,100,100)):
	dist_hx = ax_distance(start,stop)
	start_px = ax2px(start)
	stop_px = ax2px(stop)
	dot_color = 175,175,175

	pygame.draw.aaline(
		screen, 
		color, 
		scale_output(start_px,	scale, px_origin),
		scale_output(stop_px, scale, px_origin), 
		2)
	dx = (stop_px[0]-start_px[0])/dist_hx
	dy = (stop_px[1]-start_px[1])/dist_hx
	draw_x = start_px[0]
	draw_y = start_px[1]

	for i in range(dist_hx+1):
		draw = (draw_x,draw_y)

		through_hex = round_hx(px2hx(draw))
		# print('pix:',draw)
		# print('hex:',px2hx(draw))
		# print('rou:',round_hx(px2hx(draw)))

		draw_hex(hx2ax(through_hex),(50,50,50))

		draw_coords(through_hex)

		
		pygame.draw.circle(screen,dot_color,scale_output(draw,scale, px_origin),5)
		draw_x = draw_x + dx
		draw_y = draw_y + dy




def fill_primary_hex():
	draw_secondary_hex()

