from gym import Env, spaces
from ConstructionSite import ConstructionSite
from Crane import Crane
from Area import Area
from Logistics import Road, Truck
from Package import Package
import pygame
import math

L1 = [(i, j) for i in range(200) for j in range(360)]


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


class Construction(Env):
    def __init__(self, screen_length=640, screen_width=480, construction_site_name="Centrale Lille",
                 construction_site_location="Villeneuve d'Ascq",
                 delivery_area_pos=(160, 240), delivery_area_width=40, delivery_area_length=70,
                 building_area_pos=(430, 240), building_area_width=100, building_area_length=160,
                 storage_area_pos=(320, 350), storage_area_width=40, storage_area_length=80,
                 storage_angle=90, crane_pos=(120, 40), crane_sweeping_range=200,
                 road_pos=((200, 0), (180, 10), (160, 40), (160, 240), (160, 300), (200, 400), (300, 480)),
                 package_width=20, package_length=20):
        self.screen_length = screen_length
        self.screen_width = screen_width
        self.construction_site_name = construction_site_name
        self.construction_site_location = construction_site_location
        self.delivery_area_name = "Delivery"
        self.delivery_area_pos = delivery_area_pos
        self.delivery_area_width = delivery_area_width
        self.delivery_area_length = delivery_area_length
        self.building_area_name = "Building"
        self.building_area_pos = building_area_pos
        self.building_area_width = building_area_width
        self.building_area_length = building_area_length
        self.storage_area_name = "Storage"
        self.storage_area_pos = storage_area_pos
        self.storage_area_width = storage_area_width
        self.storage_area_length = storage_area_length
        self.storage_angle = storage_angle
        self.crane_pos = crane_pos
        self.crane_sweeping_range = crane_sweeping_range
        self.road_pos = road_pos
        self.package_name = "Prefab wall"
        self.package_width = package_width
        self.package_length = package_length
        self.action_space = spaces.Discrete(8)
        self.observation_space = spaces.Discrete(200 * 360 * 3)

    def step(self, action):
        return self.crane.hook.step(action)

    def reset(self):
        self.construction_site = ConstructionSite(name=self.construction_site_name,
                                                  location=self.construction_site_location)
        self.delivery_area = Area(name=self.delivery_area_name, pos=self.delivery_area_pos,
                                  width=self.delivery_area_width,
                                  length=self.delivery_area_length)
        self.building_area = Area(name=self.building_area_name, pos=self.building_area_pos,
                                  width=self.building_area_width,
                                  length=self.building_area_length)
        self.storage_area = Area(name=self.storage_area_name, pos=self.storage_area_pos, angle=self.storage_angle,
                                 width=self.storage_area_width, length=self.storage_area_length)
        self.demand_points = [self.building_area]
        self.construction_site.add_area([self.delivery_area, self.building_area, self.storage_area])
        self.crane = Crane(pos=self.crane_pos, sweeping_range=self.crane_sweeping_range,
                           demand_points=self.demand_points)
        self.crane.init_parts()
        self.construction_site.add_crane([self.crane])
        self.access_road = Road(pos=self.road_pos)
        self.access_road.calculate_length()
        self.truck = Truck(road=self.access_road)
        self.package1 = Package(name=self.package_name, width=self.package_width, length=self.package_length,
                                crane=self.crane, truck=self.truck)
        self.crane.hook.package = self.package1
        self.packages = [self.package1]
        self.construction_site.add_package(self.packages)

        return L1.index((int(changement_repere(self.crane.hook.pos[0], self.crane.hook.pos[1],
                                               self.crane.hook.angle)[0]),
                         (int(changement_repere(self.crane.hook.pos[0], self.crane.hook.pos[1],
                                                self.crane.hook.angle)[1]))))

    def render(self, window):
        window.fill(pygame.Color("grey"))  # Fills the screen with black
        self.construction_site.display(screen=window)
        self.access_road.display(screen=window)
        self.truck.display(screen=window)
        self.truck.deliver(delivery=self.delivery_area, screen=window)

        pygame.display.flip()
        pygame.display.update()
