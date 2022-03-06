import pygame
import sys
import random
import math
import colorsys

pygame.init()
size = width, height = 1000, 600
WHITE = 255, 255, 255
BLACK = (0, 0, 0)
COLLISIONS = True  # does not conserve energy
# Constants
G = 5
dt = 0.8
SOFTENING = 0.2
MAX_TRAILS = 100
step = 5


# TODO: research on velocity verlet, Barnes-Hut algorithm & Runge–Kutta method


class Planet:
    def __init__(self, pos, vel, mass, radius, colour):
        self.px = pos[0]
        self.py = pos[1]
        self.vx = vel[0]
        self.vy = vel[1]
        self.fx = 0
        self.fy = 0
        self.m = mass
        self.rad = radius
        self.prev_p = [(pos[0], pos[1])]
        # self.colour = (43, 208, 63)
        self.colour = colour

    def calc_force(self, objects):
        self.fx, self.fy = 0, 0
        for obj in objects:
            rx = obj.px - self.px
            ry = obj.py - self.py
            if rx == 0 and ry == 0:
                continue
            if COLLISIONS and self.collision_check((rx, ry), obj):  # collision check
                continue

            radius = (rx ** 2 + ry ** 2 + SOFTENING ** 2) ** (1 / 2)
            self.fx += G * self.m * obj.m / (radius ** 3) * rx
            self.fy += G * self.m * obj.m / (radius ** 3) * ry

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

    def draw(self):
        pygame.draw.circle(screen, self.colour, (self.px, self.py), self.rad)

    def trails(self):
        self.prev_p.append((self.px, self.py))
        # max_trails = 1000/((self.vx ** 2 + self.vy ** 2) ** (1/2)+1)
        if len(self.prev_p) > MAX_TRAILS:
            self.prev_p.pop(0)
            # self.prev_p = self.prev_p[(len(self.prev_p) - int(max_trails)):]
        for i in range(0, len(self.prev_p) - step, step):
            colour = self.colour_gen(i)
            pygame.draw.line(screen, colour, self.prev_p[i], self.prev_p[i + step])

    def colour_gen(self, num):
        colour = []
        for i in range(3):
            colour.append(self.colour[i] + (len(self.prev_p) - num) / len(self.prev_p) * (255 - self.colour[i]))
        return list(colour)

    def collision_check(self, dist, body):  # asymmetric at the moment
        if (dist[0] ** 2 + dist[1] ** 2) < (body.rad ** 2 + self.rad ** 2):
            self.vx = (self.m * self.vx + body.m * body.vx) / (self.m + body.m)
            self.vy = (self.m * self.vy + body.m * body.vy) / (self.m + body.m)
            self.px += dist[0] * body.m / (self.m + body.m)
            self.py += dist[1] * body.m / (self.m + body.m)
            self.m += body.m
            self.rad = (self.rad**3 + body.rad**3)**(1/3)
            body_list.remove(body)
            global dt
            dt -= 0.01
            return True


def energy_calc():
    energy = 0
    for i in range(len(body_list)):
        for j in range(i + 1, len(body_list)):
            energy += -1 * G * body_list[i].m * body_list[j].m / (
                    ((body_list[i].px - body_list[j].px) ** 2 + (body_list[i].py - body_list[j].py) ** 2) ** (
                    1 / 2))

    for body in body_list:
        energy += 0.5 * body.m * (body.vx ** 2 + body.vy ** 2)
    return energy


def com_calc():  # center of mass
    total_mass = 0
    com = [0, 0]
    for body in body_list:
        total_mass += body.m
        com[0] += body.m * body.px
        com[1] += body.m * body.py
    com[0] /= total_mass
    com[1] /= total_mass
    return com


# simulations
def first_sim():
    sun = Planet((450, 325), (0, -0.12), 500, 10, BLACK)
    moon = Planet((60, 250), (0, 5.5), 3, 3, BLACK)
    earth = Planet((100, 250), (0, 3.6), 15, 5, BLACK)
    comet = Planet((520, 325), (0, -10), 0.2, 2, BLACK)
    mercury = Planet((580, 325), (0, -5), 2, 4, BLACK)
    return [sun, earth, moon, mercury, comet]


def binary_sunset():
    sun1 = Planet((300, 325), (0, 0), 100, 20, BLACK)
    sun2 = Planet((600, 325), (0, 0), 1000, 20, BLACK)
    return [sun1, sun2]


def elliptic():
    sun = Planet((200, 325), (0, 0), 10000, 10, BLACK)
    comet = Planet((100, 325), (0, 42), 1, 5, BLACK)
    return [sun, comet]


def spam():
    sun = Planet((width/2, height/2), (0, 0), 1250, 30, (255, 255, 0))
    # planet = Planet((200, 400), (0, 7.25), 10, 5, BLACK)
    body_l = [sun]
    n = 80
    for i in range(n):
        orbit_radius = 350 + random.uniform(-1,1) * 250
        velocity = (G * sun.m / orbit_radius) ** 0.5
        mass = 0.5 + random.random()
        bod_radius = 4 + random.random()
        col = (random.random() * 255, random.random() * 255, random.random() * 255)
        angle = math.radians(i * 360 / n)
        body_l.append(Planet((width/2 + orbit_radius * math.sin(angle), height/2 + orbit_radius *
                              math.cos(angle)), (velocity * math.cos(angle), -velocity * math.sin(angle)), mass, bod_radius, col))
    return body_l


def four_body():
    sun1 = Planet((200, 300), (0, 1.55), 50, 10, BLACK)
    sun2 = Planet((600, 300), (0, -1.55), 50, 10, BLACK)
    sun3 = Planet((400, 100), (-1.55, 0), 50, 10, BLACK)
    sun4 = Planet((400, 500), (1.55, 0), 50, 10, BLACK)
    return [sun1, sun2, sun3, sun4]


def figure_eight():
    mass = 20
    sun1 = Planet((450 - 97 * 2, 300 + 24 * 2), (0.466203685, 0.43236573), mass, 5, BLACK)
    sun2 = Planet((450 + 97 * 2, 300 - 24 * 2), (0.466203685, 0.43236573), mass, 5, BLACK)
    sun3 = Planet((450, 300), (-0.93240737, -0.86473146), mass, 5, BLACK)
    return [sun1, sun2, sun3]


def border_of_wave_and_particle():
    velocity = 0.8
    mass = 5
    radius = 200
    body_l = []
    n = 12

    for i in range(n):
        angle = math.radians(i * 360 / n)
        col = tuple(round(i * 255) for i in colorsys.hsv_to_rgb(i / n, 1, 0.7))
        body_l.append(Planet((450 + radius * math.sin(angle), 300 + radius * math.cos(angle)),
                             (velocity * math.cos(angle), -velocity * math.sin(angle)), mass, 3, col))
    return body_l


def jupiter_trojans():
    orbit_radius = 300
    n = 36

    mass = 0.001
    sun = Planet((450, 300), (0, 0), 100000, 12, (255, 255, 0))
    velocity = (G * sun.m / orbit_radius) ** 0.5
    jupiter = Planet((450 + 300, 300), (0, -velocity), 100, 6, (255, 215, 0))
    # print((G*sun.m/radius)**0.5)
    print(velocity)
    period = (orbit_radius ** 3 * 4 * math.pi ** 2 / (G * sun.m)) ** 0.5
    print(((period * 2 / 3) ** 2 * G * sun.m / (4 * math.pi ** 2)) ** (1 / 3))
    body_l = [sun, jupiter]
    for i in range(n):
        if i * 360 / n == 90:
            continue
        if i * 360 / n == 30 or i * 360 / n == 150:
            col = (255, 0, 0)
        else:
            col = BLACK
        angle = math.radians(i * 360 / n)
        body_l.append(Planet((450 + orbit_radius * math.sin(angle), 300 + orbit_radius * math.cos(angle)),
                             (velocity * math.cos(angle), -velocity * math.sin(angle)), mass, 2.5, col))

    return body_l


def jupiter_hilda():
    radius = 255.58
    a = 228.52
    n = 36
    mass = 0.001
    sun = Planet((450, 300), (0, 0), 100000, 12, (255, 255, 0))
    velocity = (G * sun.m * (2 / radius - 1 / a)) ** 0.5

    jupiter = Planet((450 + 300, 300), (0, -57.735026918962575), 100, 6, (255, 215, 0))
    # print((G*sun.m/radius)**0.5)
    print(velocity)
    period = (radius ** 3 * 4 * math.pi ** 2 / (G * sun.m)) ** 0.5
    print(((period * 2 / 3) ** 2 * G * sun.m / (4 * math.pi ** 2)) ** (1 / 3))
    body_l = [sun, jupiter]
    for i in range(n):
        if i * 360 / n == 90:
            continue
        if i * 360 / n == 30 or i * 360 / n == 150:
            col = (255, 0, 0)
        else:
            col = BLACK
        angle = math.radians(i * 360 / n)
        body_l.append(Planet((450 + radius * math.sin(angle), 300 + radius * math.cos(angle)),
                             (velocity * math.cos(angle), -velocity * math.sin(angle)), mass, 2.5, col))

    return body_l


if __name__ == '__main__':
    screen = pygame.display.set_mode(size)
    font = pygame.font.SysFont("calibri", 16)

    # replace with desired simulation
    body_list = spam()

    time_elapsed = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        screen.fill(WHITE)

        for primary_body in body_list:
            primary_body.kick1()
            primary_body.drift()
            primary_body.trails()



        for primary_body in body_list:
            primary_body.kick2()
            primary_body.draw()


        total_energy = energy_calc()
        com_pos = com_calc()
        time_elapsed += dt
        text_time = font.render(f'Elapsed Time: {time_elapsed}', False, (0, 0, 0))
        text_energy = font.render(f'Total Energy (U+K): {total_energy}', False, (0, 0, 0))
        text_com = font.render(f'Center of Mass: {com_pos}', False, (0, 0, 0))
        text_obj = font.render(f'Number of objects: {len(body_list)}', False, (0, 0, 0))
        screen.blit(text_time, (0, 0))
        screen.blit(text_energy, (0, 15))
        screen.blit(text_com, (0, 30))
        screen.blit(text_obj, (0, 45))

        # centerX = 0
        #         # centerY = 0
        #         # for primary_body in body_list:
        #         #     centerX += primary_body.px
        #         #     centerY += primary_body.py
        #         # print(centerX/4, centerY/4)

        pygame.display.flip()
