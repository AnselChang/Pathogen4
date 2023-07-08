from entity_base.entity import Entity
from entity_base.entity import initEntityClass, setRootContainer

from entity_handler.entity_manager import EntityManager
from entity_handler.interactor import Interactor

from command_creation.test_commands import *

from root_container.panel_container.command_expansion.command_expansion_container import CommandExpansionContainer

from entity_ui.tooltip import initTooltipFont

from common.font_manager import FontManager, FontID
from common.image_manager import ImageManager, ImageID
from common.dimensions import Dimensions
import pygame
import sys

"""
A window object creates a pygame window with a context for entities, EntityManager, etc.
"""
class Window:

    def __init__(self, defaultWindowWidthPercent: float = 0.8, defaultWindowHeightPercent: float = 0.8):
        
        # in charge of overarching dimensions of windows
        self.dimensions = Dimensions(defaultWindowWidthPercent, defaultWindowHeightPercent)
        self.fontManager = FontManager(self.dimensions)
        
        self.screen = self.dimensions.resizeScreen(self.dimensions.DEFAULT_SCREEN_WIDTH, self.dimensions.DEFAULT_SCREEN_HEIGHT)
        self.images = ImageManager()
        imageSize = self.images.get(ImageID.FIELD).get_width()
        self.dimensions.setFieldSizePixels(imageSize)

        # set font size of tooltips
        initTooltipFont(self.fontManager.getDynamicFont(FontID.FONT_NORMAL, 10))

        # Initialize entities
        self.interactor = Interactor(self.dimensions)
        self.entities = EntityManager()
        initEntityClass(self.entities, self.interactor, self.images, self.fontManager, self.dimensions)
        self.rootContainer = self.entities.initRootContainer()
        setRootContainer(self.rootContainer)

        # initialize pygame artifacts
        pygame.display.set_caption("Pathogen 4.0 (Ansel Chang)")
        self.clock = pygame.time.Clock()

    def getRootContainer(self) -> Entity:
        return self.rootContainer

    def run(self):

        oldHoveredEntity = None
        oldMouse = None
        thisTickIsDifferent = True # whether this frame is different from previous
        while True:

            self.dimensions.RESIZED_THIS_FRAME = False

            mouse = pygame.mouse.get_pos()
            if mouse != oldMouse:
                thisTickIsDifferent = True
                oldMouse = mouse
            
            if thisTickIsDifferent: # only recompute hovered entity if mouse moved
                hoveredEntity = self.entities.getEntityAtPosition(mouse)
                if oldHoveredEntity is not hoveredEntity:
                    self.entities.redrawScreenThisTick()
                oldHoveredEntity = hoveredEntity
            else:
                hoveredEntity = oldHoveredEntity

            if hoveredEntity is not None:
                parent = f", {str(hoveredEntity._parent)}"
            else:
                parent = ""
            msg = f"({mouse[0]}, {mouse[1]}), {str(hoveredEntity)}" + parent
            #inches = fieldContainer.fieldEntity.mouseToInches(mouse)
            #mouse2 = fieldContainer.fieldEntity.inchesToMouse(inches)
            pygame.display.set_caption(msg)

            self.interactor.setHoveredEntity(hoveredEntity, mouse)
            # handle events and call callbacks
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.VIDEORESIZE:
                    screen = self.dimensions.resizeScreen(*event.size)
                elif event.type == pygame.MOUSEWHEEL:
                    self.interactor.onMouseWheel(event.y, mouse)
                elif event.type == pygame.MOUSEBUTTONDOWN and (event.button == 1 or event.button == 3):
                    ctrlKey = pygame.key.get_pressed()[pygame.K_LCTRL]
                    shiftKey = pygame.key.get_pressed()[pygame.K_LSHIFT]
                    right = (event.button == 1 and ctrlKey) or event.button == 3
                    self.interactor.onMouseDown(self.entities, mouse, right, shiftKey)

                elif event.type == pygame.MOUSEBUTTONUP:
                    self.interactor.onMouseUp(self.entities, mouse)

                elif event.type == pygame.MOUSEMOTION:
                    self.interactor.onMouseMove(self.entities, mouse)
                elif event.type == pygame.KEYDOWN:
                    self.entities.onKeyDown(event.key)
                elif event.type == pygame.KEYUP:
                    self.entities.onKeyUp(event.key)

            # Perform calculations
            self.entities.tick()

            # Draw everything
            if self.entities.isRedrawThisTick():
                self.entities.drawEntities(self.interactor, self.screen, mouse, self.dimensions)
                # Update display and maintain frame rate
                pygame.display.flip()
                self.entities.resetFlagAfterDrawingEverything()
                thisTickIsDifferent = True
            else:
                thisTickIsDifferent = False
            
            self.clock.tick(60) # fps