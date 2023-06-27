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
        
            
        
        pass

    # convert from the given system to the other system as a tuple
    def convertFrom(self, oldSystem: T, oldPoint: tuple) -> tuple:
        pass

class _Coordinate(Enum):
    TYPEA = 1
    TYPEB = 2

class CoordinateTransformTest:

        def __init__(self):

            print("Testing CoordinateTransform")

            C = _Coordinate

            builder = CoordinateTransformBuilder[C](C.TYPEA, C.TYPEB)
            builder.defineFirstPoint((5,5), (20,20))
            builder.defineSecondPoint((15,20), (100,100))
            transform = builder.build()

            assert(transform.convertFrom(C.TYPEA, (5,5)) == (20,20))
            assert(transform.convertFrom(C.TYPEB, (20,20)) == (5,5))

            assert(transform.convertFrom(C.TYPEA, (15,20)) == (100,100))
            assert(transform.convertFrom(C.TYPEB, (100,100)) == (15,20))

if __name__ == "__main__":
    CoordinateTransformTest()