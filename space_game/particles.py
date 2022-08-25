import pygame as pg
from random import choice, randint
from time import time

from config import screen, HP


class ParticleSystem:
    def __init__(self, h=1, direction_y=1, max_speed_x=1, max_speed_y=3, color=HP):
        self.h = h
        self.direction_y = direction_y
        self.max_speed_x = max_speed_x
        self.max_speed_y = max_speed_y
        self.color = color

        self.particles = []

    def create_particle(self, x, y):
        direction_x = choice([-1, 1])
        speed_x = randint(0, self.max_speed_x)
        speed_y = randint(1, self.max_speed_y)
        beginning_life = time()

        return [[x, y], [speed_x * direction_x, speed_y * self.direction_y], beginning_life]

    def add_particles(self, x, y):
        if len(self.particles) < 600:

            self.particles += [self.create_particle(x, y), self.create_particle(x, y), self.create_particle(x, y),
                               self.create_particle(x, y), self.create_particle(x, y), self.create_particle(x, y)]

    def delete_particles(self):
        self.particles = [particle for particle in self.particles if time() - particle[2] < 0.1]

    def update(self):
        if self.particles:
            self.delete_particles()
            for particle in self.particles:
                particle[0][0] += particle[1][0]
                particle[0][1] += particle[1][1]
                pg.draw.rect(screen, self.color, (particle[0][0], particle[0][1], self.h, self.h))
