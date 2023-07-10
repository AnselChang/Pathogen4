from __future__ import annotations
from enum import Enum
from typing import TYPE_CHECKING

from models.project_model import ProjectModel, SerializedProjectState

"""
Stores an ordered list of SerializedProjectState objects to represent
the save history of the project. This can be used for undo/redo.
"""
class ProjectHistoryModel:

    def __init__(self):
        
        # list of serialized project states
        self.history = [] # from oldest to newest
        self.pointer: SerializedProjectState = None # current state. if None, then we're in present

    # save a snapshot of the project as a SerializedProjectState,
    # and add it to the history
    def save(self):

        # if pointer is not None, then we must delete the incompatible future
        # essentially, disables any states that would be accessible through redo
        if self.pointer is not None:
            i = self.history.index(self.pointer)
            self.history = self.history[:i+1] # delete all states after pointer

        currentState = ProjectModel.getInstance().serialize()
        self.history.append(currentState)
        self.pointer = currentState # set pointer to this new save

    # whether undo should be enabled
    def canUndo(self) -> bool:

        # if we're at present and there's history, can undo
        if self.pointer is None and len(self.history) > 0:
            return True
        
        # if we're at some point in history, and there's history before that, can undo
        if self.pointer is not None and self.history.index(self.pointer) > 0:
            return True

        return False
    
    # revert to previous state
    def undo(self):

        # if pointer is None, go to most recent save
        if self.pointer is None:
            if len(self.history) == 0:
                raise Exception("There is no history to undo")
            self.pointer = self.history[-1]
        else: # otherwise, step back one save
            i = self.history.index(self.pointer)
            if i > 0:
                self.pointer = self.history[i-1]
            else:
                raise Exception("Cannot undo past beginning of history")
            
        ProjectModel().getInstance().loadSerializedState(self.pointer)

    # whether redo should be enabled
    def canRedo(self) -> bool:
        # if pointer is None, then it is present and cannot undo
        # if pointer is at end of history, then cannot redo
        return self.pointer is not None and self.history.index(self.pointer) < len(self.history)-1

    # go forward one state
    def redo(self):
            
        # if pointer is None, then we're at the present
        if self.pointer is None:
            raise Exception("Cannot redo past present")

        # otherwise, step forward one save
        i = self.history.index(self.pointer)
        if i < len(self.history)-1:
            self.pointer = self.history[i+1]
        else:
            raise Exception("Cannot redo past end of history")

        ProjectModel().getInstance().loadSerializedState(self.pointer)