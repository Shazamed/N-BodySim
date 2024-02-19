import numpy as np
import pygame
import sys
from Scenarios import *
import params

import math

pygame.init()
size = width, height = 1000, 600
body_number = 400
WHITE = (255, 255, 255)
energy_array = []
energy_diff = []

class system_frame:
    def __init__(self, position, velocity, forces, mass, colour, radii, collision=False, dt=0.05):
        self.body_position = position
        self.body_velocity = velocity
        self.body_forces = forces
        self.body_mass = mass
        self.body_colour = colour
        self.body_radii = radii
        self.dt = dt
        self.collision = collision

        # self.body_position = np.random.rand(n, 2) * np.array([width,height])
        # self.body_velocity = np.random.normal(size=(n, 2)).astype('float64')/2
        # self.body_forces = np.zeros([n, 2]).astype('float64')
        # self.body_mass = np.ones([n, 1]).astype('float64')
        # self.body_colour = np.ones([n, 3]).astype('float64')
        # self.body_radii = np.ones([n, 1]).astype('float64')

    def kick1(self):
        body_acceleration = self.body_forces / self.body_mass
        self.body_velocity += body_acceleration * self.dt / 2
        return

    def drift(self):
        self.body_position += self.body_velocity * self.dt
        return

    def kick2(self):
        self.calc_force()
        body_acceleration = self.body_forces / self.body_mass
        self.body_velocity += body_acceleration * self.dt / 2
        return

    def calc_force(self):
        diff = self.body_position.reshape(self.body_mass.size, 1, 2) - self.body_position
        r = np.sqrt((diff ** 2).sum(2) + params.SOFTENING ** 2)

        m_square = np.outer(self.body_mass, self.body_mass)
        self.body_forces = -(np.divide(params.G * m_square, (r ** 3))).reshape(self.body_mass.size, self.body_mass.size, 1) * diff
        self.body_forces[np.isnan(self.body_forces)] = 0.0
        self.body_forces = self.body_forces.sum(1)
        if self.collision:
            self.collision_check(r)

    def energy_calc(self):

        KE = 0.5 * np.sum(self.body_mass * self.body_velocity ** 2)

        diff = self.body_position.reshape(self.body_mass.size, 1, 2) - self.body_position
        r = np.sqrt((diff ** 2).sum(2))

        m_square = np.outer(self.body_mass, self.body_mass)
        PE = (np.divide(params.G * m_square, r).reshape(self.body_mass.size, self.body_mass.size, 1)) / 2
        PE[np.isinf(PE)] = 0.0
        PE = PE.sum(1)
        PE = np.abs(PE)
        PE = -PE.sum()

        energy = KE + PE
        return energy

    def center_of_mass_calc(self):
        com = (self.body_mass * self.body_position / self.body_mass.sum()).sum(0)
        return com.tolist()

    def collision_check(self, r):
        radii_sum = self.body_radii + self.body_radii.T
        d = r - radii_sum
        conditional = ((d < 0) & (r != params.SOFTENING))
        conditional_col = np.zeros([self.body_mass.size])
        indices = np.transpose(np.nonzero(conditional == True))
        if indices.size != 0:
            for idx in indices:
                if not conditional_col[idx[0]]:
                    self.body_position[idx[0]] = (self.body_position[idx[0]] * self.body_mass[idx[0]] + self.body_position[idx[1]] * self.body_mass[idx[1]]) / (
                                self.body_mass[idx[0]] + self.body_mass[idx[1]])
                    self.body_velocity[idx[0]] = (self.body_mass[idx[0]] * self.body_velocity[idx[0]] + self.body_mass[idx[1]] * self.body_velocity[idx[1]]) / (
                                self.body_mass[idx[0]] + self.body_mass[idx[1]])
                    self.body_mass[idx[0]] = self.body_mass[idx[0]] + self.body_mass[idx[1]]
                    self.body_radii[idx[0]] = (1 / params.DENSITY) * (self.body_mass[idx[0]] ** (1 / 3)) * (3 / (4 * math.pi)) ** (
                                1 / 3)
                    conditional_col[idx[1]] = True
        self.body_position = self.body_position[conditional_col == 0]
        self.body_mass = self.body_mass[conditional_col == 0]
        self.body_velocity = self.body_velocity[conditional_col == 0]
        self.body_forces = self.body_forces[conditional_col == 0]
        self.body_colour = self.body_colour[conditional_col == 0]
        self.body_radii = self.body_radii[conditional_col == 0]

    def draw(self):
        for i in range(0, len(self.body_position)):
          pygame.draw.circle(screen, self.body_colour[i], self.body_position[i], self.body_radii[i][0])


system = system_frame(*solar_system_evolution.system_param(height,width,body_number))
system = system_frame(*infinity.system_param(height,width))
system = system_frame(*symmetric_n_body.system_param(height,width,3))

screen = pygame.display.set_mode(size)
font = pygame.font.SysFont("calibri", 16)

time_elapsed = 0

i = 0
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    screen.fill(WHITE)

    system.kick1()
    system.drift()
    system.kick2()

    system.draw()

    total_energy = system.energy_calc()
    com_pos = system.center_of_mass_calc()

    time_elapsed += system.dt
    text_time = font.render(f'Elapsed Time: {time_elapsed}', False, (0, 0, 0))
    text_energy = font.render(f'Total Energy (U+K): {total_energy}', False, (0, 0, 0))
    text_com = font.render(f'Center of Mass: {com_pos}', False, (0, 0, 0))
    text_obj = font.render(f'Number of bodies: {system.body_mass.size}', False, (0, 0, 0))
    screen.blit(text_time, (0, 0))
    screen.blit(text_energy, (0, 15))
    screen.blit(text_com, (0, 30))
    screen.blit(text_obj, (0, 45))

    pygame.display.flip()

    i += 1

#
# # simulations
# def first_sim():
#     sun = Planet((450, 325), (0, -0.12), 500, 10, BLACK)
#     moon = Planet((60, 250), (0, 5.5), 3, 3, BLACK)
#     earth = Planet((100, 250), (0, 3.6), 15, 5, BLACK)
#     comet = Planet((520, 325), (0, -10), 0.2, 2, BLACK)
#     mercury = Planet((580, 325), (0, -5), 2, 4, BLACK)
#     return [sun, earth, moon, mercury, comet]
#
#
# def binary_sunset():
#     sun1 = Planet((300, 325), (0, 0), 100, 20, BLACK)
#     sun2 = Planet((600, 325), (0, 0), 1000, 20, BLACK)
#     return [sun1, sun2]
#
#
# def elliptic():
#     sun = Planet((200, 325), (0, 0), 10000, 10, BLACK)
#     comet = Planet((100, 325), (0, 42), 1, 5, BLACK)
#     return [sun, comet]
#
#
# def spam():
#     sun = Planet((width/2, height/2), (0, 0), 1500, 30, (255, 255, 0))
#     # planet = Planet((200, 400), (0, 7.25), 10, 5, BLACK)
#     body_l = [sun]
#     n = 100
#     for i in range(n):
#         orbit_radius = 400 + random.uniform(-1,1) * 325
#         velocity = (G * sun.m / orbit_radius) ** 0.5
#         mass = 0.5 + random.random()
#         bod_radius = 4 + random.random()
#         col = (random.random() * 255, random.random() * 255, random.random() * 255)
#         angle = math.radians(i * 360 / n)
#         body_l.append(Planet((width/2 + orbit_radius * math.sin(angle), height/2 + orbit_radius *
#                               math.cos(angle)), (velocity * math.cos(angle), -velocity * math.sin(angle)), mass, bod_radius, col))
#     return body_l
#
#
# def four_body():
#     sun1 = Planet((200, 300), (0, 1.55), 50, 10, BLACK)
#     sun2 = Planet((600, 300), (0, -1.55), 50, 10, BLACK)
#     sun3 = Planet((400, 100), (-1.55, 0), 50, 10, BLACK)
#     sun4 = Planet((400, 500), (1.55, 0), 50, 10, BLACK)
#     return [sun1, sun2, sun3, sun4]
#
#
# def figure_eight():
#     mass = 20
#     sun1 = Planet((450 - 97 * 2, 300 + 24 * 2), (0.466203685, 0.43236573), mass, 5, BLACK)
#     sun2 = Planet((450 + 97 * 2, 300 - 24 * 2), (0.466203685, 0.43236573), mass, 5, BLACK)
#     sun3 = Planet((450, 300), (-0.93240737, -0.86473146), mass, 5, BLACK)
#     return [sun1, sun2, sun3]
#
#
# def border_of_wave_and_particle():
#     velocity = 0.8
#     mass = 5
#     radius = 200
#     body_l = []
#     n = 12
#
#     for i in range(n):
#         angle = math.radians(i * 360 / n)
#         col = tuple(round(i * 255) for i in colorsys.hsv_to_rgb(i / n, 1, 0.7))
#         body_l.append(Planet((450 + radius * math.sin(angle), 300 + radius * math.cos(angle)),
#                              (velocity * math.cos(angle), -velocity * math.sin(angle)), mass, 3, col))
#     return body_l
