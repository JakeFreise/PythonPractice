class Heap:
    heap = []
    treetable = dict()

    def getLeftchild(node):
        return 2*node+1

    def getRightchild(node):
        return 2*node+2

    def parent(node):
        if node == 0:
            return None
        elif node == 1:
            return 0
        return int((node-1)/2)

    #given node positions and their respective tree, swap the two values
    def swap(self, node1, node2):
        array = type(self).heap
        table = type(self).treetable
        temp = array[node1]
        temp2 = array[node2]

        if temp in table:
            if node1 in table[temp]:
                table[temp].remove(node1)
                table[temp].add(node2)
            
        if temp2 in table:
            if node2 in table[temp2]:
                table[temp2].remove(node2)
                table[temp2].add(node1)
        
        array[node1] = temp2
        array[node2] = temp

    #take a node and bubble up if parent is smaller
    def bubbleup(self, node):
        array = type(self).heap
        parent = type(self).parent(node)
        if parent != None:
            if array[parent] > array[node]:
                self.swap(parent, node)
                self.bubbleup(parent)

    #take a node and bubble down if children are bigger. Favors left node in tie
    def bubbledown(self, node):
        array = type(self).heap
        leftchild = type(self).getLeftchild(node)
        rightchild = type(self).getRightchild(node)
        lastIndex = len(array)-1
        
        if leftchild <= lastIndex: #checkbounds
            if array[leftchild] != None: #check if left not null
                if array[leftchild] < array[node]: #check if leftchild is smaller than node
                    if array[rightchild] != None: #check if right is not null
                        if(array[leftchild] <= array[rightchild]): #if left is smaller then right bubble there
                            self.swap(node, leftchild)
                            self.bubbledown(leftchild)
                        else:
                            self.swap(node, rightchild)
                            self.bubbledown(rightchild)
                    else:
                        self.swap(node, leftchild)
                        self.bubbledown(leftchild)
                elif rightchild <= lastIndex: #checkbounds
                    if array[rightchild] != None: #check if right is not null
                        if array[rightchild] < array[node]: #check if right is smaller than node
                            sekl.swap(node, rightchild)
                            self.bubbledown(rightchild)

    #insert a value into the heap        
    def insert(self, value):
        array = type(self).heap
        table = type(self).treetable
        array.append(value)
        arrayLength = len(array)-1
        if value in table:
            hashset = table[value]
            hashset.add(arrayLength)
            table[value] = hashset
        else:
            table[value] = {arrayLength}
        self.bubbleup(arrayLength)

    #removes root value of heap
    def poll(self):
        array = type(self).heap
        table = type(self).treetable
        lastIndex = len(array)-1
        if(lastIndex >= 0):
            value = array[0] #key
            if value in table: #if key is in table
                table[ alue].remove(0) #remove the primary node(0)
                if len(table[value]) is 0:
                    del table[value]
            self.swap(0, lastIndex)
            array.pop()
            if(lastIndex-1 >= 0):
                self.bubbledown(0)

    #removes one instance of the given value from heap       
    def remove(self, value):
        array = type(self).heap
        table = type(self).treetable
        lastIndex = len(array)-1
        if value in table:
            index = table[value].pop()
            if len(table[value]) is 0:
                del table[value]
            self.swap(index, lastIndex)
            array.pop()
            if(index < lastIndex-1):
                self.bubbledown(index)
                self.bubbleup(index)

tree = Heap()
counter = 0
from random import random
while counter < 10:
    tree.insert(int(random()*10))
    counter+=1
print(tree.heap)
print(tree.treetable)
