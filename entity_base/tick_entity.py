from entity_base.entity import Entity, ROOT_CONTAINER
from entity_base.listeners.tick_listener import TickLambda
from common.draw_order import DrawOrder

"""
Used when you want to run some function every tick at some specific order
"""

class TickEntity(Entity):

    def __init__(self, functionToRun, drawOrder: DrawOrder = DrawOrder.BACK):

        super().__init__(parent = ROOT_CONTAINER,
                         tick = TickLambda(self, FonTick = functionToRun),
                         drawOrder = drawOrder
                         )