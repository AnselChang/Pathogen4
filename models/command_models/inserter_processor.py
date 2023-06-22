from __future__ import annotations
from enum import Enum
from typing import TYPE_CHECKING
from command_creation.command_type import CommandType

from models.command_models.model_based_entity import ModelBasedEntity
from root_container.panel_container.command_block.interfaces import ICommandInserter, ICommandBlock

if TYPE_CHECKING:
    from root_container.panel_container.command_block.full_container import FullContainer
    from root_container.panel_container.command_block.command_block_entity import CommandBlockEntity
    from entity_ui.group.variable_group.variable_container import VariableContainer
    from root_container.panel_container.command_block.custom_command_block_entity import CustomCommandBlockEntity
    from root_container.panel_container.command_block.command_inserter import CommandInserter


"""
Handle the traversal of command inserters for the purpose
of moving commands around to different inserters.
"""

class InserterData:
        def __init__(self, inserter: CommandInserter, before: CommandBlockEntity = None, after: CommandBlockEntity = None):
            
            if not isinstance(inserter, ICommandInserter):
                raise Exception("First argument must be a CommandInserter")
            
            if before is not None and not isinstance(before, ICommandBlock):
                raise Exception("Second argument must be a CommandBlockEntity")
            
            if after is not None and not isinstance(after, ICommandBlock):
                raise Exception("Third argument must be a CommandBlockEntity")
            
            self.inserter = inserter
            self.before = before
            self.after = after

        # displayed [inserter] [before] [after]
        # id set to 0 if before/after is None
        def __repr__(self) -> str:
            idi = id(self.inserter)
            idb = 0 if self.before is None else id(self.before)
            ida = 0 if self.after is None else id(self.after)
            return f"{idi} {idb} {ida}"

class InserterProcessor:

    def __init__(self, fullContainer: FullContainer):
        self.fullContainer = fullContainer
        self.reset()

    def reset(self):
        self.inserters: list[InserterData] = []
        self.closestInserter: CommandInserter = None

    def process(self):        
        self.reset()
        self._generateFlattenedInserters(self.inserters, self.fullContainer)

    # return an ordered list of inserters+ from top to bottom
    # exclude section inserters
    # exclude inserters inside collapsed sections/tasks
    # package with references to commands before and after inserter
    def _generateFlattenedInserters(self, inserters: list[InserterData], mbe: ModelBasedEntity):

        if mbe.getChildVGC() is None:
            return

        children: list[VariableContainer] = mbe.getChildVGC()._children
        for i in range(len(children)):
            
            before = children[i - 1].child if i > 0 else None
            entity = children[i].child
            after = children[i + 1].child if (i < len(children)-1) else None

            if isinstance(entity, ICommandInserter) and not mbe.model.isRootModel():
                inserters.append(InserterData(entity, before, after))
            elif isinstance(entity, ModelBasedEntity):
                self._generateFlattenedInserters(inserters, entity)


    class _Direction(Enum):
        UP = 0
        DOWN = 1

    # return the inserter that is closest to the mouse
    # command is not custom, cannot be moved so that
    # it is rearranged with another non-custom command
    def computeClosestInserter(self, command: CommandBlockEntity) -> CommandInserter:
        y = command.CENTER_Y
        if command.dragOffset < 0:
            self.closestInserter = self._getClosestInserter(command, y, InserterProcessor._Direction.UP)
        else:
            self.closestInserter = self._getClosestInserter(command, y, InserterProcessor._Direction.DOWN)

    def getClosestInserter(self) -> CommandInserter:
        return self.closestInserter

    # return a list of inserters up till the first non-custom command
    def _findUntilNonCustomInserter(self, index: int, direction: _Direction) -> list[InserterData]:
        
        def inc(i: int) -> int:
            if direction == InserterProcessor._Direction.UP:
                return i - 1
            else:
                return i + 1
        
        inserters: list[InserterData] = []

        inserters.append(self.inserters[index])
        index = inc(index)

        while index >= 0 and index < len(self.inserters):
            inserter = self.inserters[index]
            command = inserter.after if direction == InserterProcessor._Direction.UP else inserter.before

            if command.getCommandType() != CommandType.CUSTOM:
                break
            
            inserters.append(inserter)
            index = inc(index)

        return inserters

    def _getClosestInserterToMouseFromList(self, inserters: list[CommandInserter], mouseY: int) -> CommandInserter:
        # find closest inserter to mouse
        closestInserter: CommandInserter = inserters[0]
        closestDistance: int = abs(mouseY - closestInserter.CENTER_Y)
        for inserter in inserters[1:]:
            distance = abs(mouseY - inserter.CENTER_Y)
            if distance < closestDistance:
                closestInserter = inserter
                closestDistance = distance
        return closestInserter
    
    def _getClosestInserter(self, command: CommandBlockEntity, mouseY, direction: _Direction) -> CommandInserter:
        
        def isInserterClosestToCommand(inserterData: InserterData) -> bool:
            if direction == InserterProcessor._Direction.UP:
                return inserterData.after is command
            else:
                return inserterData.before is command

        # whether command is custom
        isCustom: bool = command.getCommandType() == CommandType.CUSTOM

        # index of inserter that is closest to command
        indexes = [i for i in range(len(self.inserters)) if isInserterClosestToCommand(self.inserters[i])]
        if len(indexes) != 1:
            raise Exception("Expected exactly one inserter to be closest to command")
        index = indexes[0]

        # If command is non-custom, filter out inserters that would
        # cause the command to be rearranged with another non-custom command
        inserterCandidates: list[InserterData] = []
        if isCustom:
            if direction == InserterProcessor._Direction.UP:
                inserterCandidates = self.inserters[:index+1]
            else:
                inserterCandidates = self.inserters[index:]
        else:
            inserterCandidates = self._findUntilNonCustomInserter(index, direction)

        # convert candidates to raw inserters
        inserters: list[CommandInserter] = [inserterData.inserter for inserterData in inserterCandidates]

        # return closest inserter to mouse
        return self._getClosestInserterToMouseFromList(inserters, mouseY)