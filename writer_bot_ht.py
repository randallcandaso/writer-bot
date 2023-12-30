'''

File: writer_bot_ht.py
Author: Randall Candaso
Course/Section: CSC 120-002
Description: Program takes a file of text and creates a
hash table that will be used to generate automated text
based off the first n number of words.

'''

import random
import sys

class Hashtable:
    '''

    Creates a hashtable that inserts keys and values into
    specific indexes of a desired table length.

    '''
    def __init__(self, size):
        '''

        Initializes the hashtable by creating a list
        of a length of the inputted size.

        :param size: desired size of hashtable
        '''
        self._size = size
        self._pairs = [None] * size

    def _hash(self, key):
        '''

        Calculates the index of a key.

        :param key: key to be inserted into
        the table
        :return: an index number
        '''
        p = 0
        for c in key:
            p = 31*p + ord(c)
        return p % self._size

    def put(self, key, value):
        '''

        Inserts a key and its corresponding
        value into the table using the _hash()
        function.

        :param key: key to be inserted into
        the table
        :param value: corresponding value
        to the key
        '''
        index = self._hash(key)
        decrement = 1
        while self._pairs[index] != None and \
                self._pairs[index][0] != key:
            index = (index - decrement) % self._size
            decrement += 1
        self._pairs[index] = [key, value]

    def add(self, key, value):
        '''

        If a key is already present in the table,
        its value is altered to add a new value.

        :param key: the key already present in
        the table
        :param value: a new value associated with
        the key
        '''
        index = self._hash(key)
        decrement = 1
        while self._pairs[index] != None and \
                self._pairs[index][0] != key:
            index = (index - decrement) % self._size
            decrement += 1
        self._pairs[index][1].append(value)

    def get(self, key):
        '''

        Iterates through the table and returns the
        value associated with the inputted key.

        :param key: the inputted key whose value is
        wanted
        :return: the value of the inputted key
        '''
        index = self._hash(key)
        decrement = 1
        while self._pairs[index] != None and \
                self._pairs[index][0] != key:
            index = (index - decrement) % self._size
            decrement += 1
        if self._pairs[index] == None:
            return None
        else:
            return self._pairs[index][1]

    def __contains__(self, key):
        '''

        If the key is present in the table, the
        method returns true, else false.

        :param key: inputted key to find
        :return: True or False
        '''
        index = self._hash(key)
        decrement = 1
        while self._pairs[index] != None and \
                self._pairs[index][0] != key:
            index = (index - decrement) % self._size
            decrement += 1
        if self._pairs[index] != None and self._pairs[index][0] \
                == key:
            return True
        return False

    def __str__(self):
        return self._pairs

SEED = 8
random.seed(SEED)

def main():
    sfile = input()
    m = input()
    n = input()
    if int(n) < 1:
        print("ERROR: specified prefix size is less than one")
        sys.exit(0)
    num_words = input()
    if int(num_words) < 1:
        print("ERROR: specified size of the generated text "
              "is less than one")
        sys.exit(0)
    words = read_in(sfile)
    hash_table = table(words, int(m), int(n))
    to_be = generation(words, hash_table, int(num_words),
                       int(n))
    printer(to_be)


def read_in(file):
    '''

    Reads in the inputted file and appends each word into
    a mass list

    :param file: inputted file from user
    :return: list containing all words from file
    '''
    opening = open(file, 'r')
    empty = []
    for i in opening.readlines():
        new = i.strip('\n')
        temporary = new.split()
        for j in temporary:
            empty.append(j)
    opening.close()
    return empty


def table(words, table, pre_size):
    '''

    Uses the Hashtable class to insert keys and values
    into a table of a certain size.

    :param words: list of all words in the inputted file
    :param table: desired size of the hashtable
    :param pre_size: the amount of words per prefix
    :return: a filled in hashtable object
    '''
    hash_browns = Hashtable(table)
    nonword = '@'
    for z in range(pre_size):
        zero = words[z]
        if hash_browns.__contains__(nonword) \
                == False:
            new = [zero]
            hash_browns.put(nonword, new)
        else:
            hash_browns.add(nonword, zero)
    for i in range(0, len(words)):
        temporary = words[i:i + pre_size]
        new_str = ''
        for j in temporary:
            new_str += j + ' '
        if hash_browns.__contains__(new_str) \
                == False:
            if (i + pre_size + 1) <= len(words):
                empty = []
                empty.append(words[i + pre_size])
                hash_browns.put(new_str, empty)
        else:
            if (i + pre_size + 1) <= len(words):
                hash_browns.add(new_str,
                                words[i + pre_size])
    return hash_browns


def generation(original, hasher, length, size):
    '''

    Based off the first n words and the
    hashtable created, words are auto-generated.

    :param hasher: the hashtable object
    :param length: the desired number of words
    to be generated
    :param size: the first n amount of words
    to start
    :return: a list of the auto-generated words
    in order
    '''
    new_empty = []
    for i in range(size):
        new_empty.append(original[i])
    for j in range(length - size):
        key = ''
        for i in new_empty[j:j + size]:
            key += i + ' '
        find = hasher.get(key)
        if len(find) > 1:
            randomized = int(random.randint
                             (0, len(find) - 1))
            actual = find[randomized]
            new_empty.append(actual)
        else:
            new_empty.append(find[0])
    return new_empty


def printer(generated):
    '''

    Prints the auto-generated list.

    :param generated: a list of the auto-generated
    words in order
    '''
    for i in range(0, len(generated), 10):
        print(" ".join(generated[i:i + 10]))

main()