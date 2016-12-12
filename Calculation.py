__author__ = 'fillan'
from Physics import *
import math


class Calculation:
    view_space = None
    my_physics = None

    def __init__(self, view_space, my_physics):
        self.my_physics = my_physics
        self.view_space = view_space
        self.Total = Quaternion(1, 0, 0, 0)

    def create_total(self, axis_x, axis_y, axis_z, double_rotation):  # 4 doubles
        rotation = double_rotation / 2
        w = math.cos(rotation)
        x = math.sin(rotation) * axis_x
        y = math.sin(rotation) * axis_y
        z = math.sin(rotation) * axis_z
        local = Quaternion(w, x, y, z)
        self.Total.multiply(local)
        self.Total.normalize()
        
    def reset(self):
        self.Total = Quaternion(1, 0, 0, 0)
        
    def rotate(self):  # One point
        rotation_matrix = Matrix(self.Total)
        for i in self.view_space:
            i.Center.multiply(rotation_matrix)
            for j in i.pointList:
                j.multiply(rotation_matrix)
                j.subtract(self.my_physics.velocity)
            i.Center.multiply(rotation_matrix)
            i.Center.subtract(self.my_physics.velocity)
        for i in range(1, len(self.view_space) - 1):  # Bubble Sort
            distance_a = self.view_space[i].calculate_distance()
            distance_b = self.view_space[i + 1].calculate_distance()
            if distance_a < distance_b:
                self.view_space[i], self.view_space[i + 1] = self.view_space[i + 1], self.view_space[i]
        for i in self.view_space:
            i.sort()
        return self.view_space