import numpy as np
import pygame
import sys
import random
import math

pygame.init()
size = width, height = 1000, 600
n = 400
dt = 0.05
WHITE = (255, 255, 255)
G = 5
SOFTENING = 0.2
DENSITY = 0.75
COLLISIONS = True
energy_array = []
energy_diff = []

pos = np.random.rand(n, 2) * np.array([width,height])
vel = np.random.normal(size=(n, 2)).astype('float64')/2
forces = np.zeros([n, 2]).astype('float64')
masses = np.ones([n,1]).astype('float64')
colours = np.ones([n,3]).astype('float64')
bod_radii = np.ones([n,1]).astype('float64')

def planets():
    pos[0] = np.array([width / 2, height / 2])
    vel[0] = np.array([0,0])
    masses[0] = 12500
    colours[0] = (255, 255, 0)
    bod_radii[0] = 30
    for i in range(1, n):
        orbit_radius = 350 + random.uniform(-1, 1) * 250
        velocity = 1 * (G * masses[0] / orbit_radius) ** 0.5

        mass = 1 + random.random()
        bod_radius = (1/DENSITY) * (mass ** (1/3)) * (3 / (4 * math.pi)) ** (1/3)

        col = (random.random() * 255, random.random() * 255, random.random() * 255)
        angle = math.radians(i * 360 / (n-1))
        pos[i] = np.array([width / 2 + orbit_radius * math.sin(angle), height / 2 + orbit_radius * math.cos(angle)])
        vel[i] = np.array([velocity * math.cos(angle), -velocity * math.sin(angle)]).flatten()
        masses[i] = mass
        colours[i] = np.array([col])
        bod_radii[i] = bod_radius


def kick1():
    global vel
    acc = forces/masses
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
    diff = pos.reshape(masses.size, 1, 2) - pos
    r = np.sqrt((diff ** 2).sum(2) + SOFTENING ** 2)

    m_square = np.outer(masses, masses)
    forces = -(np.divide(G * m_square, (r ** 3))).reshape(masses.size, masses.size, 1) * diff
    forces[np.isnan(forces)] = 0.0
    forces = forces.sum(1)
    if COLLISIONS:
        collision_check(r)


def draw():
    for i in range(0, len(pos)):
        pygame.draw.circle(screen, colours[i], pos[i], bod_radii[i][0])


def energy_calc():

    KE = 0.5 * np.sum(masses * vel ** 2)

    diff = pos.reshape(masses.size, 1, 2) - pos
    r = np.sqrt((diff ** 2).sum(2))

    m_square = np.outer(masses, masses)
    PE = (np.divide(G * m_square, r).reshape(masses.size, masses.size, 1))/2
    PE[np.isinf(PE)] = 0.0
    PE = PE.sum(1)
    PE = np.abs(PE)
    PE = -PE.sum()

    energy = KE + PE
    return energy


def center_of_mass_calc():
    com = (masses * pos / masses.sum()).sum(0)
    return com.tolist()

def collision_check(r):
    global pos, masses, forces, colours, vel, bod_radii
    radii_sum = bod_radii + bod_radii.T
    d = r - radii_sum
    conditional = ((d<0) & (r!=SOFTENING))
    conditional_col = np.zeros([masses.size])
    indices = np.transpose(np.nonzero(conditional == True))
    if indices.size !=0:
        for idx in indices:
            if not conditional_col[idx[0]]:
                pos[idx[0]] = (pos[idx[0]] * masses[idx[0]]+ pos[idx[1]] * masses[idx[1]]) / (masses[idx[0]] + masses[idx[1]])
                vel[idx[0]] = (masses[idx[0]] * vel[idx[0]] + masses[idx[1]] * vel[idx[1]]) / (masses[idx[0]] + masses[idx[1]])
                masses[idx[0]] = masses[idx[0]] + masses[idx[1]]
                bod_radii[idx[0]] = (1/DENSITY) * (masses[idx[0]] ** (1 / 3)) * (3 / (4 * math.pi)) ** (1 / 3)
                conditional_col[idx[1]] = True
    pos = pos[conditional_col == 0]
    masses = masses[conditional_col == 0]
    vel = vel[conditional_col == 0]
    forces = forces[conditional_col == 0]
    colours = colours[conditional_col == 0]
    bod_radii = bod_radii[conditional_col == 0]



planets()

screen = pygame.display.set_mode(size)
font = pygame.font.SysFont("calibri", 16)

time_elapsed = 0

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
    com_pos = center_of_mass_calc()
    time_elapsed += dt
    text_time = font.render(f'Elapsed Time: {time_elapsed}', False, (0, 0, 0))
    text_energy = font.render(f'Total Energy (U+K): {total_energy}', False, (0, 0, 0))
    text_com = font.render(f'Center of Mass: {com_pos}', False, (0, 0, 0))
    text_obj = font.render(f'Number of bodies: {masses.size}', False, (0, 0, 0))
    screen.blit(text_time, (0, 0))
    screen.blit(text_energy, (0, 15))
    screen.blit(text_com, (0, 30))
    screen.blit(text_obj, (0, 45))

    pygame.display.flip()

    i += 1