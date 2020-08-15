
from typing import List, Set, Dict, Tuple, Optional
import math


def hx2ax(hx: Tuple[float, float, float]):
	#converts hex xyz coordinates to axial qr coordinates
	x = hx[0]
	y = hx[1]
	z = hx[2]

	#hx = axial with extra redundant coordinate
	q = x
	r = y
	axial = (q,r)
	return axial


def ax2hx(axial: Tuple[float, float]):
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

def ax2px(axial: Tuple[float, float]):
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

def px2ax(pixel: Tuple[float, float]):
	#converts pixel xy coordinates to axial qr coordinates
	x = pixel[0]
	y = pixel[1]
	#solve equations in ax2bx for q and r
	q = 2/math.sqrt(3)*x
	r = y+x/math.sqrt(3)
	axial = (q,r)
	return axial

def hx2px(hx: Tuple[float, float, float]):
	#converts hex xyz coordinates to pixel xy coordinates
	x = hx[0]
	y = hx[1]
	z = hx[2]

	#hex = axial with extra redundant coordinate
	#convert to axial, then call ax2px
	axial = hx2ax((x,y,z))
	pixel = ax2px(axial)
	return pixel


def px2hx(pixel: Tuple[float, float]):
	#converts pixel xy coordinates to hex xyz coordinates
	x = pixel[0]
	y = pixel[1]

	#hx = axial with extra redundant coordinate
	#call px2ax then convert to hex
	axial = px2ax((x,y))
	hx = ax2hx(axial)
	return hx


def hx_dist(start: Tuple[float, float, float], stop: Tuple[float, float, float]):
	#calculates distance between 2 xyz hex points
	dx = abs(stop[0]-start[0])
	dy = abs(stop[1]-start[1])
	dz = abs(stop[2]-start[2])

	#x+y+z=0 is always true for hex coordinates
	#the largest translation will equal and opposite to the sum of the other 2, but we don't care about sign for absolute distance
	#translation is on any 2 axis so largest counts same as other 2
	distance = max(dx,dy,dz)
	return distance

def ax_distance(start: Tuple[float, float], stop: Tuple[float, float]):
	#calculates distance between 2 qr axial points
	#converts to hex for calculation
	hx_start = ax2hx(start)
	hx_stop = ax2hx(stop)
	hx_distance = hx_dist(hx_start,hx_stop)
	ax_distance = hx_distance
	return ax_distance


def round_hx(hx: Tuple[float, float, float]):
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
	if max(diffs) == dx:
		round_x = -(round_y+round_z)
	elif  max(diffs) == dy:
		round_y = -(round_x+round_z)
	else:
		round_z = -(round_x+round_y)

	rounded_hx = (round_x,round_y,round_z)
	return rounded_hx


def round_ax(axial: Tuple[float, float]):
	#convert to hex then round to take advantage of always discarding worst rounding amount
	hx = ax2hx(axial)
	round_hx = round_hx(hx)
	round_ax = hx2ax(round(hx))
	return round_ax

def draw_px_hx(pixel: Tuple[float, float], scale, origin: Tuple[float, float]):
	x = pixel[0]
	y = pixel[1]

	x1 = (x - 1/(2*math.sqrt(3)))*scale + origin[0]
	y1 = (y + 0.5)*scale + origin[1]
	x2 = (x + 1/(2*math.sqrt(3)))*scale + origin[0]
	y2 = (y + 0.5)*scale + origin[1]
	x3 = (x + 1/math.sqrt(3))*scale + origin[0]
	y3 = (y)*scale + origin[1]
	x4 = (x + 1/(2*math.sqrt(3)))*scale + origin[0]
	y4 = (y - 0.5)*scale + origin[1]
	x5 = (x - 1/(2*math.sqrt(3)))*scale + origin[0]
	y5 = (y - 0.5)*scale + origin[1]
	x6 = (x - 1/math.sqrt(3))*scale + origin[0]
	y6 = (y)*scale + origin[1]

	xy_points = [
		(x1,y1),
		(x2,y2),
		(x3,y3),
		(x4,y4),
		(x5,y5),
		(x6,y6)]
	return xy_points
