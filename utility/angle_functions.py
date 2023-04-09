# Bound angle to between -pi and pi, preferring the smaller magnitude
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

def headingsEqual(headingA: float, headingB: float) -> bool:
    return abs(deltaInHeading(headingA, headingB)) < 0.001
