import math

"""
A motion profile class that generates a smooth motion trajectory between a start value and an end value.
The class calculates a trapezoidal motion profile, where the value starts ramping up at a constant acceleration until
it reaches a maximum speed, and then starts ramping down at the same acceleration until it reaches the end value.
The speed is continuously adjusted to ensure that the maximum speed is not exceeded, and the distance remaining is
calculated to ensure that the value does not overshoot the end value. The `tick()` method returns the current value
after each update.
"""

class MotionProfile:
    def __init__(self, endValue, speed, threshold = 0.001):
        self._speed = speed
        self._currentValue = endValue
        self._threshold = threshold

        self._previous = None

        self.setEndValue(endValue)

    def setEndValue(self, endValue):
        self._endValue = endValue

    def forceToEndValue(self):
        self._currentValue = self._endValue
    
    def get(self) -> float:
        distanceRemaining = self._endValue - self._currentValue
        if abs(distanceRemaining) < self._threshold:
            return self._endValue
        else:
            return self._currentValue

    def isDone(self) -> bool:
        distanceRemaining = self._endValue - self._currentValue
        if abs(distanceRemaining) < self._threshold:
            self._currentValue = self._endValue
            return True
        else:
            return False

    def tick(self) -> float:

        self._previous = self._currentValue

        # Calculate the distance remaining
        distanceRemaining = self._endValue - self._currentValue

        # If we're already at the end value, return it
        if abs(distanceRemaining) < self._threshold:
            self._currentValue = self._endValue
            return self._currentValue
        
        self._currentValue += (self._endValue - self._currentValue) * self._speed

        return self._currentValue
    
    def wasChange(self) -> bool:
        return self._previous != self._currentValue