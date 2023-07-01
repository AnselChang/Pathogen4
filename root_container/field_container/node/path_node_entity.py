from __future__ import annotations
import math
from typing import TYPE_CHECKING
from root_container.field_container.field_entity import FieldEntity

from root_container.field_container.node.node_line import NodeLine
from models.path_models.segment_direction import SegmentDirection
if TYPE_CHECKING:
    from models.path_models.path_node_model import PathNodeModel

from enum import Enum
from entity_base.abstract_circle_entity import AbstractCircleEntity
from entity_base.entity import Entity
from common.reference_frame import PointRef, Ref, VectorRef
from entity_base.image.image_state import ImageState
from entity_base.listeners.drag_listener import DragLambda
from entity_base.listeners.click_listener import ClickLambda
from entity_base.listeners.select_listener import SelectListener, SelectLambda
from entity_base.listeners.key_listener import KeyLambda
from entity_base.listeners.hover_listener import HoverLambda
from root_container.field_container.segment.path_segment_entity import PathSegmentEntity
from root_container.field_container.field_container import FieldContainer
from common.draw_order import DrawOrder
from entity_handler.interactor import Interactor
from entity_handler.entity_manager import EntityManager

from adapter.path_adapter import AdapterInterface, PathAttributeID
from adapter.turn_adapter import TurnAdapter

from root_container.field_container.node.constraints import Constraints
from root_container.field_container.node.bezier_theta_node import BezierThetaNode

from common.image_manager import ImageID
from data_structures.linked_list import LinkedListNode

from utility.math_functions import isInsideBox
from utility.pygame_functions import shade
from utility.angle_functions import deltaInHeading, headingDiff
from utility.format_functions import formatDegrees

import pygame

"""
Interactable path nodes
Neighbors PathSegmentEntities
Referenced in PathSection
"""

class PathNodeEntity(Entity):

    TURN_DISABLED_COLOR = (0,0,0)
    BLUE_COLOR = (102, 153, 255)
    FIRST_BLUE_COLOR = (40, 40, 255)
    RED_COLOR = (255, 102, 102)

    def __init__(self, fieldEntity: FieldEntity, model: PathNodeModel):
        self.field = fieldEntity
        self.model = model
        Entity.__init__(self,
                parent = fieldEntity
        )

        self.RADIUS = 5
        
    def defineCenter(self) -> tuple:
        return self.field.inchesToMouse(self.model.getPosition())
    
    def isTouching(self, position: tuple) -> bool:
        MARGIN = 4
        return self.distanceTo(position) <= self.RADIUS + MARGIN
    
    def draw(self, screen, isActive, isHovered):
        COLOR = (255, 0, 0)
        POSITION = [self.CENTER_X, self.CENTER_Y]
        pygame.draw.circle(screen, COLOR, POSITION, self.RADIUS)