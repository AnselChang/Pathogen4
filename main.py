from PathEntities.independent_circle_entity import IndependentCircleEntity
from PathEntities.dependent_circle_entity import DependentCircleEntity
from PathEntities.test_edge_entity import TestEdgeEntity

from UIEntities.radio_group import RadioGroup
from UIEntities.tab_entity import TabEntity

from EntityHandler.entity_manager import EntityManager
from EntityHandler.interactor import Interactor
from reference_frame import PointRef, Ref, initReferenceframe, VectorRef
from field_transform import FieldTransform
from dimensions import Dimensions
import pygame, random
import sys

pygame.init()

RED = [255,0,0]
GREEN = [0,255,0]
BLUE = [0,0,255]

def initTabs(dimensions, entities) -> RadioGroup:
    tabs = RadioGroup(entities)
    tabNames = ["A", "B", "C"]

    N = len(tabNames)
    for i, text in enumerate(tabNames):
        tabs.add(TabEntity(dimensions, text, i, N))
    return tabs

def main():
    
    # Initialize field
    dimensions = Dimensions()
    screen = dimensions.resizeScreen(800, 800)
    fieldTransform: FieldTransform = FieldTransform(dimensions)
    initReferenceframe(dimensions, fieldTransform)
    mouse: PointRef = PointRef()
    
    # Initialize entities
    interactor = Interactor()
    entities = EntityManager()

    # Create tabs
    tabs = initTabs(dimensions, entities)

    for i in range(2):
        x = random.randint(100, 600)
        y = random.randint(100, 600)

        a = IndependentCircleEntity(PointRef(Ref.SCREEN, (x,y)), 50, RED, "red")
             
        b = DependentCircleEntity(a, VectorRef(Ref.SCREEN, (50,50)), 20, GREEN, "green")
        
        c = DependentCircleEntity(b, VectorRef(Ref.SCREEN, (50,50)), 20, BLUE, "blue")
        

        entities.addEntity(TestEdgeEntity(a, b))
        entities.addEntity(TestEdgeEntity(b, c))

        entities.addEntity(a)
        entities.addEntity(b)
        entities.addEntity(c)

    # initialize pygame artifacts
    pygame.display.set_caption("Pathogen 4.0")
    clock = pygame.time.Clock()
    # Main game loop
    while True:

        mouse.screenRef = pygame.mouse.get_pos()
        interactor.hoveredEntity = entities.getEntityAtPosition(mouse)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.VIDEORESIZE:
                screen = dimensions.resizeScreen(*event.size)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                ctrlKey = pygame.key.get_pressed()[pygame.K_LCTRL]
                right = (event.button == 1 and ctrlKey) or event.button == 3
                interactor.onMouseDown(entities, mouse, right)

            elif event.type == pygame.MOUSEBUTTONUP:
                interactor.onMouseUp(entities, mouse)

            elif event.type == pygame.MOUSEMOTION:
                interactor.onMouseMove(entities, mouse)

        # Clear screen
        screen.fill((255,255,255))

         # draw panel
        x, y = dimensions.FIELD_WIDTH, 0
        width, height = dimensions.PANEL_WIDTH, dimensions.SCREEN_HEIGHT
        pygame.draw.rect(screen, (100,100,100), (x, y, width, height))

        entities.drawEntities(interactor, screen)
        interactor.draw(screen)

       

        # Update display and maintain frame rate
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
