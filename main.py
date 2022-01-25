import pygame
import sys
import random
pygame.init()
size = width, height = 900, 600
white = 255, 255, 255

# Constants
G = 10
dt = 0.07
softening = 0.002

# TODO: research on velocity verlet, Barnes-Hut algorithm & Runge–Kutta method

class Planet:
    def __init__(self, pos, vel, mass, size):
        self.px = pos[0]
        self.py = pos[1]
        self.vx = vel[0]
        self.vy = vel[1]
        self.fx = 0
        self.fy = 0
        self.m = mass
        self.sz = size

    def calc_force(self, objects):
        self.fx, self.fy = 0, 0
        for obj in objects:
            rx = obj.px - self.px
            ry = obj.py - self.py
            if rx == 0 and ry == 0:
                continue
            radius = (rx ** 2 + ry ** 2 + softening**2)**(1/2)
            self.fx += G * self.m * obj.m / (radius ** 3) * rx
            self.fy += G * self.m * obj.m / (radius ** 3) * ry

    def new_position(self):
        ax = self.fx / self.m
        ay = self.fy / self.m

        self.vx += ax * dt
        self.vy += ay * dt
        self.px += self.vx * dt
        self.py += self.vy * dt

        pygame.draw.circle(screen, (0, 0, 0), (self.px, self.py), self.sz)

    def kick1(self):
        ax = self.fx / self.m
        ay = self.fy / self.m
        self.vx += ax * dt / 2
        self.vy += ay * dt / 2

    def drift(self):
        self.px += self.vx * dt
        self.py += self.vy * dt

    def kick2(self):
        self.calc_force(body_list)
        ax = self.fx / self.m
        ay = self.fy / self.m
        self.vx += ax * dt / 2
        self.vy += ay * dt / 2
        pygame.draw.circle(screen, (0, 0, 0), (self.px, self.py), self.sz)


def energy_calc():
    energy = 0
    for i in range(len(body_list)):
        for j in range(i + 1, len(body_list)):
            energy += -1 * G * body_list[i].m * body_list[j].m / (
                        ((body_list[i].px - body_list[j].px) ** 2 + (body_list[i].py - body_list[j].py) ** 2) ** (
                            1 / 2))

    for primary_body in body_list:
        energy += 0.5 * primary_body.m * (primary_body.vx ** 2 + primary_body.vy ** 2)
    print(energy)


# simulations

def first_sim():
    sun = Planet((450, 325), (0, -0.12), 125, 10)
    moon = Planet((60, 250), (0, 3.3), 2, 3)
    earth = Planet((100, 250), (0, 1.6), 10, 5)
    comet = Planet((520, 325), (0, -5.5), 0.2, 2)
    mercury = Planet((580, 325), (0, -3), 2, 4)
    return [sun, earth, moon, mercury, comet]


def binary_sunset():
    sun1 = Planet((300, 325), (0, 4), 1000, 10)
    sun2 = Planet((600, 325), (0, -4), 1000, 10)
    return [sun1, sun2]


def elliptic():
    sun = Planet((200, 325), (0, 0), 10000, 10)
    comet = Planet((100, 325), (0, 42), 1, 5)
    return [sun, comet]


def lagrangian():
    sun = Planet((450, 325), (0, 0), 1250, 10)
    jupiter = Planet((200, 325), (0, -7), 10, 5)
    body_l = [sun, jupiter]
    for x in range(60):
        body_l.append(Planet((450, random.uniform(500, 550)), (-8, 0), 0.0001, 2))
    return body_l

def four_body():
    sun1 = Planet((200, 300), (0, 2.2), 100, 10)
    sun2 = Planet((600, 300), (0, -2.2), 100, 10)
    sun3 = Planet((400, 100), (-2.2, 0), 100, 10)
    sun4 = Planet((400, 500), (2.2, 0), 100, 10)
    return [sun1, sun2, sun3, sun4]


if __name__ == '__main__':
    screen = pygame.display.set_mode(size)
    body_list = first_sim()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        screen.fill(white)
        for primary_body in body_list:
            # primary_body.calc_force(body_list)
            primary_body.kick1()
            primary_body.drift()

        for primary_body in body_list:
            # primary_body.new_position()
            primary_body.kick2()

        energy_calc()

        # centerX = 0
        #         # centerY = 0
        #         # for primary_body in body_list:
        #         #     centerX += primary_body.px
        #         #     centerY += primary_body.py
        #         # print(centerX/4, centerY/4)



        pygame.display.flip()
