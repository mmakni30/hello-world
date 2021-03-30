import numpy as np


class ConstructionSite(object):

    def __init__(self, name, location, width=640, height=480):
        self.name = name
        self.location = location
        self.areas = []
        self.cranes = []
        self.packages = []
        self.width = width  # la largeur de notre construction site in pixel
        self.height = height  # la longuer de notre construction site in pixel
        self.body = np.zeros(shape=(self.height, self.width))

    def add_area(self, area):
        for a in area:
            self.areas.append(a)

    def add_crane(self, crane):
        for c in crane:
            self.cranes.append(c)

    def add_package(self, package):
        for o in package:
            self.packages.append(o)

    def update_field(self):
        try:
            self.body = np.zeros(shape=(self.height, self.width))
            for a in self.areas:
                self.body[a.pos[0] - a.length / 2:a.pos[0] + a.length / 2,
                a.pos[1] - a.width / 2:a.pos[1] + a.width / 2] = a.body

            for c in self.cranes:
                self.body[c.hook.pos[0] - c.hook.size / 2:c.hook.pos[0] + c.hook.size / 2,
                c.hook.pos[1] - c.hook.size / 2:c.hook.pos[1] + c.hook.size] = c.body

            for o in self.packages:
                self.body[o.pos[0] - o.length / 2:o.pos[0] + o.length / 2,
                o.pos[1] - o.width / 2:o.pos[1] + o.width / 2] = o.hook.body
        except:
            pass

    def display(self, screen):

        for area in self.areas:
            area.display_from_center(screen)

        for crane in self.cranes:
            crane.display(screen)

        for package in self.packages:
            package.display_from_center(screen)
