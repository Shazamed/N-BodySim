import colorsys

import numpy as np
import math
def system_param(height, width, body_number):
    collision = False
    dt = 0.05
    velocity = 1
    radius = 100
    body_position = np.zeros([body_number, 2]).astype('float64')
    body_velocity = np.zeros([body_number, 2]).astype('float64')
    body_forces = np.zeros([body_number, 2]).astype('float64')
    body_mass = np.full([body_number, 1], 240).astype('float64')
    body_colour = np.full([body_number, 3], 0).astype('float64')
    body_radii = np.full([body_number, 1], 5).astype('float64')


    body_l = []
    for i in range(body_number):
        angle = math.radians(i * 360 / body_number)
        # col = tuple(round(i * 255) for i in colorsys.hsv_to_rgb(i / body_number, 1, 0.7))
        body_position[i] = np.array([width/2 + radius * math.sin(angle), height/2 + radius * math.cos(angle)])
        body_velocity[i] = np.array([velocity * math.cos(angle), -velocity * math.sin(angle)])
    return body_position, body_velocity, body_forces, body_mass, body_colour, body_radii, collision, dt

