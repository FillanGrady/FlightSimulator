__author__ = 'fillan'
from Geometry import *
import copy


class Physics:
    velocity = None
    moved_velocity = None
    Engine = 0
    
    def __init__(self, velocity):  # One point
        self.velocity = copy.deepcopy(velocity)
        self.moved_velocity = copy.deepcopy(velocity)
        self.Engine = 0
        
    def update_engine(self, power):
        self.Engine = power
        
    def accelerate(self):
        total_acceleration = (self.Engine - self.moved_velocity.Magnitude() / 10) / 2
        self.velocity.x += self.moved_velocity.x * total_acceleration / 10
        self.velocity.y += self.moved_velocity.y * total_acceleration / 10
        self.velocity.z += self.moved_velocity.z * total_acceleration / 10
        
    def update_camera(self):
        self.accelerate()
        return self.cameraPoint
    
    def calculate_velocity(self):
        return math.sqrt(self.velocity.x * self.velocity.x + self.velocity.y * self.velocity.y + self.velocity.z * self.velocity.z)