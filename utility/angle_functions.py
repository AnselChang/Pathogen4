# Bound angle to between -pi and pi, preferring the smaller magnitude
import math

class Direction:
    EAST = 0
    NORTH = math.pi / 2
    WEST = math.pi
    SOUTH = 3 * math.pi / 2

def boundAngleRadians(angle: float) -> float:
    PI = 3.1415
    angle %= 2 * PI
    if angle < -PI:
        angle += 2*PI
    if angle > PI:
        angle -= 2*PI
    return angle
    
# Find the closest angle between two universal angles
def deltaInHeading(targetHeading: float, currentHeading: float) -> float:
    return boundAngleRadians(targetHeading - currentHeading)

def headingDiff(headingA: float, headingB: float):
    return abs(deltaInHeading(headingA, headingB))

def headingDiff180(headingA: float, headingB: float):
    diff1 = headingDiff(headingA, headingB)
    diff2 = headingDiff(headingA, headingB + math.pi)
    return diff1 if diff1 < diff2 else diff2

def parallelTheta(theta1, theta2, tolerance = 1e-3) -> bool:

    if headingDiff(theta1, theta2) < tolerance:
        return True
    if headingDiff(theta1, theta2 + math.pi) < tolerance:
        return True
    return False

def equalTheta(theta1, theta2, tolerance = 1e-3) -> bool:
    return headingDiff(theta1, theta2) < tolerance

def equalTheta180(theta1, theta2, tolerance = 1e-3) -> bool:
    return equalTheta(theta1, theta2, tolerance) or equalTheta(theta1, theta2 + math.pi, tolerance)