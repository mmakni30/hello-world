import pygame
import math
from Area import Area
from pythonProject1.Package import Package

L = [(i, j) for i in range(200) for j in range(360)]


def changement_repere(a, b, angle):
    x = -315 + a
    y = -235 + b
    angle1 = angle
    if angle1 >= 360:
        angle1 = angle1 - 360
    if angle1 <= 0:
        angle1 = 0 - angle1
        if angle1 >= 360:
            angle1 = -360 + angle1
    r = math.sqrt(x ** 2 + y ** 2)
    return r, angle1


class Crane(object):
    """Crane Class"""
    final_id = 0

    def __init__(self, name="G1", pos=(0, 0), sweeping_range=200, displayed=False, background=None, boom=None,
                 hook=None, demand_points=[], counter_jib=None):
        self.name = name
        Crane.final_id += 1
        self.pos = pos
        self.sweeping_range = sweeping_range
        self.displayed = displayed
        self.background = background
        self.boom = boom
        self.hook = hook
        self.demand_points = demand_points
        self.counter_jib = counter_jib
        print(self.name + " crane " + str(Crane.final_id) + " creation completed")

    def init_parts(self):
        self.boom = Boom(pos=(self.pos[0], self.pos[1]), angle=0, length=self.sweeping_range, shape="LINE")
        # self.counter_jib = Boom(pos=(self.pos[0], self.pos[1]), angle=180, length=self.sweeping_range, shape="AREA")
        self.hook = Hook(radius=20, size=10, boom=self.boom, demand_points=self.demand_points)
        self.boom.hook = self.hook

    def display(self, screen):
        self.background = pygame.Surface((2 * self.sweeping_range, 2 * self.sweeping_range), pygame.SRCALPHA)
        self.background.fill(pygame.Color(0, 0, 0, 0))  # fill with transparent color

        # Draw the basis (mast and sweeping range)
        pygame.draw.rect(surface=self.background,
                         color=pygame.Color("black"),
                         rect=(self.sweeping_range - 10, self.sweeping_range - 10, 20, 20))
        pygame.draw.circle(surface=self.background,
                           color=pygame.Color("black"),
                           center=(self.sweeping_range, self.sweeping_range),
                           radius=self.sweeping_range,
                           width=1)

        # Boom
        self.boom.display(screen)
        screen.blit(self.background, (self.pos[0], self.pos[1]))

        # Hook
        self.hook.display(screen)
        screen.blit(self.background, (self.pos[0], self.pos[1]))
        self.displayed = True


class Boom:
    """Boom Class"""

    def __init__(self, name="boom", pos=(0, 0), angle=90, length=200, background=None, shape=None,
                 displayed=None, area=None, hook=None):
        self.name = name
        self.pos = pos
        self.angle = angle
        self.length = length
        self.background = background
        self.shape = shape
        self.displayed = displayed
        self.area = area
        self.hook = hook
        print(self.name + " creation completed")

    def turn_left(self, value):
        self.angle += value
        self.hook.pos = (self.pos[0]
                         + self.length
                         - int(self.hook.size / 2)
                         + self.hook.radius * math.sin(math.radians(self.angle)),
                         self.pos[1]
                         + self.length
                         - int(self.hook.size / 2)
                         + self.hook.radius * math.cos(math.radians(self.angle)))

    def turn_right(self, value):
        self.angle -= value
        self.hook.pos = (self.pos[0]
                         + self.length
                         - int(self.hook.size / 2)
                         + self.hook.radius * math.sin(math.radians(self.angle)),
                         self.pos[1]
                         + self.length
                         - int(self.hook.size / 2)
                         + self.hook.radius * math.cos(math.radians(self.angle)))

    def display(self, screen):
        self.background = pygame.Surface((2 * self.length, 2 * self.length), pygame.SRCALPHA).convert_alpha()
        self.background.fill(pygame.Color(0, 0, 0, 0))  # fill with transparent color

        if self.shape == "LINE":
            pygame.draw.line(surface=self.background,
                             color=pygame.Color("black"),
                             start_pos=(self.length,
                                        self.length),
                             end_pos=(self.length + self.length * math.sin(math.radians(self.angle)),
                                      self.length + self.length * math.cos(math.radians(self.angle))),
                             width=8)

            screen.blit(self.background, (self.pos[0], self.pos[1]))

        elif self.shape == "AREA":
            if self.area is None:
                self.area = Area(name="Boom",
                                 pos=(self.pos[0] + self.length, self.pos[1] + self.length),
                                 angle=self.angle,
                                 width=8,
                                 length=self.length,
                                 color=pygame.Color("black"))
                self.area.init_background()

            self.area.angle = self.angle  # update the angle in the area class

            pygame.draw.polygon(surface=self.background,
                                color=pygame.Color("black"),
                                points=self.area.coordinates_from_side())

            screen.blit(self.background, (self.pos[0], self.pos[1]))


class Hook:
    """Hook Class"""

    def __init__(self, name="hook", radius=0, size=10, background=None, boom=None, package=None,
                 demand_points=[], busy=False):
        self.name = name
        self.radius = radius
        self.boom = boom
        self.angle = self.boom.angle
        self.size = size
        self.background = background
        self.color = pygame.Color("orange")
        self.pos = (self.boom.pos[0]
                    + self.boom.length
                    - int(self.size / 2)
                    + self.radius * math.sin(math.radians(self.boom.angle)),
                    self.boom.pos[1]
                    + self.boom.length
                    - int(self.size / 2)
                    + self.radius * math.cos(math.radians(self.boom.angle)))
        self.pos_init = (self.boom.pos[0]
                         + self.boom.length
                         - int(self.size / 2)
                         + self.radius * math.sin(math.radians(self.boom.angle)),
                         self.boom.pos[1]
                         + self.boom.length
                         - int(self.size / 2)
                         + self.radius * math.cos(math.radians(self.boom.angle)))
        self.package = package
        self.demand_points = demand_points
        self.busy = busy
        print(self.name + " creation completed")

    def move_along_closer(self, value):
        if self.radius >= 20:
            self.radius -= value
        self.pos = (self.boom.pos[0]
                    + self.boom.length
                    - int(self.size / 2)
                    + self.radius * math.sin(math.radians(self.boom.angle)),
                    self.boom.pos[1]
                    + self.boom.length
                    - int(self.size / 2)
                    + self.radius * math.cos(math.radians(self.boom.angle)))
        self.angle = self.boom.angle

    def move_along_further(self, value):
        if self.radius <= (self.boom.length - int(self.size / 2)):
            self.radius += value
        self.pos = (self.boom.pos[0]
                    + self.boom.length
                    - int(self.size / 2)
                    + self.radius * math.sin(math.radians(self.boom.angle)),
                    self.boom.pos[1]
                    + self.boom.length
                    - int(self.size / 2)
                    + self.radius * math.cos(math.radians(self.boom.angle)))
        self.angle = self.boom.angle

    def right_further(self, value):
        self.move_along_further(value)
        self.boom.turn_right(value)

    def right_closer(self, value):
        self.move_along_closer(value)
        self.boom.turn_right(value)

    def left_further(self, value):
        self.move_along_further(value)
        self.boom.turn_left(value)

    def left_closer(self, value):
        self.move_along_closer(value)
        self.boom.turn_left(value)

    def hook_nearby_demand_point(self):
        hook_nearby_demand_point = False
        for d in self.demand_points:
            if d.pos[0] - d.width / 4 <= self.pos[0] <= d.pos[0] + d.width / 4:
                if d.pos[1] - d.length / 4 <= self.pos[1] <= d.pos[1] + d.length / 4:
                    hook_nearby_demand_point = True
        return hook_nearby_demand_point

    def hook_nearby_package(self):
        return self.package.pos[0] - self.package.width / 2 <= self.pos[0] <= \
               self.package.pos[0] + self.package.width / 2 and \
               self.package.pos[1] - self.package.length / 2 <= self.pos[1] \
               <= self.package.pos[1] + self.package.length / 2

    def hook_nearby_target(self, target):
        if isinstance(target, Package):
            return self.hook_nearby_package()
        else:
            self.package.taken = "taken_by_hook"
            return self.hook_nearby_demand_point()

    def display(self, screen):
        self.background = pygame.Surface((2 * self.size, 2 * self.size), pygame.SRCALPHA).convert_alpha()
        self.background.fill(pygame.Color(0, 0, 0, 0))  # fill with transparent color

        pygame.draw.circle(surface=self.background,
                           color=self.color,
                           center=(int(self.size / 2), int(self.size / 2)),
                           radius=int(self.size / 2))

        origin = (self.boom.pos[0]
                  + self.boom.length
                  - int(self.size / 2)
                  + self.radius * math.sin(math.radians(self.boom.angle)),
                  self.boom.pos[1]
                  + self.boom.length
                  - int(self.size / 2)
                  + self.radius * math.cos(math.radians(self.boom.angle)))
        self.pos = origin
        self.angle = self.boom.angle
        screen.blit(self.background, self.pos)

    def is_finished(self):
        return self.hook_nearby_demand_point()

    def step_before_pickup(self, action):
        reward = 0
        distance_init = math.sqrt((self.pos[0] - self.package.pos[0]) ** 2 +
                                  (self.pos[1] - self.package.pos[1]) ** 2)
        if action == 0:
            self.boom.turn_right(value=1)
        elif action == 1:
            self.boom.turn_left(value=1)
        elif action == 2:
            self.move_along_further(value=1)
        elif action == 3:
            self.move_along_closer(value=1)
        elif action == 4:
            self.right_further(value=1)
        elif action == 5:
            self.right_closer(value=1)
        elif action == 6:
            self.left_further(value=1)
        elif action == 7:
            self.left_closer(value=1)

        distance = math.sqrt((self.pos[0] - self.package.pos[0]) ** 2 +
                             (self.pos[1] - self.package.pos[1]) ** 2)

        if self.hook_nearby_package():
            reward += 3
            self.busy = True
            self.package.taken = "taken_by_hook"

        elif distance < distance_init:
            reward += 1
        elif distance > distance_init:
            reward -= 1

        # self.actions = self.action(self.pos)
        return L.index((int(changement_repere(self.pos[0], self.pos[1], self.angle)[0]),
                        int(changement_repere(self.pos[0], self.pos[1], self.angle)[1]))), reward, distance

    def step_after_pickup(self, action):
        self.package.move_package()
        reward = 0
        distance_init = math.sqrt((self.pos[0] - self.demand_points[0].pos[0]) ** 2 +
                                  (self.pos[1] - self.demand_points[0].pos[1]) ** 2)
        if action == 0:
            self.boom.turn_right(value=1)
        elif action == 1:
            self.boom.turn_left(value=1)
        elif action == 2:
            self.move_along_further(value=1)
        elif action == 3:
            self.move_along_closer(value=1)
        elif action == 4:
            self.right_further(value=1)
        elif action == 5:
            self.right_closer(value=1)
        elif action == 6:
            self.left_further(value=1)
        elif action == 7:
            self.left_closer(value=1)

        distance = math.sqrt((self.pos[0] - self.demand_points[0].pos[0]) ** 2 +
                             (self.pos[1] - self.demand_points[0].pos[1]) ** 2)

        if self.hook_nearby_demand_point():
            reward += 3

        elif distance < distance_init:
            reward += 1
        elif distance > distance_init:
            reward -= 1
        # self.actions = self.action(self.pos)

        return L.index((int(changement_repere(self.pos[0], self.pos[1], self.angle)[0]),
                        int(changement_repere(self.pos[0], self.pos[1], self.angle)[1]))) + 72000, reward, distance

    def step(self, action):
        if not self.busy:
            return self.step_before_pickup(action)
        else:
            return self.step_after_pickup(action)
