from utility.math_functions import distanceTuples

def lerp(p1, p2, t):
    return (p1[0] + t * (p2[0] - p1[0]), p1[1] + t * (p2[1] - p1[1]))

def bezier_curve_points(p1, p2, p3, segment_length):
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