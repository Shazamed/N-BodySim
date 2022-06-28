import numpy as np
import pygame
import sys
import random
import math

pygame.init()
size = width, height = 1000, 600
n = 100
dt = 0.1
WHITE = (255, 255, 255)
G = 5
SOFTENING = 0.2
energy_array = []
energy_diff = []

pos = np.random.rand(n, 2) * np.array([width,height])
vel = np.random.normal(size=(n, 2)).astype('float64')/2
forces = np.zeros([n, 2]).astype('float64')
masses = np.ones([n,1]).astype('float64')
colours = np.ones([n,3]).astype('float64')

def planets():
    global pos, vel, masses, forces
    pos[0] = np.array([width / 2, height / 2])
    vel[0] = np.array([0,0])
    masses[0] = 1250
    for i in range(1, n):
        orbit_radius = 300 + random.uniform(-1, 1) * 150
        velocity = (G * masses[0] / orbit_radius) ** 0.5
        mass = 0.5 + random.random()
        # bod_radius = 4 + random.random()
        col = (random.random() * 255, random.random() * 255, random.random() * 255)
        angle = math.radians(i * 360 / n)
        pos[i] = np.array([width / 2 + orbit_radius * math.sin(angle), height / 2 + orbit_radius * math.cos(angle)])
        vel[i] = np.array([velocity * math.cos(angle), -velocity * math.sin(angle)]).flatten()
        masses[i] = mass
        colours[i] = np.array([col])

planets()

screen = pygame.display.set_mode(size)
font = pygame.font.SysFont("calibri", 16)

time_elapsed = 0

def kick1():
    acc = forces/masses
    global vel
    vel += acc * dt / 2
    return


def drift():
    global pos
    pos += vel * dt
    return

def kick2():
    global vel
    calc_force()
    acc = forces/masses
    vel += acc * dt / 2
    return

def calc_force():
    global forces
    diff = pos.reshape(n, 1, 2) - pos
    r = np.sqrt((diff ** 2).sum(2) + SOFTENING ** 2)
    m_square = np.outer(masses, masses)
    forces = -(np.divide(G * m_square, (r ** 3))).reshape(n, n, 1) * diff
    # print(forces)
    forces[np.isnan(forces)] = 0.0
    forces = forces.sum(1)


def draw():
    pygame.draw.circle(screen, (255, 255, 0), pos[0], 10)
    for i in range(1, len(pos)):
        pygame.draw.circle(screen, colours[i], pos[i], 4)

def energy_calc():

    KE = 0.5 * np.sum(masses * vel ** 2)

    diff = pos.reshape(n, 1, 2) - pos
    r = np.sqrt((diff ** 2).sum(2))

    m_square = np.outer(masses, masses)
    PE = (np.divide(G * m_square, r).reshape(n, n, 1))/2
    PE[np.isinf(PE)] = 0.0
    PE = PE.sum(1)
    PE = np.abs(PE)
    PE = -PE.sum()

    energy = KE + PE
    return energy









i = 0
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    screen.fill(WHITE)
    kick1()
    drift()
    kick2()

    draw()
    total_energy = energy_calc()
    # com_pos = com_calc()
    time_elapsed += dt
    text_time = font.render(f'Elapsed Time: {time_elapsed}', False, (0, 0, 0))
    text_energy = font.render(f'Total Energy (U+K): {total_energy}', False, (0, 0, 0))
    # text_com = font.render(f'Center of Mass: {com_pos}', False, (0, 0, 0))
    # text_obj = font.render(f'Number of objects: {len(body_list)}', False, (0, 0, 0))
    screen.blit(text_time, (0, 0))
    screen.blit(text_energy, (0, 15))
    # screen.blit(text_com, (0, 30))
    # screen.blit(text_obj, (0, 45))

    # centerX = 0
    #         # centerY = 0
    #         # for primary_body in body_list:
    #         #     centerX += primary_body.px
    #         #     centerY += primary_body.py
    #         # print(centerX/4, centerY/4)

    pygame.display.flip()

    i += 1