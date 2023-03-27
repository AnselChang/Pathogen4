import pygame

def drawTransparentRect(surface, x1, y1, x2, y2, color, alpha):
    
    width = abs(x2 - x1)
    height = abs(y2 - y1)
    x = min(x1, x2)
    y = min(y1, y2)

    rect_surface = pygame.Surface((width, height), pygame.SRCALPHA)
    rect_surface.fill((color[0], color[1], color[2], alpha))
    surface.blit(rect_surface, (x, y))

def drawTransparentCircle(surface, center, radius, color, alpha):
    """
    Draw a transparent circle on a Pygame surface.
    """
    circleSurface = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
    color_with_alpha = list(color) + [alpha]
    pygame.draw.circle(circleSurface, color_with_alpha, (radius, radius), radius)
    surface.blit(circleSurface, (center[0]-radius, center[1]-radius))