import numpy as np
import random
import math
import params

def system_param(height, width, body_number):
    collision = True
    body_position = np.random.rand(body_number, 2) * np.array([width,height])
    body_velocity = np.random.normal(size=(body_number, 2)).astype('float64')/2
    body_forces = np.zeros([body_number, 2]).astype('float64')
    body_mass = np.ones([body_number, 1]).astype('float64')
    body_colour = np.ones([body_number, 3]).astype('float64')
    body_radii = np.ones([body_number, 1]).astype('float64')
    body_position[0] = np.array([width / 2, height / 2])
    body_velocity[0] = np.array([0,0])
    body_mass[0] = 125000
    body_colour[0] = (255, 255, 0)
    body_radii[0] = 30
    for i in range(1, body_number):
        orbit_radius = 350 + random.uniform(-1, 1) * 250
        velocity = 1 * (params.G * body_mass[0] / orbit_radius) ** 0.5

        mass = 1 + random.random()*10
        bod_radius = (1/params.DENSITY) * (mass ** (1/3)) * (3 / (4 * math.pi)) ** (1/3)

        col = (random.random() * 255, random.random() * 255, random.random() * 255)
        angle = math.radians(i * 360 / (body_number-1))
        body_position[i] = np.array([width / 2 + orbit_radius * math.sin(angle), height / 2 + orbit_radius * math.cos(angle)])
        body_velocity[i] = np.array([velocity * math.cos(angle), -velocity * math.sin(angle)]).flatten()
        body_mass[i] = mass
        body_colour[i] = np.array([col])
        body_radii[i] = bod_radius
    return body_position, body_velocity, body_forces, body_mass, body_colour, body_radii, collision
