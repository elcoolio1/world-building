
from typing import List, Set, Dict, Tuple, Optional
import math
import random
import arcade


def hx2ax(hx: Tuple[int, int, int]):
	# converts hex xyz coordinates to axial qr coordinates
	x = hx[0]
	y = hx[1]
	z = hx[2]

	# hx = axial with extra redundant coordinate
	q = x
	r = y
	axial = (q, r)
	return axial


def ax2hx(axial: Tuple[int, int]):
	# converts axial qr coordinates to hex xyz coordinates
	q = axial[0]
	r = axial[1]
	# hex = axial with extra redundant coordinate
	# sum of coordinates must be 0. ie x+y+z = 0
	x = q
	y = r
	# solve x+y+z = 0 for 'z'
	z = -(x + y)
	hx = (x, y, z)
	return hx

def global_display(size,x,y):
	global scale
	scale = size
	global origin_x
	origin_x = x
	global origin_y
	origin_y = y
	global origin
	origin = 0,0

def ax2px(axial: Tuple[int, int]) -> Tuple[int, int]:
	# converts axial qr coordinates to pixel xy coordinates
	
	q = axial[0]
	r = axial[1]
	# use triangle to break down into vector movement from 1 r and 1 q.
	# special 30-60-90 triangle gives sqrt(3)/2 x in the positive direction for every 1 q.
	#x = x1, x1 = sqrt(3)/2*q
	x = q * math.sqrt(3) / 2

	# same special triangle gives -1/2 y for every 1 q. 1r directly results in 1y
	# y = y1 + y2, y1 = r, y2 = -1/2*q
	y = -(r + q / 2)
	pixel = (x*scale+origin_x, y*scale+origin_y)
	return pixel


def px2ax(pixel: Tuple[int, int]):
	# converts pixel xy coordinates to axial qr coordinates
	x = (pixel[0]-origin_x)/scale
	y = (pixel[1]-origin_y)/scale
	# solve equations in ax2px for q and r
	q = x * 2 / math.sqrt(3)
	r = -y - q / 2
	axial = (q, r)
	return axial


def hx2px(hx: Tuple[int, int, int]):
	# converts hex xyz coordinates to pixel xy coordinates
	x = hx[0]
	y = hx[1]
	z = hx[2]

	# hex = axial with extra redundant coordinate
	# convert to axial, then call ax2px
	axial = hx2ax((x, y, z))
	pixel = ax2px(axial)
	return pixel


def px2hx(pixel: Tuple[int, int]):
	# converts pixel xy coordinates to hex xyz coordinates
	x = pixel[0]
	y = pixel[1]

	# hx = axial with extra redundant coordinate
	# call px2ax then convert to hex
	axial = px2ax((x, y))
	hx = ax2hx(axial)
	return hx


def hx_dist(start: Tuple[int, int, int], stop: Tuple[int, int, int]):
	# calculates distance between 2 xyz hex points
	dx = abs(stop[0] - start[0])
	dy = abs(stop[1] - start[1])
	dz = abs(stop[2] - start[2])

	# x+y+z=0 is always true for hex coordinates
	# the largest translation will equal and opposite to the sum of the other 2, but we don't care about sign for absolute distance
	# translation is on any 2 axis so largest counts same as other 2
	distance = max(dx, dy, dz)
	return distance


def ax_distance(start: Tuple[int, int], stop: Tuple[int, int]):
	# calculates distance between 2 qr axial points
	# converts to hex for calculation
	hx_start = ax2hx(start)
	hx_stop = ax2hx(stop)
	hx_distance = hx_dist(hx_start, hx_stop)
	ax_distance = hx_distance
	return ax_distance


def round_hx(hx: Tuple[int, int, int]):
	# rounds hex coordinates to nearest whole integer coordinate
	x = hx[0]
	y = hx[1]
	z = hx[2]

	round_x = round(x)
	round_y = round(y)
	round_z = round(z)

	# hex coordinates must always satisfy x+y+z=0
	# discard largest rounding and calculate from other coordinates
	dx = abs(x - round_x)
	dy = abs(y - round_y)
	dz = abs(z - round_z)
	diffs = [dx, dy, dz]
	# print('diffs',diffs)
	if max(diffs) == dx:
		round_x = -(round_y + round_z)
	elif max(diffs) == dy:
		round_y = -(round_x + round_z)
	else:
		round_z = -(round_x + round_y)

	rounded_hx = (round_x, round_y, round_z)
	# print('raw',hx)
	# print('rounded',rounded_hx)
	return rounded_hx


def round_ax(axial: Tuple[int, int]):
	# convert to hex then round to take advantage of always discarding worst rounding amount
	hx = ax2hx(axial)
	rounded_hx = round_hx(hx)
	rounded_ax = hx2ax(rounded_hx)
	return rounded_ax


def scale_output(point: Tuple[int, int], scale, origin: Tuple[int, int]):
	# Used to prepare px coordinates for drawing. Scales up by factor (default is set in display_init() below)
	# adds half screen size to place origin at 0,0

	# I think in the future we can get rid of this and do it at the level of axial to pixel conversion. I just didn't want to mess that up yet
	# update: NOT WORTH MOVING. EVERYTHING BROKE. SPEND HOURS. REVERTED COMMIT
	x = point[0] * scale + origin[0]
	y = point[1] * scale + origin[1]
	scaled_coords = (int(x), int(y))
	return scaled_coords


def hex_on_center(center: Tuple[int, int]):
	# returns list of xy tuples defining (flat topped) hexagon points around input point

	x = center[0]
	y = center[1]

	x1 = x - 1 / (2 * math.sqrt(3))
	y1 = y + 0.5
	x2 = x + 1 / (2 * math.sqrt(3))
	y2 = y + 0.5
	x3 = x + 1 / math.sqrt(3)
	y3 = y
	x4 = x + 1 / (2 * math.sqrt(3))
	y4 = y - 0.5
	x5 = x - 1 / (2 * math.sqrt(3))
	y5 = y - 0.5
	x6 = x - 1 / math.sqrt(3)
	y6 = y

	xy_points = [
		(x1, y1),
		(x2, y2),
		(x3, y3),
		(x4, y4),
		(x5, y5),
		(x6, y6)]
	return xy_points


def display_init(hx_scale=50, hx_size=(20, 20), grid_thickness=1):
	# call at start of script to set up pygames display

	hx_width = hx_size[0]
	hx_height = hx_size[1]
	px_size = width, height = (hx_width + 2) * \
		hx_scale, (hx_height + 2) * hx_scale

	center_x = int(width / 2)
	center_y = int(height / 2)
	origin = (center_x, center_y)

	# global px_origin
	# px_origin = origin  # used in scale_output()
	# global scale
	# scale = hx_scale  # used in scale_output()
	# global px_grid_thickness
	# px_grid_thickness = int(grid_thickness)  # thickness of lines around hex

	arcade.open_window(width, height, 'arcade window')
	arcade.set_background_color(arcade.csscolor.BLACK)


def draw_hex(center, color=(255, 255, 255)):
	# draws a filled hex at center
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

	arcade.draw_polygon_filled(shape, color)


def draw_hex_outline(center, color=(0, 0, 0)):
	# draws empty hex outline
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

	arcade.draw_polygon_outline(shape, color, px_grid_thickness)


def draw_center(center, color=(255, 0, 0), size=2):
	# draws point, meant for center points of hex
	location = scale_output(
		ax2px(center),
		scale,
		px_origin
	)
	arcade.draw_circle_filled(location[0], location[1], size, color)


def draw_coords(center, color=(0, 0, 128)):
	# writes coordinates 10px below where they are
	# used to label coordinates on hex
	string_to_print = str(
		round_hx(
			ax2hx(
				center
			)
		)
	)

	position = scale_output(ax2px(center), scale, px_origin)
	# 10 is to offset vertically and show in bottom half of hex
	arcade.draw_text(string_to_print, position[0], position[1] - 10, color, 10)


def draw_line(start, stop, color=(100, 100, 100), line_width=2):
	# draws a straight line across map
	# highlights hexes it passes through
	# test points are drawn as small dots
	dist_hx = ax_distance(start, stop)
	start_px = ax2px(start)
	stop_px = ax2px(stop)
	dot_color = 175, 175, 175

	scaled_start = scale_output(start_px, scale, px_origin)
	scaled_stop = scale_output(stop_px, scale, px_origin)

	dx = (stop_px[0] - start_px[0]) / dist_hx
	dy = (stop_px[1] - start_px[1]) / dist_hx
	draw_x = start_px[0]
	draw_y = start_px[1]

	for i in range(dist_hx + 1):  # test points for hex distance + 1 to test start and end as well
		draw = (draw_x, draw_y)
		scaled_draw = scale_output(draw, scale, px_origin)

		# converts test point from pixel to hex coordinate, then rounds to nearest whole hex
		through_hex = round_hx(px2hx(draw))
		# color in hex that line passes through
		draw_hex(hx2ax(through_hex), (50, 50, 50))
		# draws circle on test point
		arcade.draw_circle_filled(scaled_draw[0], scaled_draw[1], 5, dot_color)
		draw_x = draw_x + dx  # increment x and y pixel position to next test point
		draw_y = draw_y + dy

	arcade.draw_line(scaled_start[0], scaled_start[1],
					 scaled_stop[0], scaled_stop[1], color, line_width)

def draw_cluster(center, color=(255, 0, 0), radius=2, draw_borders=True):

	for q in range(center[0] - radius, center[0] + radius + 1):
		for r in range(center[1] - radius, center[1] + radius + 1):
			draw_at = q, r
			if ax_distance(draw_at, center) <= radius:
				draw_hex(draw_at, color)
				if draw_borders:
					draw_hex_outline(draw_at)


def draw_cluster_center(center, color=(255, 255, 255), radius=2, draw_all_centers=False, cluster_radius=2):
	if draw_all_centers:
		for q in range(center[0] - cluster_radius, center[0] + cluster_radius + 1):
			for r in range(center[1] - cluster_radius, center[1] + cluster_radius + 1):
				draw_at = q, r
				if ax_distance(draw_at, center) <= cluster_radius:
					draw_center(draw_at, color, radius)

	else:
		draw_center(center, color, radius)
