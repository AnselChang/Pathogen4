import pygame

class SurfaceOpacityCache:
    """
    A utility class for caching different versions of a given Pygame surface at different opacity levels.
    The class pre-caches surfaces with different levels of transparency, ranging from 0% to 100%, with the given delta.
    The surfaces are stored in a dictionary for quick access and optimized performance.
    """

    def __init__(self, surface, resolution):
        """
        Constructs a SurfaceCache object for the given Pygame surface.

        Parameters:
        surface (pygame.Surface): The Pygame surface to cache.
        resolution (int): the number of images to generate
        """
        self.surface = surface
        self.cache = {}

        # Pre-cache surfaces with different opacity levels
        for i in range(resolution):
            alpha = (i+1) * 255 / resolution
            self.cache[alpha] = surface.copy().convert_alpha()
            self.cache[alpha].fill((255, 255, 255, alpha), special_flags=pygame.BLEND_RGBA_MULT)

    # opacity from 0 to 1
    def get(self, opacity):
        """
        Returns the cached Pygame surface with the closest matching opacity level.

        Parameters:
        opacity (int): The opacity level, ranging from 0 (completely transparent) to 100 (completely opaque).

        Returns:
        pygame.Surface: The cached Pygame surface with the closest matching opacity level.
        """
        # Find the closest matching opacity level in the cache
        alpha = opacity * 255
        closest_opacity = min(self.cache.keys(), key=lambda x: abs(x - alpha))

        # Return the cached surface with the closest matching opacity level
        return self.cache[closest_opacity]
