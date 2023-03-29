"""

Straight segment -> StraightCommand
    - distance
    - start position
    - end position

Arc segment -> ArcCommand
    - arc length
    - radius
    - start position
    - end position
    - start angle
    - end angle

Node stores
- list of InlineTurns
- start angle
- end angle
- start angle -> inline1 -> inline 2 -> end angle


"""

class CommandPathInterface:
    pass