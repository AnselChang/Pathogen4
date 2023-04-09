def formatDegrees(radians: float, roundDigits: int = 2) -> str:
    deg = round(radians * 180 / 3.1415, roundDigits)
    return f"{deg}\u00b0"

def formatInches(inches: float, roundDigits: int = 2) -> str:
    return f"{round(inches, roundDigits)}\""

def hsvToRgb(h, s, v) -> tuple:
    """
    Convert HSV color values to RGB color values.
    """
    # Convert HSV values to the range 0-1
    h /= 360.0
    s /= 100.0
    v /= 100.0

    # Calculate the RGB values
    if s == 0:
        r, g, b = v, v, v
    else:
        i = int(h * 6.) # floor
        f = (h * 6.) - i
        p = v * (1. - s)
        q = v * (1. - s * f)
        t = v * (1. - s * (1. - f))
        if i == 0: r, g, b = v, t, p
        if i == 1: r, g, b = q, v, p
        if i == 2: r, g, b = p, v, t
        if i == 3: r, g, b = p, q, v
        if i == 4: r, g, b = t, p, v
        if i == 5: r, g, b = v, p, q

    # Convert the RGB values to the range 0-255
    r = int(r * 255)
    g = int(g * 255)
    b = int(b * 255)

    return (r, g, b)
