class LinkedListNode:
    def __init__(self):
        self._next = None
        self._prev = None

    def getPrevious(self):
        return self._prev
    
    def getNext(self):
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

    def insertBefore(self, node, newNode):

        if self.head is None:
            return
        if self.head == node:
            self.addToBeginning(newNode)
            return
                
        newNode._prev = node._prev
        node._prev._next = newNode
        newNode._next = node
        node._prev = newNode

    def insertAfter(self, node, newNode):

        if self.tail == node:
            self.addToEnd(newNode)
            return

        newNode._next = node._next
        node._next._prev = newNode
        node._next = newNode
        newNode._prev = node

    def printList(self):
        current = self.head
        while current is not None:
            print(current)
            current = current._next

        print()