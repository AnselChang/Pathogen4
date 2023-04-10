from utility.math_functions import distanceTuples, hypo

def lerp(p1, p2, t):
    return (p1[0] + t * (p2[0] - p1[0]), p1[1] + t * (p2[1] - p1[1]))

# Generate list of points fo quadratic bezier curve
# this is NOT equally-spaced points
# given how long each segment should be in pixels (approximately)
def generate_quadratic_points(p1, p2, p3, segment_length):
    points = []
    total_length = distanceTuples(p1, p2) + distanceTuples(p2, p3)
    num_segments = int(total_length / segment_length)
    if num_segments == 0:
        return [p1, p3]

    increment = 1.0 / num_segments

    for i in range(num_segments + 1):
        t = i * increment
        q1 = lerp(p1, p2, t)
        q2 = lerp(p2, p3, t)
        bezier_point = lerp(q1, q2, t)
        points.append(bezier_point)

    return points

# Uses gradients to generate equally-spaced points for a cubic bezier curve
def generate_cubic_points(p0, p1, p2, p3, segmentDistance: float):

    # Convert to list if necessary
    p0 = list(p0)
    p1 = list(p1)
    p2 = list(p2)
    p3 = list(p3)

    points = []

    ns = 0
    while ns < 1:
        point = get_cubic_point(ns, p0, p1, p2, p3)

        # for some reason points are getting way out of bounds. stop if so
        if point[0] < 0 or point[0] > 144 or point[1] < 0 or point[1] > 144:
            break
        points.append(point)

        dxds, dyds = get_cubic_gradient(ns, p0, p1, p2, p3)
        dsdt = segmentDistance / hypo(dxds, dyds)
        ns += dsdt

    # make sure to include the end point
    if ns < 1:
        points.append(p3)

    return points


VECTOR_STRENGTH = 1.2 - 1 # The -1 is to make editing more intuitive. At a first value of 1, they're at 100%, 0.5 at 50% etc.

# Returns the point on a bezier curve defined by the four points on location 0<=t<1.
def get_cubic_point(t: float, p0: list, p1: list, p2: list, p3: list) -> list:
    p1[0] += p0[0] + p1[0] * VECTOR_STRENGTH
    p1[1] += p0[1] + p1[1] * VECTOR_STRENGTH
    p2[0] += p3[0] + p2[0] * VECTOR_STRENGTH
    p2[1] += p3[1] + p2[1] * VECTOR_STRENGTH

    inv_t = 1-t
    coefs = [inv_t ** 3,
             3 * t * inv_t ** 2,
             3 * inv_t * t ** 2,
             t ** 3]

    tx = coefs[0] * p0[0] + coefs[1] * p1[0] + \
         coefs[2] * p2[0] + coefs[3] * p3[0]
    ty = coefs[0] * p0[1] + coefs[1] * p1[1] + \
         coefs[2] * p2[1] + coefs[3] * p3[1]

    return [tx, ty]


# returns the derivative on a bezier curve defined by the four points on location 0<=t<1
def get_cubic_gradient(t: float, p0: tuple, p1: tuple, p2: tuple, p3: tuple) -> list:

    inv_t = 1-t

    p1[0] += p0[0] + p1[0] * VECTOR_STRENGTH
    p1[1] += p0[1] + p1[1] * VECTOR_STRENGTH
    p2[0] += p3[0] + p2[0] * VECTOR_STRENGTH
    p2[1] += p3[1] + p2[1] * VECTOR_STRENGTH

    xs = [p1[0] - p0[0], p2[0] - p1[0], p3[0] - p2[0]]
    ys = [p1[1] - p0[1], p2[1] - p1[1], p3[1] - p2[1]]

    coefs = [3 * inv_t ** 2,
             6 * inv_t * t,
             3 * t ** 2]

    tx = coefs[0] * xs[0] + coefs[1] * xs[1] + coefs[2] * xs[2]
    ty = coefs[0] * ys[0] + coefs[1] * ys[1] + coefs[2] * ys[2]

    return [tx, ty]