import math

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

def hypo(s1, s2):
    return math.sqrt(s1*s1 + s2*s2)

def distance(x1,y1,x2,y2):
    return hypo(y2-y1, x2-x1)

# Distance between point (x, y) and line (x1, y1,),(x2,y2)
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