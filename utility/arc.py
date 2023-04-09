from common.reference_frame import *
from pygame_functions import drawArc
import pygame
import math

"""
The Arc class represents an arc or a straight line segment in Pygame.
It provides an easy way to create, modify, and draw arcs with specified
start and end points, curvature, and other properties. The class
automatically handles the straight line edge case without dealing
with infinity or division by zero errors. The Arc class also allows
users to set a new theta angle for an arc, updating the other angle
while maintaining the positions of the start and end points. When
the arc is a straight line, the set_theta method converts the line
back into an arc based on the provided theta angle.
"""
class Arc:
    def __init__(self, start, end, curvature=None):

        self.MIN_CURVATURE = 1e-4

        self.start = start
        self.end = end
        self.curvature = curvature
        self.calculate_arc_properties()

    def calculate_arc_properties(self):
        dx = self.end[0] - self.start[0]
        dy = self.end[1] - self.start[1]
        distance = math.sqrt(dx*dx + dy*dy)

        # The arc can never be a straight line. Force some curvature.
        if self.curvature >= 0 and self.curvature < self.MIN_CURVATURE:
            self.curvature = self.MIN_CURVATURE
        elif self.curve < 0 and self.curve > -self.MIN_CURVATURE:
            self.curvature = -self.MIN_CURVATURE

        self.radius = distance / (2 * self.curvature)
        self.center = self.calculate_center()
        self.angle_start, self.angle_end = self.calculate_angles()

    def calculate_center(self):
        mid_point = ((self.start[0] + self.end[0]) / 2, (self.start[1] + self.end[1]) / 2)
        dx = self.end[0] - self.start[0]
        dy = self.end[1] - self.start[1]
        distance = math.sqrt(dx*dx + dy*dy)
        direction = (dy / distance, -dx / distance)

        center_x = mid_point[0] + direction[0] * self.radius
        center_y = mid_point[1] + direction[1] * self.radius
        return center_x, center_y

    def calculate_angles(self):
        angle_start = math.atan2(self.start[1] - self.center[1], self.start[0] - self.center[0])
        angle_end = math.atan2(self.end[1] - self.center[1], self.end[0] - self.center[0])
        return angle_start, angle_end

    def draw(self, screen, color, width):
        center = PointRef(self.center).screenRef
        radius = ScalarRef(self.radius).screenRef
        drawArc(screen, color, center, radius, self.angle_start, self.angle_end, width, True)