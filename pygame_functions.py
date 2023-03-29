import pygame, pygame.gfxdraw, math
import math_functions

def shade(color: tuple, scalar: float):
    return math_functions.intTuple(math_functions.clampTuple(math_functions.scaleTuple(color, scalar), 0, 255))

# Draw a transparent rect on a Pygame surface
def drawTransparentRect(surface, x1, y1, x2, y2, color, alpha):
    
    width = abs(x2 - x1)
    height = abs(y2 - y1)
    x = min(x1, x2)
    y = min(y1, y2)

    rect_surface = pygame.Surface((width, height), pygame.SRCALPHA)
    rect_surface.fill((color[0], color[1], color[2], alpha))
    surface.blit(rect_surface, (x, y))

# Draw a transparent circle on a Pygame surface
def drawTransparentCircle(surface, center, radius, color, alpha):

    circleSurface = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
    color_with_alpha = list(color) + [alpha]
    pygame.draw.circle(circleSurface, color_with_alpha, (radius, radius), radius)
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
    

pygame.font.init()
FONT_PATH = 'Corbel.ttf'
FONT15 = pygame.font.Font(FONT_PATH, 15)
FONT20 = pygame.font.Font(FONT_PATH, 20)
FONT25 = pygame.font.Font(FONT_PATH, 25)
FONT30 = pygame.font.Font(FONT_PATH, 30)
FONT40 = pygame.font.Font(FONT_PATH, 40)

FONTCODE = pygame.font.SysFont("arial", 8)

# align = 0 -> align left/top
# align = 0.5 -> align mid
# align = 1 -> align right/bottom
def drawText(surface: pygame.Surface, font: pygame.font, string: str, color: tuple, x: int, y: int, alignX: float = 0.5, alignY: float = 0.5):
    text = font.render(string, True, color)
    x -= text.get_width()*alignX
    y -= text.get_height()*alignY
    surface.blit(text, (x,y))