
"""
An interface for ProjectHistoryModel
Stores an ordered list of SerializedProjectState objects to represent
the save history of the project. This can be used for undo/redo.
"""
class ProjectHistoryInterface:

    _INSTANCE = None

    def initInstance(instance: 'ProjectHistoryInterface'):
        ProjectHistoryInterface._INSTANCE = instance

    def getInstance() -> 'ProjectHistoryInterface':
        if ProjectHistoryInterface._INSTANCE is None:
            raise Exception("ProjectHistoryInterface has not been initialized")

        return ProjectHistoryInterface._INSTANCE

    # save a snapshot of the project as a SerializedProjectState,
    # and add it to the history
    def save(self):
        raise NotImplementedError

    # whether undo should be enabled
    def canUndo(self) -> bool:
        raise NotImplementedError
    
    # revert to previous state
    def undo(self):
        raise NotImplementedError

    # whether redo should be enabled
    def canRedo(self) -> bool:
        raise NotImplementedError
    
    # go forward one state
    def redo(self):
        raise NotImplementedError