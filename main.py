from BaseEntity.circle_entity import CircleEntity
from EntityHandler.entity_manager import EntityManager
from EntityHandler.interactor import Interactor
from reference_frame import PointRef, Ref, initReferenceframe
from field_transform import FieldTransform
from dimensions import Dimensions
import pygame
import sys

pygame.init()

RED = [255,0,0]
GREEN = [0,255,0]

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

    entities.addEntity(CircleEntity(PointRef(Ref.SCREEN, (100,100)), 50, RED))
    #entities.addEntity(CircleEntity(PointRef(Ref.SCREEN, (500,500)), 5, GREEN))

    # initialize pygame artifacts
    pygame.display.set_caption("Pathogen 4.0")
    clock = pygame.time.Clock()

    # Main game loop
    while True:

        mouse.screenRef = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.VIDEORESIZE:
                screen = dimensions.resizeScreen(*event.size)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                interactor.onMouseDown(entities)
            elif event.type == pygame.MOUSEBUTTONUP:
                interactor.onMouseUp(entities)

        interactor.hoveredEntity = entities.getEntityAtPosition(mouse)

        # Clear screen
        screen.fill((255,255,255))

        entities.drawEntities(interactor, screen)

        # Update display and maintain frame rate
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
