from __future__ import annotations
from enum import Enum
from typing import TYPE_CHECKING

from root_container.panel_container.command_block.custom_command_block_entity import CustomCommandBlockEntity
from models.command_models.model_based_entity import ModelBasedEntity
from root_container.panel_container.command_block.command_inserter import CommandInserter

if TYPE_CHECKING:
    from root_container.panel_container.command_block.command_block_entity import CommandBlockEntity
    from entity_ui.group.variable_group.variable_container import VariableContainer

"""
Handle the traversal of command inserters for the purpose
of moving commands around to different inserters.
"""

class InserterData:
        def __init__(self, inserter: CommandInserter, before: CommandBlockEntity = None, after: CommandBlockEntity = None):
            
            if not isinstance(inserter, CommandInserter):
                raise Exception("First argument must be a CommandInserter")
            
            if before is not None and not isinstance(before, CommandBlockEntity):
                raise Exception("Second argument must be a CommandBlockEntity")
            
            if after is not None and not isinstance(after, CommandBlockEntity):
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

    def __init__(self, mbe: ModelBasedEntity):
        self.mbe = mbe

        self.inserters: list[InserterData] = []
        self._generateFlattenedInserters(self.inserters, mbe)

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

            if isinstance(entity, CommandInserter) and not mbe.model.isRootModel():
                inserters.append(InserterData(entity, before, after))
            elif isinstance(entity, ModelBasedEntity):
                self._generateFlattenedInserters(inserters, entity)


    class _Direction(Enum):
        UP = 0
        DOWN = 1

    # return the inserter that is closest to the mouse
    # command is not custom, cannot be moved so that
    # it is rearranged with another non-custom command
    def getClosestInserter(self, command: CommandBlockEntity, mouseY) -> CommandInserter:
        cy = command.CENTER_Y
        if mouseY < cy:
            return self._getClosestInserter(command, mouseY, InserterProcessor._Direction.UP)
        else:
            return self._getClosestInserter(command, mouseY, InserterProcessor._Direction.DOWN)

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

            if not isinstance(command, CustomCommandBlockEntity):
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
        isCustom: bool = isinstance(command, CustomCommandBlockEntity)

        # index of inserter that is closest to command
        indexes = [i for i in len(self.inserters) if isInserterClosestToCommand(self.inserters[i])]
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