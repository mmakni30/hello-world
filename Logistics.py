import pygame
import math
import numpy
import time

from Area import Area


class Road(object):
    """Road Class"""

    def __init__(self, pos, way="THROUGH", dist=None, background=None):
        self.pos = pos
        self.way = way
        self.background = background
        self.dist = dist
        self.color = pygame.Color("dark orange")

    def calculate_length(self):
        if self.dist is None:
            self.dist = []
            for r in range(0, len(self.pos) - 1, 1):
                self.dist.append(int(math.dist(self.pos[r], self.pos[r + 1])))

    def display(self, screen):
        (w, h) = screen.get_size()
        self.background = pygame.Surface((w, h), pygame.SRCALPHA).convert_alpha()
        self.background.fill(pygame.Color(0, 0, 0, 0))  # fill with transparent color

        pygame.draw.lines(surface=self.background,
                          color=self.color,
                          closed=False,
                          points=self.pos,
                          width=10)

        screen.blit(self.background, (0, 0))


class Truck(object):
    """Truck Class"""

    # les attribus: pos: qui indique la position du camion utile pour la position de la grue,
    # busy:"True":le camion porte toujours des objets,
    #       "false":il ne porte plus d'objet donc il est libre de se déplacer

    def __init__(self, length=50, width=20, road=None, shape=None, track=0, vel=5,
                 busy=True, waiting_time=0, pos=(0, 0), arrived=False):
        self.length = length
        self.width = width
        self.road = road
        self.shape = shape
        self.track = track
        self.vel = vel
        self.busy = busy
        self.waiting_time = waiting_time
        self.first_stop = waiting_time
        self.pos = pos
        self.arrived = arrived

    def road_part(self):
        cum_dist = numpy.cumsum(self.road.dist)
        cum_dist = numpy.insert(arr=cum_dist, obj=0, values=0)

        for i in range(0, len(cum_dist) - 1, 1):
            if cum_dist[i] <= self.track < cum_dist[i + 1]:
                return i, cum_dist[i]

    def pos_on_road(self):
        rp = self.road_part()
        ind = rp[0]
        dist = rp[1]
        alpha = math.atan2(self.road.pos[ind + 1][1] - self.road.pos[ind][1],
                           self.road.pos[ind + 1][0] - self.road.pos[ind][0])
        pos = (self.road.pos[ind][0] + (self.track - dist) * math.cos(alpha),
               self.road.pos[ind][1] + (self.track - dist) * math.sin(alpha))
        if not self.arrived:
            self.pos = pos
        # print("truck position "+ str(self.pos))
        return pos, alpha - math.pi / 2

    def move_along(self, direction):
        if direction == "forward" and self.track < sum(self.road.dist) - self.vel:
            self.track += self.vel

        if direction == "backward" and self.track > self.vel:
            self.track -= self.vel

    def move_to(self, delivery, screen):
        if delivery.is_completely_inside(truck=self, screen=screen) is False:
            self.move_along("forward")
            return False
        else:
            self.vel = 0
            self.arrived = True
            self.pos = delivery.pos
            return True

    def calculate_waiting_time(self):
        if self.vel == 0:
            if self.waiting_time == 0:
                self.first_stop = time.time()
                self.waiting_time = 10 ** -8
            else:
                self.waiting_time = time.time() - self.first_stop

    def deliver(self, delivery, screen):
        if self.move_to(delivery=delivery, screen=screen):
            self.calculate_waiting_time()
            if not self.busy:
                if self.waiting_time >= 5:
                    self.vel = 5
                    self.move_along("forward")

    def display(self, screen):
        if self.shape is None:
            self.shape = Area(name="Truck",
                              pos=self.road.pos[0],
                              angle=-90,
                              width=self.width,
                              length=self.length)
            self.shape.set_color()

        self.shape.pos = self.pos_on_road()[0]
        self.shape.angle = math.degrees(self.pos_on_road()[1])
        self.shape.display_from_center(screen)
