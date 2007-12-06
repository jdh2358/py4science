#!/usr/bin/env python
"""Visual Python demo: shooting a falling object.

Note that this script can NOT be run inside ipython via the 'run' command.
You MUST run it from the command line as a standalone program.  Start by doing

chmod +x shoot.py

(or whatever you called it), and then you can run it via

./shoot.py
"""

import time
import sys

# Visual is built on top of the 'old' Numeric, so do NOT use numpy here.  We
# do a wholesale import for coding convenience, this is highly discouraged in
# larger codebases (but usually OK in very small demo scripts and interactive
# use).
from Numeric import *

import visual as V

# Geometric parameters  (all in MKS units)
theta = pi/4  # initial angle of gun
D = 20  # width ...
H = 20  # height of floor
g = -9.8  # gravity
gun_len = 2  # size of gun
arrow_len = 4  # and of arrow
v0_default = 15  # default for initial velocity if not given

# Numerical simulation parameters
dt = 0.01
# Update for all velocities under constant acceleration (gravity)
dv = V.vector(0,g*dt,0)

# Tolerance for deciding whether a collision happened
impact_distance = 0.5

# Initialize arguments
try:
    v0 = float(sys.argv[1])
except:
    v0 = v0_default
    print 'Using default v0 =',v0,'m/s.'

# Build 3d world

# Define the line of sight
sight = V.vector(cos(theta),sin(theta),0)

# The floor is just a thin box
floor = V.box(pos=(D/2.,0,0), length=D, height=0.5, width=D, color=V.color.blue)

# Use a cone for our 'arrow'
arrow = V.cone(pos=(0,0,0), radius=0.9, axis=sight,color=V.color.red)
arrow.velocity = v0*sight

# The target is a sphere
target = V.sphere(pos=(D,H,0), radius=1, color=V.color.yellow)
target.velocity = V.vector(0,0,0)

# The 'dart gun' is just a cylinder.
gun = V.cylinder(pos=(0,0,0), axis=gun_len*sight, radius=1,
                 color = V.color.green)

# Run simulation

print 'Starting simulation...'

# Put a little delay to give all the OpenGL stuff time to initialize nicely.
time.sleep(1)

while (arrow.y >= 0 and target.y >=0) and \
          V.mag(arrow.pos-target.pos) > impact_distance:

    V.rate(75)

    for obj in (arrow,target):
        obj.pos += obj.velocity*dt
        obj.velocity += dv

# Report to user.
if V.mag(arrow.pos-target.pos) <= impact_distance:
    print 'Hit!'
else:
    print 'Miss...'
