import config
import sys

sys.setrecursionlimit(2000)  # set the limit of recursion for having a successful test

class bstree:
    def __init__(self, value = None):
        self.value = value
        self.left = None
        self.right = None
        self.count_comp_insert = 1 # Count the number of comparisons when inserting
        self.count_comp_find = 0 # Count the number of comparisons when finding
        self.find_recure = 0 # Used to count the times of recursive calling of find function
        self.count_find = self.count_comp_find - self.find_recure # The actual number of words for finding
        self.height = 0
        self.verbose = config.verbose

    def size(self):
        if self.value is not None:
            # Check whether the left node and right node are none
            if (self.left is not None) and (self.right is not None):
                return 1 + self.left.size() + self.right.size()
            elif (self.left is not None) and (self.right is None):
                return 1 + self.left.size()
            elif (self.left is None) and (self.right is not None):
                return 1 + self.right.size()
            elif (self.left is None) and (self.right is None):
                return 1
        else:
            return 0

    def tree(self):
        return self.value is not None
        
    def insert(self, value):
        # If the root node is None, then insert the value here
        if self.value is None:
            self.value = value
        # If the root node is not None, then compare it with the value
        else:
            self.count_comp_insert += 1 # when compare, the number of comparisons for insert increase
            # The root node's value is the target value, then do nothing
            if self.value == value:
                return
            # root node's value is greater than the target value, then go to the left node
            elif self.value > value:
                if self.left is None:
                    self.left = bstree(value)
                else:
                    self.left.insert(value)
            # root node's value is greater than the target value, then go to the left node
            elif self.value < value:
                if self.right is None:
                    self.right = bstree(value)
                else:
                    self.right.insert(value)



    def find(self, value):
        # Return False if the root node is None
        if self.value is None:
            return False
        else:
            self.count_comp_find += 1 # when compare, the number of comparisons for find increase
            if self.value == value:
                return True
            # Find in the left node if the value is less than the current node
            elif self.value > value:
                if self.left is None:
                    return False
                else:
                    self.find_recure += 1 # Only increase when find is called recursively
                    return self.left.find(value)
            # Find in the right node if the value is greater than the current node
            elif self.value < value:
                if self.right is None:
                    return False
                else:
                    self.find_recure += 1 # Only increase when find is called recursively
                    return self.right.find(value)

        
    # You can update this if you want
    def print_set_recursive(self,depth):
        if depth == 0:
            self.height = depth
        if self.tree():
            for i in range(depth):
                print(" ", end='')
            print("%s" % self.value)
            if self.left is not None:
                self.height = max(self.height, depth + 1)
                self.left.print_set_recursive(depth + 1)
            else:
                for i in range(depth):
                    print(" ", end='')
                print("%s" % "lEFT_NODE")

            if self.right is not None:
                self.height = max(self.height, depth + 1)
                self.right.print_set_recursive(depth + 1)
            else:
                for i in range(depth):
                    print(" ", end='')
                print("%s" % "RIGHT_NODE")


    # You can update this if you want
    def print_set(self):
        print("Tree:\n")
        self.print_set_recursive(0)
        
    def print_stats(self):
        # TODO update code to record and print statistic
        if self.verbose == 0:
            return
        elif self.verbose == 1:
            print("The height of the tree is : " + str(self.height))
        elif self.verbose == 2:
            print("The height of the tree is : " + str(self.height))
            print("The average number of comparisons per insert is : " + str(self.count_comp_insert / self.size()))
        elif self.verbose == 3:
            print("The height of the tree is : " + str(self.height))
            print("The average number of comparisons per insert is : " + str(self.count_comp_insert / self.size()))
            print("The average number of comparisons per find is : " + str(self.count_comp_find / self.count_find))
