import pygame, pygame.gfxdraw, math
import utility.math_functions as math_functions

def shade(color: tuple, scalar: float):
    return math_functions.intTuple(math_functions.clampTuple(math_functions.scaleTuple(color, scalar), 0, 255))

# Draw a transparent rect on a Pygame surface
def drawTransparentRect(surface, x, y, w, h, color, alpha, radius = 0, width = 0):

    alpha = math_functions.clamp(alpha, 0, 255)

    rect_surface = pygame.Surface((w, h), pygame.SRCALPHA)
    pygame.draw.rect(rect_surface, (*color, alpha), (0,0,w,h), border_radius = radius, width = width)
    surface.blit(rect_surface, (x, y))

# Draw a transparent circle on a Pygame surface
def drawTransparentCircle(surface, center, radius, color, alpha = 255, width = 0):

    if alpha == 255:
        pygame.draw.circle(surface, color, center, radius)
        return

    circleSurface = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
    color_with_alpha = list(color) + [alpha]
    pygame.draw.circle(circleSurface, color_with_alpha, (radius, radius), radius, width = width)
    surface.blit(circleSurface, (center[0]-radius, center[1]-radius))

# Draw a thick line on a Pygame surface
def drawLine(screen: pygame.Surface, color: tuple, x1: int, y1: int, x2: int, y2: int, thickness: int = 1, borderColor: tuple = None):

    thickness = round(thickness)

    X0 = [x1,y1]
    X1 = [x2,y2]

    center_L1 = [(x1+x2) / 2, (y1+y2) / 2 ]
    length = math_functions.distance(x1, y1, x2, y2)
    angle = math.atan2(X0[1] - X1[1], X0[0] - X1[0])
    
    UL = (center_L1[0] + (length/2.) * math.cos(angle) - (thickness/2.) * math.sin(angle), center_L1[1] + (thickness/2.) * math.cos(angle) + (length/2.) * math.sin(angle))
    UR = (center_L1[0] - (length/2.) * math.cos(angle) - (thickness/2.) * math.sin(angle), center_L1[1] + (thickness/2.) * math.cos(angle) - (length/2.) * math.sin(angle))
    BL = (center_L1[0] + (length/2.) * math.cos(angle) + (thickness/2.) * math.sin(angle), center_L1[1] - (thickness/2.) * math.cos(angle) + (length/2.) * math.sin(angle))
    BR = (center_L1[0] - (length/2.) * math.cos(angle) + (thickness/2.) * math.sin(angle), center_L1[1] - (thickness/2.) * math.cos(angle) - (length/2.) * math.sin(angle))

    pygame.gfxdraw.aapolygon(screen, (UL, UR, BR, BL), color)
    pygame.gfxdraw.filled_polygon(screen, (UL, UR, BR, BL), color)

    if borderColor is not None:
        pygame.gfxdraw.aapolygon(screen, (UL, UR, BR, BL), borderColor)
    
def getText(font: pygame.font.Font, string: str, color: tuple, opacity: float = 1) -> pygame.Surface:
    text = font.render(string, True, color)
    text.set_alpha(opacity * 255)
    return text

# align = 0 -> align left/top
# align = 0.5 -> align mid
# align = 1 -> align right/bottom
# return text width
def drawText(surface: pygame.Surface, font: pygame.font.Font, string: str, color: tuple, x: int, y: int, alignX: float = 0.5, alignY: float = 0.5, opacity = 1) -> int:
    
    text = getText(font, string, color, opacity)
    width = text.get_width()
    height = text.get_height()

    x -= width * alignX
    y -= height * alignY
    surface.blit(text, (x,y))

    return width, height

# Return an image given a filename
def getImage(filename: str, imageScale: float = 1) -> pygame.Surface:
    unscaledImage = pygame.image.load(filename).convert_alpha()
    if imageScale == 1:
        return unscaledImage
    else:
        dimensions = ( int(unscaledImage.get_width() * imageScale), int(unscaledImage.get_height() * imageScale) )
        return pygame.transform.smoothscale(unscaledImage, dimensions)
    
# Draw surface with center coordinates (cx, cy)
def drawSurface(surface: pygame.Surface, drawnSurface: pygame.Surface, cx: int, cy: int, angle: float = 0):
    
    if angle != 0:
        drawnSurface = pygame.transform.rotate(drawnSurface, angle)

    r = drawnSurface.get_rect()
    rect = drawnSurface.get_rect(center = (cx, cy))
    surface.blit(drawnSurface, (rect.x, rect.y))

def brightenSurface(surface, brightness): # brigtness from 0-255
    # Convert the surface to a new format that allows direct pixel access
    surface = surface.convert_alpha().copy()

    # Loop over the pixels and increase the brightness of each pixel
    for x in range(surface.get_width()):
        for y in range(surface.get_height()):
            r, g, b, a = surface.get_at((x, y))
            r = max(0, min(r + brightness, 255))
            g = max(0, min(g + brightness, 255))
            b = max(0, min(b + brightness, 255))
            surface.set_at((x, y), (r, g, b, a))

    return surface

def scaleSurface(surface, scale):
    width = int(surface.get_width() * scale)
    height = int(surface.get_height() * scale)
    return pygame.transform.smoothscale(surface, (width, height))

def getGradientSurface(width, height, color1, color2, vertical = True, invert = False):

    width = int(width)
    height = int(height)

    """Draws a rectangle with a gradient from color1 to color2"""
    gradient = pygame.Surface((width, height))
    if vertical:
        for y in range(height):
            progress = y / height
            color = [int(c1 * (1 - progress) + c2 * progress) for c1, c2 in zip(color1, color2)]
            if invert:
                y = height-y-1
            pygame.draw.line(gradient, color, (0, y), (width, y))
    else:
        for x in range(width):
            progress = x / width
            color = [int(c1 * (1 - progress) + c2 * progress) for c1, c2 in zip(color1, color2)]
            if invert:
                x = width-x-1
            pygame.draw.line(gradient, color, (x, 0), (x, height))
    
    gradient.set_alpha(color1[3])
    return gradient


def drawDottedLine(screen, color, start_pos, end_pos, dot_length=4, dot_gap=4):
    """
    Draw a dotted line between two points on the screen.
    :param screen: the Pygame screen surface to draw on
    :param color: the color of the line as an RGB tuple
    :param start_pos: the start position of the line as an (x, y) tuple
    :param end_pos: the end position of the line as an (x, y) tuple
    :param dot_length: the length of each dot in pixels (default: 4)
    :param dot_gap: the gap between dots in pixels (default: 4)
    """
    # calculate the distance and angle between the two points
    dx, dy = end_pos[0] - start_pos[0], end_pos[1] - start_pos[1]
    distance = pygame.math.Vector2(dx, dy).length()
    angle = pygame.math.Vector2(dx, dy).angle_to((1, 0))

    # calculate the number of dots needed to fill the line
    dot_count = int(distance / (dot_length + dot_gap))

    # calculate the x and y distances between each dot
    x_spacing = dx / dot_count
    y_spacing = dy / dot_count

    # draw the dotted line
    current_pos = start_pos
    for i in range(dot_count):
        end_pos = (current_pos[0] + x_spacing, current_pos[1] + y_spacing)
        pygame.draw.line(screen, color, current_pos, end_pos, dot_length)
        current_pos = (end_pos[0] + x_spacing, end_pos[1] + y_spacing)


def scaleImageToRect(image: pygame.Surface, width, height):
    """
    Scale an image so that it fits entirely inside a given rectangle while preserving its aspect ratio.

    Args:
        image (pygame.Surface): The image surface to scale.
        rect (pygame.Rect): The rectangle where the image should fit.

    Returns:
        pygame.Surface: The scaled image surface.

    """

    rect = pygame.Rect(0, 0, width, height)

    # Get the dimensions of the image and the rectangle
    imgWidth, imgHeight = image.get_size()
    rectWidth, rectHeight = rect.size

    # Calculate the aspect ratios of the image and the rectangle
    imgAspectRatio = imgWidth / imgHeight
    rectAspectRatio = rectWidth / rectHeight

    # Calculate the scaling factor to fit the image inside the rectangle
    if imgAspectRatio > rectAspectRatio:
        scaleFactor = rectWidth / imgWidth
    else:
        scaleFactor = rectHeight / imgHeight

    # Scale the image and return the new surface
    scaledSize = (round(imgWidth * scaleFactor), round(imgHeight * scaleFactor))
    return pygame.transform.smoothscale(image, scaledSize)

# manually draw an arc through linear approximation
# parity is the modular direction from theta1 -> theta2
def drawArc(screen: pygame.Surface, color: tuple, center: tuple, radius: float, theta1: float, theta2: float, parity: bool, thickness: int = 1, alpha: int = 255):

    dt = math_functions.deltaInHeadingParity(theta2, theta1, parity)

    K = 1 # constant for how many lines to draw (the more the smoother)
    numberLines = min(500, int(K * abs(dt*radius)))

    x1, y1 = center[0] + radius * math.cos(theta1), center[1] - radius * math.sin(theta1)
    for i in range(1, numberLines+1):
        t2 = theta1 + dt * (i) / numberLines
        x2, y2 = center[0] + radius * math.cos(t2), center[1] - radius * math.sin(t2)

        drawLine(screen, color, x1, y1, x2, y2, thickness, alpha)

        x1 = x2
        y1 = y2