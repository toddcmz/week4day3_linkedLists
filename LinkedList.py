from Node import Node

# see line 92 for HW assignment 1 implemented - add a list of items to linked list
class LinkedList:

    def __init__(self):
        self.head = None
    
    def add_node(self, value):
        node = Node(value)
        if not self.head:
            self.head = node
        else:
            current_node=self.head
            while current_node.right:
                current_node = current_node.right
            current_node.right = node

    # see usage of __iter__ below in conjuction with __repr__
    def __iter__(self):
        current_node = self.head
        while current_node:
            yield current_node
            current_node = current_node.right
            
    # this will return some sort of user friendly message when we call just the instance,
    # specifically within a print. If we call print(classInstance) otherwise we get the place
    # in memory. If we include a __repr__ method, then print(classInstance) will return whatever
    # is in repr. This only works as written, with the node in self loop because of the __iter__ method
    # added above. __iter__ let's us call self alone. 
    def __repr__(self): 
        nodes = []
        for node in self:
            nodes.append(node.value)
        return ' -> '.join(nodes)

    # let's say we want to add a node to the middle of the list - need to update pointers.
    def insert_node(self, target, value):
        new_node = Node(value)
        if self.head:
            # we have the __iter__ dunder method that lets us loop through all our nodes.
            for node in self:
                if node.value == target:
                    right_node = node.right
                    node.right = new_node
                    new_node.right = right_node
        else:
            print("empty list")

    def remove_node(self, value):
        if value == self.head.value:
            self.head = self.head.right
        else:
            for node in self:
                if node.right.value == value:
                    node.right = node.right.right
                    return

    def insert_prior(self, target, value):
        new_node = Node(value)
        if self.head:
            # we have the __iter__ dunder method that lets us loop through all our nodes.
            if self.head.value == target:
                right_node = self.head
                self.head = new_node
                new_node.right = right_node
            for node in self:
                if node.right.value == target:
                    right_node = node.right
                    node.right = new_node
                    new_node.right = right_node
                    return
        else:
            print("empty list")

    def get_tail(self):
        # for node in self:
        #     pass
        # return(node.value)
        current_node = self.head
        while current_node.right:
            current_node = current_node.right
        return current_node.value
    
    def remove_tail(self):
        current_node = self.head
        if current_node.right:
            while current_node.right.right:
                current_node = current_node.right
            current_node.right = None

    # add each element in this list to the current linked list - hw assignment one
    def add_list(self, this_list):
        for ele in this_list:
            self.add_node(ele)

    # also add an evolution chain with a linked list of every pokemon in the evolution chain.
    # head is base, then add node for each level available.

# linked_list = LinkedList()
# linked_list.add_node("Sunday")
# linked_list.add_node("Monday")
# linked_list.add_node("Tuesday")
# linked_list.add_node("Thursday")

# print(linked_list)
# # he initially wrote this, which is ignoring the linked_list class, just trying to
# # show how nodes are working. then we went to write it for real using linked_list
# # node = Node(1)
# # node.right = Node(2)
# # node.right.right = Node(3)
# linked_list.insert_node("Tuesday", "Wednesday")
# print(linked_list)

# linked_list.add_node("Spazday")
# print(linked_list)

# linked_list.remove_node("Monday")
# print(linked_list)

# linked_list.insert_prior("Sunday", "PreSpazday")
# print(linked_list)

# print(linked_list.get_tail())

# linked_list.remove_tail()

# print(linked_list)

# my_list = ["plus1", "plus2", "plus3"]

# linked_list.add_list(my_list)

# print(linked_list)

