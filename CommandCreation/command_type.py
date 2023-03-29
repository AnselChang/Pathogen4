from dataclasses import dataclass

@dataclass
class CommandType:
    color: tuple

CommandType.TURN = CommandType((0,0,0))
CommandType.STRAIGHT = CommandType((0,0,0))
CommandType.ARC = CommandType((0,0,0))
CommandType.BEZIER = CommandType((0,0,0))
CommandType.CUSTOM = CommandType((0,0,0))