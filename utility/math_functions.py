import math, pygame

# Whether (x,y) is inside the rectangle described by (x1,y1) and (x2,y2)
def isInsideBox(x, y, x1, y1, x2, y2):
    x_min, x_max = min(x1, x2), max(x1, x2)
    y_min, y_max = min(y1, y2), max(y1, y2)
    return x_min <= x <= x_max and y_min <= y <= y_max

# Whether (x,y) is inside rectangle defined by x, y, width height
def isInsideBox2(x, y, topLeftX, topLeftY, width, height):
    return isInsideBox(x, y, topLeftX, topLeftY, topLeftX + width, topLeftY + height)

# Clamp a value between a minimum and a maximum value.
def clamp(value, minValue, maxValue):
    return max(min(value, maxValue), minValue)

def addTuples(tupleA: tuple, tupleB: tuple):
    assert len(tupleA) == len(tupleB)
    return [a+b for a,b in zip(tupleA, tupleB)]

def subtractTuples(tupleA: tuple, tupleB: tuple):
    assert len(tupleA) == len(tupleB)
    return [a-b for a,b in zip(tupleA, tupleB)]

def scaleTuple(nums: tuple, scalar: float):
    return [i * scalar for i in nums]

def divideTuple(nums: tuple, scalar: float):
    return [i / scalar for i in nums]

def clampTuple(nums: tuple, min: float, max: float):
    return [clamp(i, min, max) for i in nums]

def intTuple(nums: tuple):
    return [int(i) for i in nums]

def hypo(s1, s2):
    return math.sqrt(s1*s1 + s2*s2)

def distance(x1,y1,x2,y2):
    return hypo(y2-y1, x2-x1)

def distanceTuples(point1, point2):
    return distance(*point1, *point2)

def midpoint(point1: tuple, point2: tuple):
    return divideTuple(addTuples(point1, point2), 2)

def vectorFromThetaAndMagnitude(theta: float, magnitude: float):
    return [magnitude * math.cos(theta), magnitude * math.sin(theta)]

# Distance between point (x, y) and line (x1, y1),(x2,y2)
def distancePointToLine(x, y, x1, y1, x2, y2, signed: bool = False):
    ans = ((x2-x1)*(y1-y) - (x1-x)*(y2-y1)) / distance(x1, y1, x2, y2)
    if signed:
        return ans
    else:
        return abs(ans)

# Whether point is touching the line with some margin given by lineHitboxThickness
def pointTouchingLine(mouseX: int, mouseY: int, x1: int, y1: int, x2: int, y2: int, lineHitboxThickness: int) -> bool:

    if x1 == x2 and y1 == y2:
        return False
    
    if distancePointToLine(mouseX,mouseY, x1, y1, x2, y2) <= lineHitboxThickness:
        dist = distance(x1, y1, x2, y2)
        if distance(mouseX, mouseY, x1, y1) < dist and distance(mouseX, mouseY, x2, y2) < dist:
            return True
    return False

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

# If parity == true, must return negative. if parity == false, must return positive.
def deltaInHeadingParity(targetHeading: float, currentHeading: float, parity: bool) -> float:
    diff = (targetHeading - currentHeading) % (3.1415*2)
    if parity and diff > 0:
        diff -= 3.1415*2
    elif not parity and diff < 0:
        diff += 3.1415*2
    return diff

def thetaFromPoints(p1, p2):
    return math.atan2(p2[1] - p1[1], p2[0] - p1[0])

# return point given by point + vector (defined by magnitude and angle)
def pointPlusVector(point: tuple, magnitude: float, angle: float) -> tuple:
    return (point[0] + magnitude * math.cos(angle), point[1] + magnitude * math.sin(angle))

# Vector projection algorithm
def pointOnLineClosestToPoint(pointX: int, pointY: int, firstX: int, firstY: int, secondX: int, secondY: int) -> tuple:
    ax = pointX - firstX
    ay = pointY - firstY
    bx = secondX - firstX
    by = secondY - firstY

    scalar = (ax * bx + ay * by) / (bx * bx + by * by)
    return [firstX + scalar * bx, firstY + scalar * by]

def clipLineToBox(point: tuple, theta: float, boxX, boxY, boxWidth, boxHeight): # returns start and end line

    line_start = point
    line_length = max(boxWidth, boxHeight) * 1.42
    line_theta = theta

    # calculate the end point of the line
    line_end_x = line_start[0] + line_length * math.cos(line_theta)
    line_end_y = line_start[1] + line_length * math.sin(line_theta)
    line_end = (line_end_x, line_end_y)

    rect = pygame.Rect(boxX, boxY, boxWidth, boxHeight)

    # clip the line so that it does not go past the screen
    line_rect = pygame.Rect(line_start, (line_length, 1))
    if not line_rect.colliderect(rect):
        # calculate the intersection points of the line with the edges of the screen
        intersections = []
        for edge in rect.inflate(-line_length, -line_length).as_lines():
            intersection_point = line_rect.clipline(edge)
            if intersection_point:
                intersections.append(intersection_point)
        if intersections:
            # clip the line to the closest intersection point
            line_end = min(intersections, key=lambda p: math.hypot(line_start[0] - p[0], line_start[1] - p[1]))

    return line_start, line_end

# returns center, radius given three consecutive points
def arcFromThreePoints(p1, p2, p3):
    d = 2 * (p1[0] * (p2[1] - p3[1]) + p2[0] * (p3[1] - p1[1]) + p3[0] * (p1[1] - p2[1]))
    if d == 0:  # The points are collinear
        return None, None

    center_x = (
        (p1[0] ** 2 + p1[1] ** 2) * (p2[1] - p3[1])
        + (p2[0] ** 2 + p2[1] ** 2) * (p3[1] - p1[1])
        + (p3[0] ** 2 + p3[1] ** 2) * (p1[1] - p2[1])
    ) / d
    center_y = (
        (p1[0] ** 2 + p1[1] ** 2) * (p3[0] - p2[0])
        + (p2[0] ** 2 + p2[1] ** 2) * (p1[0] - p3[0])
        + (p3[0] ** 2 + p3[1] ** 2) * (p2[0] - p1[0])
    ) / d
    radius = math.sqrt((center_x - p1[0]) ** 2 + (center_y - p1[1]) ** 2)

    return (center_x, center_y), radius

# Given (x1,y1), (x2,y2), and the heading of (x1,y1), find the center of the /arc
def arcCenterFromTwoPointsAndTheta(x1, y1, x2, y2, theta) -> tuple:

    a = (x1 - x2) * math.cos(theta) + (y1 - y2) * math.sin(theta)
    b = (y1 - y2) * math.cos(theta) - (x1 - x2) * math.sin(theta)
    c = a / (2 * b)
    

    x = (x1+x2)/2 + c * (y1 - y2)
    y = (y1+y2)/2 + c * (x2 - x1)

    return x,y

# Given (x1,y1) and (x2,y2) and a radius to define an arc,
# return the two possible midpoints
def getArcMidpoint(x1, y1, x2, y2, r) -> tuple[tuple]:

    # mx is either positive or negative
    mx1 = r * (x1 + x2) / math.sqrt((x1+x2)**2 + (y1+y2)**2)
    mx2 = -mx1

    def myFromMx(mx):
        return mx * (y1 + y2) / (x1 + x2)
    
    my1 = myFromMx(mx1)
    my2 = myFromMx(mx2)

    return (mx1, my1), (mx2, my2)


# Given an initial theta and an offset x and y, calculate the final theta
# if (0,0) and (x,y) were two points of an arc with the initial theta
def thetaFromArc(theta1: float, dx: float, dy: float) -> float:
    return (2 * math.atan2(dy, dx) - theta1) % (3.1415*2)

def thetaFromVector(vector: tuple):
    return math.atan2(vector[1], vector[0])