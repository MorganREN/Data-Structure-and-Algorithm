from enum import Enum
import config

class hashset:
    def __init__(self):
        # TODO: create initial hash table
        self.verbose = config.verbose
        self.mode = config.mode
        self.hash_table_size = config.init_size
        self.hashtable = [None] * self.hash_table_size
        self.count_collision = 0
        self.num = 0 # Count the current number of inserted values
        self.load_factor = 0.75 # Used to expand the hash table the number of the value is too much
        self.second_prime = self.lastPrime(self.hash_table_size)  # Used for the second hash function of double hash
        self.hashtable_linked = [SignLinklist() for x in range(self.hash_table_size)]
                
    # Helper functions for finding prime numbers
    def isPrime(self, n):
        i = 2
        while i * i < n:
            if n % i == 0:
                return False
            i = i + 1
        return True
        
    def nextPrime(self, n):
        while not self.isPrime(n):
            n = n + 1
        return n

    def lastPrime(self, n):
        n = n - 1
        while not self.isPrime(n):
            n = n - 1
        return n

    def rehash(self):
        self.hash_table_size = self.num * 2
        temp = self.hashtable[:]
        self.hashtable = [None] * self.hash_table_size
        for i in range(len(temp)):
            self.hashtable[i] = temp[i]

    def hashfunction(self, value):
        # The polynomial hash code
        if self.mode < 4:
            p = 53  # Better for inputs which contain upper and lower cases
            power_of_p = 1
            count_char = 0
            for letter in value:
                count_char = ((count_char + (ord(letter) - ord('a') + 1) * power_of_p) % self.hash_table_size)
                power_of_p = (power_of_p * p) % self.hash_table_size
            return int(count_char)

        # The easiest way, just sum up the ascii code of each letters
        else:
            count_char = 0
            for letter in value:
                count_char += ord(letter)
            length = len(str(count_char))
            if length > 3:
                mid_int = 100 * int((str(count_char)[length // 2 - 1])) \
                          + 10 * int((str(count_char)[length // 2])) \
                          + 1 * int((str(count_char)[length // 2 + 1]))
            else:
                mid_int = count_char
            return mid_int % self.hash_table_size

    # Rehashing function for the linear probing
    def more_linear_hash(self, value):
        return (value + 1) % self.hash_table_size

    # Rehashing function for the quadratic probing
    def more_quad_hash(self, value, i):
        return (value + i ** 2) % self.hash_table_size

    # Rehashing function for the double hash probing
    def double_hash(self, value, num):
        second_Prime = self.second_prime
        return (value % self.hash_table_size + num * (value % second_Prime)) % self.hash_table_size



    def insert(self, value):
        # TODO code for inserting into  hash table
        hash_value = self.hashfunction(value)
        # Using the separate chaining method to insert value
        if self.mode == 3 or self.mode == 7:
            # If the value has been found in the linked list, then just return
            if self.find(value):
                return
            # else append the value
            else:
                self.hashtable_linked[hash_value].append(value)
                self.num += 1
        # Open addressing method
        else:
            if self.hashtable[hash_value] is None:
                pass
            elif self.hashtable[hash_value] == value:
                pass
            else:
                # Insert the value in linear probing way
                if self.mode == 0 or self.mode == 4:
                    self.count_collision += 1
                    hash_value = self.more_linear_hash(hash_value)
                    while (self.hashtable[hash_value] is not None) and (self.hashtable[hash_value] != value):
                        self.count_collision += 1
                        hash_value = self.more_linear_hash(hash_value)
                # Insert the value in quadratic probing way
                elif self.mode == 1 or self.mode == 5:
                    self.count_collision += 1
                    i = 1
                    hash_value = self.more_quad_hash(hash_value, i)
                    while (self.hashtable[hash_value] is not None) and (self.hashtable[hash_value] != value):
                        self.count_collision += 1
                        i += 1
                        hash_value = self.more_quad_hash(hash_value, i)
                # Insert the value in double hash way
                elif self.mode == 2 or self.mode == 6:
                    self.count_collision += 1
                    i = 1
                    first_hash_value = hash_value
                    hash_value = self.double_hash(first_hash_value, i)
                    while (self.hashtable[hash_value] is not None) and (self.hashtable[hash_value] != value):
                        self.count_collision += 1
                        i += 1
                        hash_value = self.double_hash(first_hash_value, i)
            # The while loop stops when the current place is empty or equal to the target value
            self.hashtable[hash_value] = value
            self.num += 1  # When a value is inserted, the number should add 1
            # IF the current load factor is greater that 0.75, then do rehash
            if (self.num / self.hash_table_size) > self.load_factor:
                self.rehash()
        
    def find(self, value):
        # TODO code for looking up in hash table
        hash_value = self.hashfunction(value)
        first_hash = hash_value  # Sometimes useful
        # Find the value like the separate chaining method
        if self.mode == 3 or self.mode == 7:
            return self.hashtable_linked[hash_value].find(value)
        else:
            if self.hashtable[hash_value] is None:
                return False
            elif self.hashtable[hash_value] == value:
                return True
            else:
                # Search the value in linear probing way
                if self.mode == 0 or self.mode == 4:
                    hash_value = self.more_linear_hash(hash_value)
                    while (self.hashtable[hash_value] is not None) and (self.hashtable[hash_value] != value):
                        hash_value = self.more_linear_hash(hash_value)
                        if hash_value == first_hash:
                            return False
                # Search the value in quadratic probing way
                elif self.mode == 1 or self.mode == 5:
                    i = 1
                    hash_value = self.more_quad_hash(hash_value, i)
                    while (self.hashtable[hash_value] is not None) and (self.hashtable[hash_value] != value):
                        i += 1
                        hash_value = self.more_quad_hash(hash_value, i)
                        if hash_value == first_hash:
                            return False
                # Search the value in double hash way
                elif self.mode == 2 or self.mode == 6:
                    i = 1
                    hash_value = self.double_hash(first_hash, i)
                    while (self.hashtable[hash_value] is not None) and (self.hashtable[hash_value] != value):
                        i += 1
                        hash_value = self.double_hash(first_hash, i)
                        if hash_value == first_hash:
                            return False
                # Rehashing function stopped when the current searching place is none or equal to the target value
                if self.hashtable[hash_value] is None:
                    return False
                elif self.hashtable[hash_value] == value:
                    return True


        
    def print_set(self):
        # Print the set if choose the separate chaining
        if self.mode == 3 or self.mode == 7:
            for i in range(len(self.hashtable_linked)):
                if self.hashtable_linked[i] is not None:
                    print(" " + self.hashtable_linked[i].__repr__())
        # Open method manner for printing
        else:
            print("Hashset: ")
            for i in range(len(self.hashtable)):
                if self.hashtable[i] is not None:
                    print(" " + self.hashtable[i])
        
    def print_stats(self):
        if self.verbose == 0:
            return
        elif self.verbose == 1:
            print("The number of collision: " + str(self.count_collision))
        elif self.verbose == 2:
            print("The number of collision: " + str(self.count_collision))
            print("The average number of collision per insert: " + str(self.count_collision / self.num))
        elif self.verbose == 3:
            print("The number of collision: " + str(self.count_collision))
            print("The average number of collision per insert: " + str(self.count_collision / self.num))
            print("The size of the hashtable: " + str(self.hash_table_size))
        elif self.verbose == 4:
            print("The number of collision: " + str(self.count_collision))
            print("The average number of collision per insert: " + str(self.count_collision / self.num))
            print("The size of the hashtable: " + str(self.hash_table_size))
            print("The number of values inserted: " + str(self.num))

        
# Hashing Modes
class HashingModes(Enum):
    HASH_1_LINEAR_PROBING=0
    HASH_1_QUADRATIC_PROBING=1
    HASH_1_DOUBLE_HASHING=2
    HASH_1_SEPARATE_CHAINING=3
    HASH_2_LINEAR_PROBING=4
    HASH_2_QUADRATIC_PROBING=5
    HASH_2_DOUBLE_HASHING=6
    HASH_2_SEPARATE_CHAINING=7


# A new class used to store value for separate chaining
class SignLinklist:
    # The Node Class
    class Node:
        def __init__(self, item):
            self.item = item
            self.next = None

        def __str__(self):
            return str(self.item)

    # The iterable linked list class
    class LinkedListIterator:
        def __init__(self, node):
            self.node = node

        def __next__(self):
            if self.node:
                cur_node = self.node
                self.node = cur_node.next
                return cur_node.item
            else:
                raise StopIteration

        def __iter__(self):
            return self

    def __init__(self, iterable=None):
        self.head = None
        self.tail = None
        if iterable:
            self.extend(iterable)

    # Append node
    def append(self, obj):
        node = SignLinklist.Node(obj)
        if not self.head:
            self.head = node
            self.tail = node
        else:
            self.tail.next = node
            self.tail = node

    # Find node
    def find(self, obj):
        for n in self:
            if n == obj:
                return True
        else:
            return False

    # Iterator the linked list
    def __iter__(self):
        return self.LinkedListIterator(self.head)

    # print the link list
    def __repr__(self):
        return '<<' + ','.join(map(str, self)) + '>>'
