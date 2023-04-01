import math

class Line:
    def __init__(self, point: tuple, theta):
        self.point = point
        self.theta = theta
        
    def intersection(self, other: 'Line') -> tuple:
        x1, y1 = self.point
        x2, y2 = other.point
        theta1 = self.theta
        theta2 = other.theta
        
        # Check if the lines are parallel
        if abs(theta1 - theta2) < 1e-6:
            return None
        
        # Calculate the intersection point
        x = (y2 - y1 + math.tan(theta1) * x1 - math.tan(theta2) * x2) / (math.tan(theta1) - math.tan(theta2))
        y = y1 + math.tan(theta1) * (x - x1)
        
        return x, y
    
    def closestPoint(self, point: tuple):
        x0, y0 = point
        x1, y1 = self.point
        theta = self.theta
        
        # Calculate the point on the line closest to the given point
        x = (x0 + math.tan(theta) * (y1 - y0) + math.cos(theta) * x1) / (math.tan(theta)**2 + 1)
        y = y1 + math.tan(theta) * (x - x1)
        
        return x, y
