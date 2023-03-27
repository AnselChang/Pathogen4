import pygame, pygame.gfxdraw, math
import math_functions

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
def drawLine(screen: pygame.Surface, color: tuple, x1: int, y1: int, x2: int, y2: int, thickness: int = 1, alpha: int = 255):

    thickness = round(thickness)

    if alpha != 255:
        mx = min(x1, x2)
        my = min(y1, y2)
        dx = abs(x1-x2)
        dy = abs(y1-y2)
        x1 -= mx
        x2 -= mx
        y1 -= my
        y2 -= my


    X0 = [x1,y1]
    X1 = [x2,y2]

    center_L1 = [(x1+x2) / 2, (y1+y2) / 2 ]
    length = math_functions.distance(x1, y1, x2, y2)
    angle = math.atan2(X0[1] - X1[1], X0[0] - X1[0])
    
    UL = (center_L1[0] + (length/2.) * math.cos(angle) - (thickness/2.) * math.sin(angle), center_L1[1] + (thickness/2.) * math.cos(angle) + (length/2.) * math.sin(angle))
    UR = (center_L1[0] - (length/2.) * math.cos(angle) - (thickness/2.) * math.sin(angle), center_L1[1] + (thickness/2.) * math.cos(angle) - (length/2.) * math.sin(angle))
    BL = (center_L1[0] + (length/2.) * math.cos(angle) + (thickness/2.) * math.sin(angle), center_L1[1] - (thickness/2.) * math.cos(angle) + (length/2.) * math.sin(angle))
    BR = (center_L1[0] - (length/2.) * math.cos(angle) + (thickness/2.) * math.sin(angle), center_L1[1] - (thickness/2.) * math.cos(angle) - (length/2.) * math.sin(angle))

    if alpha == 255:
        pygame.gfxdraw.aapolygon(screen, (UL, UR, BR, BL), color)
        pygame.gfxdraw.filled_polygon(screen, (UL, UR, BR, BL), color)
    else:
        surface = pygame.Surface([dx, dy], pygame.SRCALPHA)
        
        pygame.gfxdraw.aapolygon(surface, (UL, UR, BR, BL), (*color, alpha))
        pygame.gfxdraw.filled_polygon(surface, (UL, UR, BR, BL), (*color, alpha))

        screen.blit(surface, (mx, my))