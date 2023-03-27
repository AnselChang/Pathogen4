import math

# Whether (x,y) is inside the rectangle described by (x1,y1) and (x2,y2)
def isInsideBox(x, y, x1, y1, x2, y2):
    x_min, x_max = min(x1, x2), max(x1, x2)
    y_min, y_max = min(y1, y2), max(y1, y2)
    return x_min <= x <= x_max and y_min <= y <= y_max

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