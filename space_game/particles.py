import pygame as pg

from random import choice, randint
from time import time

from config import screen, HP


class ParticleSystem:
    def __init__(self, size=1, direction_y=1, max_speed_x=1, max_speed_y=3, color=HP):
        self.size= size
        self.direction_y = direction_y
        self.max_speed_x = max_speed_x
        self.max_speed_y = max_speed_y
        self.color = color

        self.particles = []

    def create_particle(self, x, y) -> list:
        direction_x = choice([-1, 1])
        speed_x = randint(0, self.max_speed_x)
        speed_y = randint(1, self.max_speed_y)
        beginning_life = time()

        return [[x, y], [speed_x * direction_x, speed_y * self.direction_y], beginning_life]

    def add_particles(self, x, y):
        if len(self.particles) < 600:

            self.particles += [self.create_particle(x, y) for _ in range(10)]

    def delete_particles(self):
        self.particles = [pt for pt in self.particles if time() - pt[2] < 0.1]

    def update(self):
        if self.particles:
            self.delete_particles()
            for pt in self.particles:
                pt[0][0] += pt[1][0]
                pt[0][1] += pt[1][1]
                pg.draw.rect(screen, self.color, (pt[0][0], pt[0][1], self.size, self.size))
