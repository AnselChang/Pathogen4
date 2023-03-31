from typing import TypeVar, Generic

T = TypeVar('T')
class LinkedListNode(Generic[T]):
    def __init__(self):
        self._next: T = None
        self._prev: T = None

    def getPrevious(self) -> T:
        return self._prev
    
    def getNext(self) -> T:
        return self._next

class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def addToBeginning(self, node):
        
        if self.head is None:
            self.head = node
            self.tail = node
        else:
            node._next = self.head
            self.head._prev = node
            self.head = node

    def addToEnd(self, node):

        if self.head is None:
            self.head = node
            self.tail = node
        else:
            self.tail._next = node
            node._prev = self.tail
            self.tail = node

    def insertBeforeEnd(self, node):
        self.insertBefore(self.tail, node)

    def insertBefore(self, node, newNode):

        if self.head is None:
            return
        if self.head is node:
            self.addToBeginning(newNode)
            return
                
        newNode._prev = node._prev
        node._prev._next = newNode
        newNode._next = node
        node._prev = newNode

    def insertAfter(self, node, newNode):

        if self.tail is node:
            self.addToEnd(newNode)
            return

        newNode._next = node._next
        node._next._prev = newNode
        node._next = newNode
        newNode._prev = node

    def remove(self, node):

        if self.head is self.tail:
            self.head = None
            self.tail = None
        elif self.head is node:
            self.head = self.head.__next
            self.head.__prev = None
        elif self.tail is node:
            self.tail = self.tail.__prev
            self.tail.__next = None
        else:
            node._prev._next = node._next
            node._next._prev = node._prev

    def printList(self):
        current = self.head
        while current is not None:
            print(current)
            current = current._next

        print()