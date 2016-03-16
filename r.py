#!/usr/bin/python3

import numpy as np
import itertools, sys

# Works with odd cubes
# Store each cubie as a 3x3x3 array, with colours of stickers on each face in the six elements (1,0,0), (-1,0,0), (0,1,0), etc.
# Overall cube a concatenation of cubies

# Colour 0 is transparent/no sticker

N = 3 #size of the Rubik's cube, must be odd


T = 3*N #side length of representation

class Cube: #To be indexed with 3-vectors, centre cell is (0,0,0)
	def __init__(self, T):
		assert(T>=1 and T%2==1)
		self.C = np.zeros( (T,T,T), np.int_)
		self.centre = np.array([T//2, T//2, T//2], np.int_)
	
	def tup(self, a):
		z = tuple((a+self.centre).tolist())
		assert(len(z) == 3)
		assert(all(0 <= d < T for d in z))
		return z
	
	def __getitem__(self, q):
		return self.C[self.tup(q)]
	
	def __setitem__(self, q, k):
		self.C[self.tup(q)] = k

# Match POVray as far as possible
x = np.array([1,0,0], np.int_)
y = np.array([0,1,0], np.int_)
z = np.array([0,0,1], np.int_)

C = Cube(T)

def initface(d, od1, od2, c):
	Nby2 = (N-1)//2
	idxs = list(range(-Nby2, 1 + Nby2))
	for i in idxs:
		for j in idxs:
			C[(3*Nby2+1)*d + (3*i*od1) + (3*j*od2)] = c

WHITE=1
YELLOW=2
RED=3
ORANGE=4
BLUE=5
GREEN=6

colours = ['Blank', 'White', 'Yellow', 'Red', 'Orange', 'Blue', 'Green']

# POVray conventions for view
#+ and - for emphasis. Sign doesn't matter where not noted
# This is for 3x3x3:
initface(+x, y, z, RED) # R face
initface(-x, y, z, ORANGE) #L face
initface(+y, z, x, WHITE) #U face
initface(-y, z, x, YELLOW) #D face
initface(+z, x, y, BLUE) #B face
initface(-z, x, y, GREEN) #F face

def rotate(d, s, layers=[1]):
	'''Rotate layers in the direction of the unit vector d. Default is layers=[1] to rotate face for a 3x3x3 cube. Direction of rotation (clockwise or anticlockwise) is given by s, which is +1 or -1.'''
	
	assert(all(-(N//2) <= layer <= (N//2) for layer in layers))
	# Permutation is a product of cycles of length 4. Implemented in place, by executing each cycle at one go.
	assert(d.dot(d) == 1)
	def rot(w):
		return(s*np.cross(d,w))
	
	p = np.array([d[1], d[2], d[0]], np.int_)
	q = rot(p)
	assert(p.dot(p) == 1 and q.dot(q) == 1)
	assert(d.dot(p) == 0 and d.dot(q) == 0 and p.dot(q) == 0)
	#p,q,d mutually perpendicular unit vectors. Sign of p and q doesn't matter.
	finelayers = [h for layer in layers for h in [(3*layer-1)*d, 3*layer*d, (3*layer+1)*d] ]
	for h in finelayers:
		for i in range(1, (T-1)//2 + 1):
			for j in range(0, (T-1)//2 + 1): #one of i and j starts with 0, other with 1
				w = i*p + j*q
				[C[h+w] , C[h+rot(w)], C[h+rot(rot(w))], C[h+rot(rot(rot(w)))] ] = [C[h+q] for q in [rot(rot(rot(w))), w, rot(w), rot(rot(w))]]

def vec_in_pov(w):
	return ('<{},{},{}>'.format(w[0], w[1], w[2]))

def cubie_macro(w):
	# In POVray: #macro Cubie(F, R, U, B, L, D, tr)
	w3 = 3*w
	r = ['Cubie(']
	r.append(','.join([colours[C[s]] for s in [w3-z, w3+x, w3+y, w3+z, w3-x, w3-y]]))
	r.extend([',', vec_in_pov(w), ')'])
	return ''.join(r)



def rot_output(d, s, layers=[1]):
	'''Output a representation of the cube undergoing this rotation. Parameters as in 'rotate'.'''
	idxs = list(range(-(N//2), 1 + (N//2)))
	for ww in itertools.product(idxs, idxs, idxs):
		w = np.array(ww)
		if w.dot(d) in layers:
			print('object{ ', end='')
			print(cubie_macro(w), end='')
			print(' rotate ', end='')
			print('rot*90*' + vec_in_pov(s*d), end='')
			print('}')
		else:
			print(cubie_macro(w))
	rotate(d, s, layers)


#for 3x3x3
#Face rotations:
singm = {
	"F" : (-z, 1), "F'" : (-z, -1),
	"R" : ( x, 1), "R'" : ( x, -1),
	"U" : ( y, 1), "U'" : ( y, -1),
	"B" : ( z, 1), "B'" : ( z, -1),
	"L" : (-x, 1), "L'" : (-x, -1),
	"D" : (-y, 1), "D'" : (-y, -1) }
def addl(p, b):
	return (p[0], p[1], b)
#Two-layer rotations:
for k in [q for q in singm.keys()]:
	s = addl(singm[k], [0,1])
	singm[k.lower()] = s
	singm[k[0] + 'w' + k[1:]] = s
#Whole-cube rotations:
for (c,d) in [ ("x", "R"), ("x'", "R'"), ("y", "U"), ("y'", "U'"), ("z", "F"), ("z'", "F'")]:
	singm[c] = addl(singm[d], [-1,0,1])


DEFW=960
DEFH=720

import argparse
epilog='If only one of width and height is specified, the other is computed assuming a 4:3 aspect ratio. If neither is specified, the default is a width of {} and a height of {}.'.format(DEFW, DEFH)
parser = argparse.ArgumentParser(epilog=epilog)
parser.add_argument('base', type=str, help='base filename for output POV-Ray sources')
parser.add_argument('-o', '--outf', type=str, dest='out', help='base filename for output images (default: same as base)')
parser.add_argument('script', type=str, help='output render script filename')
parser.add_argument('-f', '--frames', type=int, dest='frames', default=16, help='number of frames per rotation (default: 16)')
parser.add_argument('-W', '--width', type=int, dest='width', help='width in pixels')
parser.add_argument('-H', '--height', type=int, dest='height', help='height in pixels')
parser.add_argument('-p', '--povray-bin', type=str, dest='povbin', default='povray', help='POV-Ray executable')
parser.add_argument('-m', '--moves', type=str, dest='moves', help='sequence of moves (can alternatively be provided on stdin)')
parser.add_argument('-a', '--pov-options', type=str, dest='povoptions', default='+A +AM2 +R2', help='command-line options to POV-Ray (default: +A +AM2 +R2)')

args = parser.parse_args()
FR = args.frames
assert(FR>=1)
shflnm=args.script
POVBIN=args.povbin
basef=args.base
outf=args.base+'.png'
if args.out != None:
	outf=args.out+'.png'

def getWH(W,H):
	import fractions
	F = fractions.Fraction
	if W==None and H==None:
		return (DEFW, DEFH)
	if W==None:
		assert(H>0)
		W = max(1,round(H*F(4,3)))
		return (W,H)
	if H==None:
		assert(W>0)
		H = max(1,round(W*F(3,4)))
		return (W,H)
	assert(W > 0 and H > 0)
	return (W,H)

W, H = getWH(args.width, args.height)

moves = args.moves
if moves == None:
	moves = input().split()
else:
	moves = moves.split()

def resolve2(inp):
	ans=[]
	for m in inp:
		if(len(m) > 1 and m[-1] == '2'):
			ans.append(m[:-1])
			ans.append(m[:-1])
		else:
			ans.append(m)
	return ans


moves=resolve2(moves)


assert(all(m in singm.keys() for m in moves))

TOTFR = len(moves)*FR


baseframe = int('1' + (len(str(TOTFR)))*'0')
POVOPT = '+W{} +H{} {} -D'.format(W, H, args.povoptions)


with open(shflnm, 'w') as script:
	for (i,m) in enumerate(moves):
		flnm = basef + str(i).zfill(len(str(len(moves)))) + '.pov'
		with open(flnm, 'w') as sys.stdout:
			print('#include "cube_setup_scene.inc"')
			rot_output(*singm[m])
		if i != len(moves) - 1:
			print('{} +I{} +O{} {} +KFI{} +KFF{} +KC'.format(POVBIN, flnm, outf, POVOPT, baseframe+i*FR, baseframe+(i+1)*FR-1), file=script)
		else: #special case for the last frame : the total number of frames is the total number of gaps between frame plus 1
			print('{} +I{} +O{} {} +KFI{} +KFF{}'.format(POVBIN, flnm, outf, POVOPT, baseframe+i*FR, baseframe+(i+1)*FR), file=script)

