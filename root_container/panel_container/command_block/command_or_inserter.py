from data_structures.linked_list import LinkedListNode

class CommandOrInserter(LinkedListNode['CommandOrInserter']):

    def __init__(self):
        super().__init__()

        self.WIDTH_PERCENT_OF_PANEL = 0.95
    
    # Called when linked list position changes. Update parent and children entity relationships
    def onUpdateLinkedListPosition(self):
        self._parent = self.getPrevious()

        # remove the existing next command/inserter, if any
        self._children = [child for child in self._children if isinstance(child, CommandOrInserter)]

        if self.getNext() is not None:
            self._children.append(self.getNext())