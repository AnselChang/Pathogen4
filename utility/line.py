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
        line1 = [self.p1, self.p2]
        line2 = [other.p1, other.p2]
        
        xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
        ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

        def det(a, b):
            return a[0] * b[1] - a[1] * b[0]

        div = det(xdiff, ydiff)
        if div == 0:
            raise Exception('lines do not intersect')

        d = (det(*line1), det(*line2))
        x = det(d, xdiff) / div
        y = det(d, ydiff) / div
        return x, y

    
    def closestPoint(self, point: tuple):
        x0, y0 = point
        x1, y1 = self.p1
        x2, y2 = x1 + math.cos(self.theta), y1 + math.sin(self.theta)
        return pointOnLineClosestToPoint(x0, y0, x1, y1, x2, y2)