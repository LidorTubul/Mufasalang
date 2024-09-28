import math
import string
from typing import Union

"""
Author: Lidor Tubul
"""


class Shmuple:

    def __init__(self, *args):
        """
        initializes a Shmuple with the provided arguments as a tuple.
        :param args: elements in the tuple.
        """
        self.myTuple = tuple(args)

    def sortuple(self):
        """
        sorts the elements of a Shmuple and returns a new sorted Shmuple.
        :return: new Shmuple with sorted elements.
        """
        newt = tuple(sorted(self.myTuple))
        return Shmuple(*newt)

    def Add(self, b):
        """
        :param b: Shmuple object
        :return: new Shmuple Object with Shmuple b added 
        """
        return Shmuple(*(self.myTuple + b.myTuple))

    def getitem(self, index: int):
        """
        retrieves an element at a given index from the Shmuple.

        :param index: The index.
        :return: element at the given index.
        """
        try:
            return self.myTuple.__getitem__(index)
        except IndexError:
            raise IndexError(f"Not valid index {index} for shmuple with size {self.myTuple.__len__()}")
            # return ""

    def Index(self, item):
        """
        finds the index of the first appearece of an item in the Shmuple.

        :param item: The item to search for.
        :return: index of the first appearece, or -1 if not found.
        """
        for c in range(len(self.myTuple) - 1):
            if self.getitem(c) == item:
                return c
        return -1

    def Length(self):
        """
        returns number of elements in the Shmuple.

        :return: length of the Shmuple.
        """
        return len(self.myTuple)

    def __repr__(self):
        """

        :return: string representation of the Shmuple.
        """
        lis = []
        for i in self.myTuple:
            lis.append(i)
        newtup = tuple(lis)
        return newtup.__repr__()


class Arrays:

    def __init__(self, size=0):
        """
        initializes Arrays with a given size.

        :param size: the size of the array (default is 0).
        """
        if type(size) is not int:
            raise ValueError("size of array must be an integer")
        self.size = size
        self.array = [0] * self.size

    def check_index(self, index: int):
        """
        checks if an index is valid.

        :param index: the index to check.
        :return: True if the index is valid.
        """
        if index < 0:
            raise IndexError("Index out of bounds (can't be a negative number)")
        elif index >= self.size:  # Fixing this condition
            raise IndexError("Index out of bounds (can't be greater than or equal to the size of the array)")

        return True

    def length(self):
        """

        :return: size of the array.
        """
        return self.size

    def at(self, index: int):
        """
        return element at the given index in the array.

        :param index: index of the element we want.
        :return: element at the given index.
        """
        if not self.check_index(index):
            return
        return self.array[index]

    def insert(self, index: int, item):
        """
        inserts an item at given index in the array.

        :param index: index at which to insert the item.
        :param item: item to insert into the array.
        """
        if not self.check_index(index):
            return
        self.array[index] = item

    def remove(self, index: int):
        """
        removes the element given index from the array.

        :param index: the index of element we want to remove.
        """
        if not self.check_index(index):
            return
        if self.size == 0:
            raise IndexError("Index out of bounds")

        newarray = []

        for i in range(self.size):
            if i == index:
                continue
            newarray.append(self.array[i])

        self.size -= 1
        self.array = newarray

    def add(self, item):
        """
        adds an item to the end of the array.

        :param item: the item to add.
        """
        new_array = [0] * (self.size + 1)

        for i in range(self.size):
            new_array[i] = self.array[i]

        # Add the new item to the end
        new_array[self.size] = item

        # Update the size and the array
        self.size += 1
        self.array = new_array

    def display(self):
        """
        Returns a string of the array's contents.

        :return: String of the array.
        """
        return str(self.array)


class StringBeans:

    def __init__(self, string_=""):
        """
        initializes a StringBeans with a given string.

        :param string_: The initialized StringBean(default is an empty string).
        """
        self.string_ = string_

    def splitBeans(self, a: str):
        """

        :param a: a string which be used to split the StringBean
        :return: an array of stringBeans from type Arrays. if splitter 'a' not exist will return an array which contain
        the original StringBean
        """
        lis = self.string_.split(a)
        length = len(lis)
        y = Arrays(length)
        index = 0
        for cell in lis:
            y.insert(item=cell, index=index)
            index += 1

        return y

    def Replace(self, old: str, new: str):
        """
        replaces all instances of a given value in the string with another value.

        :param old: value to be replaced.
        :param new: value to replace with.
        :return: modified string with the replacements.
        """
        if not self.string_.__contains__(old):
            return self.string_
        result = []
        i = 0
        while i < len(self.string_):
            if self.string_[i:i + len(old)] == old:
                result.append(new)
                i += len(old)
            else:
                result.append(self.string_[i])
                i += 1
        self.string_ = ''.join(result)
        return self.string_

    def allUpper(self):
        """
        checks if all the characters in the string are uppercase.

        :return: True if all characters are uppercase.
        """
        for char in self.string_:
            if char in string.digits or char in string.punctuation:
                continue
            if 'a' <= char <= 'z':
                return False
        return True

    def allLower(self):
        """
        checks if all the characters in a string are lowercase

        :return: True if all characters are lowercase.
        """
        for char in self.string_:
            if char in string.digits or char in string.punctuation:
                continue
            if 'A' <= char <= 'Z':
                return False
        return True

    def Conjoin(self, str2):
        """
        joins together two different strings into one

        :param str2: string to join with the first one.
        """
        self.string_ = self.string_ + str2

    def show(self):
        """
        displays given string.
        """
        print(self.string_)

    def __copy__(self):
        """
        creates a copy of the StringBeans object.

        :return: new StringBeans object that is a copy of itself.
        """
        return StringBeans(self.string_)

    def __repr__(self):
        """
        returns a string representation of the StringBeans object.

        :return: string representing the StringBeans object.
        """
        return f'"{self.string_}"'


class mathforlenguage:
    def __init__(self):
        """
        initializes a mathforlenguage.
        """
        self.Dict = {}

    def getDict(self):
        """

        :return: The dictionary used by mathforlenguage.
        """
        return self.Dict

    def updateDict(self, Dict):
        """
        updates the dictionary used by mathforlenguage.
        """
        self.Dict = Dict

    def Add(self, x: Union[int, float], y: Union[int, float]):
        """adds two numbers together"""
        return x + y

    def Subtract(self, x: Union[int, float], y: Union[int, float]):
        """subtracts two numbers together"""
        return x - y

    def Multiply(self, x: Union[int, float], y: Union[int, float]):
        """multiplies two numbers together"""
        return x * y

    def Divide(self, x: Union[int, float], y: Union[int, float]):
        """divides two numbers together"""
        return x / y

    def Pow(self, x: Union[int, float], y: Union[int, float]):
        """multiplies two numbers together"""
        return x ** y

    def squareRoot(self, x: Union[int, float]):
        """return the squared root of a number"""
        return math.sqrt(x)

    def Min(self, x: Union[int, float], y: Union[int, float]):
        """return the smallest number"""
        return x if x < y else y

    def Max(self, x: Union[int, float], y: Union[int, float]):
        """return the largest number"""
        return x if x > y else y

    def assign(self, x: str, y):
        """asign a value to a varible in the dictionary"""
        self.Dict[x] = y

    def Equal(self, x, y):
        """
        check if two values are equel
        
        handels different types of comparisons between numbers and literals
        """
        if type(x) is type(5) and type(y) is type(5):
            return x == y

        if type(x) is type(5) and type(y) is type(""):
            raise TypeError("action can't be between a number and a literal. the literal must come first")

        if type(x) is type("") and type(y) is type(5):
            return self.Dict[x] == y

        if type(x) is type("") and type(y) is type(""):
            return self.Dict[x] == self.Dict[y]

    def notEqual(self, x, y):
        """
        check if two values are not equel
        
        uses the Equal function and returns the oposite result
        """
        return not self.Equal(x, y)

    def greater(self, x: Union[int, float], y: Union[int, float]):
        """
        check if first number is greater than the second one
        :return: True if x is greater than y, False otherwize
        """
        return x > y

    def less(self, x: Union[int, float], y: Union[int, float]):
        """
        chek if first number is less than second
        :return: True if x is les than y, False otherwize
        """
        return x < y

    def Or(self, x: bool, y: bool):
        """
        return logical OR of two booleans
        :return: True if ether x or y is True, False otherwize
        """
        return x or y

    def And(self, x: bool, y: bool):
        """
        return logical AND of two booleans
        :return: True if both x and y are True, False otherwize
        """
        return x and y


if __name__ == "__main__":
    pass
