class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None

class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def addToBeginning(self, node):

        node.next = None
        node.prev = None
        
        if self.head is None:
            self.head = node
            self.tail = node
        else:
            node.next = self.head
            self.head.prev = node
            self.head = node

    def addToEnd(self, node):

        node.next = None
        node.prev = None

        if self.head is None:
            self.head = node
            self.tail = node
        else:
            self.tail.next = node
            node.prev = self.tail
            self.tail = node

    def insertBefore(self, node, newNode):

        newNode.next = None
        newNode.prev = None

        if self.head is None:
            return
        if self.head == node:
            self.addToBeginning(newNode)
            return

        current = self.head
        while current.next is not None:
            if current.next == node:
                newNode.next = current.next
                current.next.prev = newNode
                current.next = newNode
                newNode.prev = current
                return
            current = current.next

    def insertAfter(self, node, newNode):

        newNode.next = None
        newNode.prev = None

        if self.tail == node:
            self.addToEnd(newNode)
            return

        newNode.next = node.next
        node.next.prev = newNode
        node.next = newNode
        newNode.prev = node

    def printList(self):
        current = self.head
        while current is not None:
            print(current)
            current = current.next

        print()

if __name__ == "__main__":

    # Test case 1: Creating a new linked list and adding nodes to it
    my_list = LinkedList()
    node1 = Node("apple")
    node2 = Node("banana")
    node3 = Node("cherry")
    my_list.addToEnd(node1)
    my_list.addToEnd(node2)
    my_list.addToEnd(node3)
    assert my_list.head == node1
    assert my_list.tail == node3
    my_list.printList()

    # Test case 2: Adding nodes to the beginning of the list
    node4 = Node("date")
    node5 = Node("elderberry")
    my_list.addToBeginning(node4)
    my_list.addToBeginning(node5)
    assert my_list.head == node5
    assert my_list.tail == node3
    my_list.printList()

    # Test case 3: Inserting a node before an existing node
    node6 = Node("cantaloupe")
    my_list.insertBefore(node2, node6)
    assert node1.next == node6
    assert node6.prev == node1
    assert node6.next == node2
    assert node2.prev == node6
    my_list.printList()

    # Test case 4: Inserting a node after an existing node
    node7 = Node("fig")
    my_list.insertAfter(node3, node7)
    assert node3.next == node7
    assert node7.prev == node3
    assert node7.next is None
    assert my_list.tail == node7
    my_list.printList()