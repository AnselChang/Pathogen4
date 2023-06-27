from enum import Enum
from typing import TypeVar, Generic

"""
Maps one coordinate system to another.
Define coordinate system relation by providing two points,
in respect to both systems.
For example, for a system A and B, we have:
    System A: (5,5) -> (15,20)
    System B: (20,20) -> (100,100)

Refer to test cases at bottom of file for usage.

"""

T = TypeVar('T')
class CoordinateTransformBuilder(Generic[T]):
    
    def __init__(self, systemAType: T, systemBType: T):
        self.systemAType = systemAType
        self.systemBType = systemBType
        self.systemAFirstPoint = None
        self.systemBFirstPoint = None
        self.systemASecondPoint = None
        self.systemBSecondPoint = None

    # define first point in respect to first and second coordinate systems
    def defineFirstPoint(self, systemAFirstPoint: tuple, systemBFirstPoint: tuple):
        self.systemAFirstPoint = systemAFirstPoint
        self.systemBFirstPoint = systemBFirstPoint

    def defineSecondPoint(self, systemASecondPoint: tuple, systemBSecondPoint: tuple):
        self.systemASecondPoint = systemASecondPoint
        self.systemBSecondPoint = systemBSecondPoint

    def build(self) -> 'CoordinateTransform[T]':
        if self.systemAFirstPoint is None or self.systemBFirstPoint is None:
            raise Exception("First point not defined.")
        elif self.systemASecondPoint is None or self.systemBSecondPoint is None:
            raise Exception("Second point not defined.")
        
        return CoordinateTransform[T](
            self.systemAType,
            self.systemBType,
            self.systemAFirstPoint,
            self.systemBFirstPoint,
            self.systemASecondPoint,
            self.systemBSecondPoint
        )

class CoordinateTransform(Generic[T]):

    def __init__(self,
                 systemAType: T,
                 systemBType: T,
                 systemAFirstPoint: tuple,
                 systemBFirstPoint: tuple,
                 systemASecondPoint: tuple,
                 systemBSecondPoint: tuple):
        
        if systemAFirstPoint == systemASecondPoint or systemBFirstPoint == systemBSecondPoint:
            raise ValueError("The two points in a system should not be the same.")

        self.systemAType = systemAType
        self.systemBType = systemBType

        # Precompute scales and offsets
        self.scale_x_A_to_B = (systemBSecondPoint[0] - systemBFirstPoint[0]) / (systemASecondPoint[0] - systemAFirstPoint[0])
        self.offset_x_A_to_B = systemBFirstPoint[0] - self.scale_x_A_to_B * systemAFirstPoint[0]
        
        self.scale_y_A_to_B = (systemBSecondPoint[1] - systemBFirstPoint[1]) / (systemASecondPoint[1] - systemAFirstPoint[1])
        self.offset_y_A_to_B = systemBFirstPoint[1] - self.scale_y_A_to_B * systemAFirstPoint[1]

        self.scale_x_B_to_A = 1 / self.scale_x_A_to_B
        self.offset_x_B_to_A = systemAFirstPoint[0] - self.scale_x_B_to_A * systemBFirstPoint[0]

        self.scale_y_B_to_A = 1 / self.scale_y_A_to_B
        self.offset_y_B_to_A = systemAFirstPoint[1] - self.scale_y_B_to_A * systemBFirstPoint[1]

    # convert from the given system to the other system as a tuple
    def convertFrom(self, oldSystem: T, oldPoint: tuple) -> tuple:
        
        if oldSystem == self.systemAType:
            x = self.scale_x_A_to_B * oldPoint[0] + self.offset_x_A_to_B
            y = self.scale_y_A_to_B * oldPoint[1] + self.offset_y_A_to_B
        else:
            x = self.scale_x_B_to_A * oldPoint[0] + self.offset_x_B_to_A
            y = self.scale_y_B_to_A * oldPoint[1] + self.offset_y_B_to_A
            
        return (x, y)

class _Coordinate(Enum):
    TYPEA = 1
    TYPEB = 2

class CoordinateTransformTest:

        def __init__(self):

            print("Testing CoordinateTransform")

            C = _Coordinate

            # Test case 1
            builder1 = CoordinateTransformBuilder[C](C.TYPEA, C.TYPEB)
            builder1.defineFirstPoint((5,6), (6,5))
            builder1.defineSecondPoint((0,0), (0,0))
            transform1 = builder1.build()

            
if __name__ == "__main__":
    CoordinateTransformTest()