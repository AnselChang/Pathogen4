from utility.math_functions import deltaInHeading, pointOnLineClosestToPoint
import math

class Line:
    def __init__(self, point: tuple, theta = None, point2: tuple = None):
        self.p1 = point

        if theta is None:
            self.p2 = point2
            self.theta = math.atan2(self.p2[1] - self.p1[1], self.p2[0] - self.p1[0])
        else:
            self.p2 = (self.p1[0] + math.cos(theta), self.p1[1] + math.sin(theta))
            self.theta = theta
        
    def intersection(self, other: 'Line') -> tuple:
        x1, y1 = self.p1
        x2, y2 = other.p1
        theta1 = self.theta
        theta2 = other.theta
        
        # Check if the lines are parallel
        if abs(deltaInHeading(theta1, theta2)) < 1e-6:
            return None
        
        # Calculate the intersection point
        x = (y2 - y1 + math.tan(theta1) * x1 - math.tan(theta2) * x2) / (math.tan(theta1) - math.tan(theta2))
        y = y1 + math.tan(theta1) * (x - x1)
        
        return x, y
    
    def closestPoint(self, point: tuple):
        x0, y0 = point
        x1, y1 = self.p1
        x2, y2 = x1 + math.cos(self.theta), y1 + math.sin(self.theta)
        return pointOnLineClosestToPoint(x0, y0, x1, y1, x2, y2)