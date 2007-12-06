#!/usr/bin/env python
"""Simple visual python demo"""

import visual as V

floor = V.box(pos=(0,0,0), length=4, height=0.5, width=4, color=V.color.blue)
ball = V.sphere(pos=(0,4,0), radius=1, color=V.color.red)
ball.velocity = V.vector(0,-1,0)
dt = 0.01

while 1:
    V.rate(100)
    ball.pos = ball.pos + ball.velocity*dt
    if ball.y < ball.radius:
        ball.velocity.y *= -0.8
    else:
        ball.velocity.y = ball.velocity.y - 9.8*dt
