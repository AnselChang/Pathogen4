import numpy as np
from scipy.integrate import quad
from scipy.optimize import root_scalar, brentq
from utility.math_functions import distanceTuples

def cubic_bezier_point(t, p0, p1, p2, p3):
    t_inv = 1 - t
    return (t_inv ** 3) * p0 + 3 * (t_inv ** 2) * t * p1 + 3 * t_inv * (t ** 2) * p2 + (t ** 3) * p3

def cubic_bezier_derivative(t, p0, p1, p2, p3):
    t_inv = 1 - t
    return -3 * (t_inv ** 2) * p0 + 3 * (t_inv ** 2) * p1 - 6 * t_inv * t * p1 + 6 * t_inv * t * p2 - 3 * (t ** 2) * p2 + 3 * (t ** 2) * p3

def arc_length_integrand(t, p0, p1, p2, p3):
    derivative = cubic_bezier_derivative(t, p0, p1, p2, p3)
    return np.linalg.norm(derivative)

def arc_length(t, p0, p1, p2, p3):
    return quad(arc_length_integrand, 0, t, args=(p0, p1, p2, p3))[0]

def find_t_for_arc_length(target_arc_length, p0, p1, p2, p3):
    def target_function(t):
        return arc_length(t, p0, p1, p2, p3) - target_arc_length

    try:
        result = brentq(target_function, 0, 1)
    except ValueError:
        result = 1.0

    return result

def normalized_points_cubic_bezier(segment_length, p0, p1, p2, p3):

    end = p3
    p0, p1, p2, p3 = map(np.array, [p0, p1, p2, p3])

    points = [p0]
    t = 0

    while True:
        current_arc_length = arc_length(t, p0, p1, p2, p3)
        target_arc_length = current_arc_length + segment_length
        t = find_t_for_arc_length(target_arc_length, p0, p1, p2, p3)

        if t >= 1:
            points.append(end)
            return points

        point = cubic_bezier_point(t, p0, p1, p2, p3)
        points.append(point.tolist())

    
# Evenly-spaced values of t. Segments may not be equidistant
def fast_points_cubic_bezier(RESOLUTION, p0, p1, p2, p3):

    # use approximate distance to calculate how many points to calculate
    approximateDistance = distanceTuples(p0, p1)
    approximateDistance += distanceTuples(p1, p2)
    approximateDistance += distanceTuples(p2, p3)
    N = int(approximateDistance * RESOLUTION) # number of points

    p0, p1, p2, p3 = map(np.array, [p0, p1, p2, p3])

    points = []
    for i in range(N):
        t = i / (N-1)
        point = cubic_bezier_point(t, p0, p1, p2, p3)
        points.append(point.tolist())

    return points