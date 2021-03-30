import pygame
import math
from shapely.geometry import Polygon


def rotate(coord, deg):
    """Only rotate a point around the origin (0, 0)."""
    [x, y] = [coord[0], coord[1]]
    xx = x * math.cos(math.radians(deg)) - y * math.sin(math.radians(deg))
    yy = x * math.sin(math.radians(deg)) + y * math.cos(math.radians(deg))

    return [xx, yy]


def offset(coord, offset_coord):
    return [coord[0] + offset_coord[0], coord[1] + offset_coord[1]]


class Area(object):
    """Area Class"""

    def __init__(self, name="test", pos=(20, 20), angle=0, width=30, length=30, color=None,
                 shape=None, displayed=False, background=None):
        self.name = name
        self.pos = pos
        self.angle = angle
        self.width = width
        self.length = length
        self.color = color
        self.shape = shape
        self.displayed = displayed
        self.background = background
        print(self.name + " area creation completed")

    def is_inside(self, truck, screen):
        area = Polygon(self.coordinates_in_world())
        truck_area = Polygon(truck.shape.coordinates_in_world())
        result = area.intersection(truck_area)

        bg = pygame.Surface((2*self.length, 2*self.length), pygame.SRCALPHA).convert_alpha()
        bg.fill(pygame.Color(0, 0, 0, 0))

        if result.area != 0.0 and result.geom_type == 'Polygon':
            world_coords = result.exterior.coords[:-1]
            local_coords = []

            for i in world_coords:
                new = list(i)
                new[0] = new[0] - self.pos[0] + self.length
                new[1] = new[1] - self.pos[1] + self.length
                local_coords.append(new)

            pygame.draw.polygon(surface=bg,
                                color=pygame.Color("black"),
                                points=local_coords)

        screen.blit(bg, (self.pos[0] - self.length, self.pos[1] - self.length))

        return truck_area.area-result.area

    def is_completely_inside(self, truck, screen):
        if self.is_inside(truck=truck, screen=screen) <= 0.02:
            return True
        else:
            return False

    def init_background(self):
        self.background = pygame.Surface((2*self.length, 2*self.length), pygame.SRCALPHA).convert_alpha()
        self.background.fill(pygame.Color(0, 0, 0, 0))  # fill with transparent color

    def coordinates_in_world(self):
        cfc = self.coordinates_from_center()
        for i in cfc:
            i[0] = i[0] + self.pos[0] - self.length
            i[1] = i[1] + self.pos[1] - self.length
        return cfc

    def coordinates_from_center(self):
        top_left_corner = [-self.width/2, -self.length/2]
        top_right_corner = [self.width/2, -self.length/2]
        bottom_left_corner = [-self.width/2, self.length/2]
        bottom_right_corner = [self.width/2, self.length/2]

        rotated_top_left_corner = rotate(top_left_corner, self.angle)
        rotated_top_right_corner = rotate(top_right_corner, self.angle)
        rotated_bottom_left_corner = rotate(bottom_left_corner, self.angle)
        rotated_bottom_right_corner = rotate(bottom_right_corner, self.angle)

        return [offset(rotated_top_left_corner, [self.length, self.length]),
                offset(rotated_top_right_corner, [self.length, self.length]),
                offset(rotated_bottom_right_corner, [self.length, self.length]),
                offset(rotated_bottom_left_corner, [self.length, self.length])]

    def coordinates_from_side(self):
        top_left_corner = [-self.width/2, 0]
        top_right_corner = [self.width/2, 0]
        bottom_left_corner = [-self.width/2, self.length]
        bottom_right_corner = [self.width/2, self.length]

        rotated_top_left_corner = rotate(top_left_corner, -self.angle)
        rotated_top_right_corner = rotate(top_right_corner, -self.angle)
        rotated_bottom_left_corner = rotate(bottom_left_corner, -self.angle)
        rotated_bottom_right_corner = rotate(bottom_right_corner, -self.angle)

        return [offset(rotated_top_left_corner, [self.length, self.length]),
                offset(rotated_top_right_corner, [self.length, self.length]),
                offset(rotated_bottom_right_corner, [self.length, self.length]),
                offset(rotated_bottom_left_corner, [self.length, self.length])]

    def set_color(self):
        if self.name == "Delivery":
            self.color = pygame.Color("green4")
        if self.name == "Access":
            self.color = pygame.Color("yellow")
        if self.name == "Building":
            self.color = pygame.Color("red")
        if self.name == "Storage":
            self.color = pygame.Color("blue")
        if self.name == "Truck":
            self.color = pygame.Color("darkviolet")

    def display_from_center(self, screen):
        if self.color is None:
            self.set_color()

        self.init_background()

        pygame.draw.polygon(surface=self.background,
                            color=self.color,
                            points=self.coordinates_from_center())

        screen.blit(self.background, (self.pos[0] - self.length, self.pos[1] - self.length))
