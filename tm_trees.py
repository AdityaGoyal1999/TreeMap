"""Assignment 2: Trees for Treemap

=== CSC148 Winter 2019 ===
This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

All of the files in this directory and all subdirectories are:
Copyright (c) 2019 Bogdan Simion, David Liu, Diane Horton, Jacqueline Smith

=== Module Description ===
This module contains the basic tree interface required by the treemap
visualiser. You will both add to the abstract class, and complete a
concrete implementation of a subclass to represent files and folders on your
computer's file system.
"""
from __future__ import annotations
import os
import math
from random import randint
from typing import List, Tuple, Optional
# remove this later on
# from print_dirs import print_items


class TMTree:
    """A TreeMappableTree: a tree that is compatible with the treemap
    visualiser.

    This is an abstract class that should not be instantiated directly.

    You may NOT add any attributes, public or private, to this class.
    However, part of this assignment will involve you implementing new public
    *methods* for this interface.
    You should not add any new public methods other than those required by
    the client code.
    You can, however, freely add private methods as needed.

    === Public Attributes ===
    rect:
        The pygame rectangle representing this node in the treemap
        visualization.
    data_size:
        The size of the data represented by this tree.

    === Private Attributes ===
    _colour:
        The RGB colour value of the root of this tree.
    _name:
        The root value of this tree, or None if this tree is empty.
    _subtrees:
        The subtrees of this tree.
    _parent_tree:
        The parent tree of this tree; i.e., the tree that contains this tree
        as a subtree, or None if this tree is not part of a larger tree.
    _expanded:
        Whether or not this tree is considered expanded for visualization.

    === Representation Invariants ===
    - data_size >= 0
    - If _subtrees is not empty, then data_size is equal to the sum of the
      data_size of each subtree.

    - _colour's elements are each in the range 0-255.

    - If _name is None, then _subtrees is empty, _parent_tree is None, and
      data_size is 0.
      This setting of attributes represents an empty tree.

    - if _parent_tree is not None, then self is in _parent_tree._subtrees

    - if _expanded is True, then _parent_tree._expanded is True
    - if _expanded is False, then _expanded is False for every tree
      in _subtrees
    - if _subtrees is empty, then _expanded is False
    """

    rect: Tuple[int, int, int, int]
    data_size: int
    _colour: Tuple[int, int, int]
    _name: str
    _subtrees: List[TMTree]
    _parent_tree: Optional[TMTree]
    _expanded: bool

    def __init__(self, name: str, subtrees: List[TMTree],
                 data_size: int = 0) -> None:
        """Initialize a new TMTree with a random colour and the provided <name>.

        If <subtrees> is empty, use <data_size> to initialize this tree's
        data_size.

        If <subtrees> is not empty, ignore the parameter <data_size>,
        and calculate this tree's data_size instead.

        Set this tree as the parent for each of its subtrees.

        Precondition: if <name> is None, then <subtrees> is empty.
        """
        self.rect = (0, 0, 0, 0)
        self._name = name
        self._subtrees = subtrees[:]
        self._parent_tree = None

        # You will change this in Task 5
        if len(self._subtrees) > 0:
            self._expanded = True
        else:
            self._expanded = False
        # self._expanded = False

        # TODO: (Task 1) Complete this initializer by doing two things:
        # 1. Initialize self._colour and self.data_size, according to the
        # docstring.
        # 2. Set this tree as the parent for each of its subtrees.

        #
        # if self.is_empty()
        #

        self._colour = (randint(0, 255), randint(0, 255), randint(0, 255))
        if len(subtrees) == 0:
            self.data_size = data_size
        else:
            self.data_size = self._calculate_data_size()

    def _calculate_data_size(self) -> int:
        """ Helper method to calculate the data size recursively.
        """
        if self.is_empty():
            return 0
        # there is some difference in elif condition
        elif len(self._subtrees) == 0:
            return self.data_size
        else:
            # data size abbreviated as ds
            ds = 0
            for subtree in self._subtrees:
                ds += subtree._calculate_data_size()
            return ds

    def is_empty(self) -> bool:
        """Return True iff this tree is empty.
        """
        return self._name is None

    def update_rectangles(self, rect: Tuple[int, int, int, int]) -> None:
        """Update the rectangles in this tree and its descendents using the
        treemap algorithm to fill the area defined by pygame rectangle <rect>.
        """
        # TODO: (Task 2) Complete the body of this method.
        # Read the handout carefully to help get started identifying base cases,
        # then write the outline of a recursive step.
        #
        # Programming tip: use "tuple unpacking assignment" to easily extract
        # elements of a rectangle, as follows.
        # x, y, width, height = rect
        #
        # Does this base case actully hold?
        if self.data_size == 0:
            pass
        # I am missing some case
        # What are we supposed to do for an empty folder?
        elif self._parent_tree is not None and len(self._parent_tree._subtrees)\
                == 1:
            self.rect = rect
        else:
            x, y, width, height = rect
            w1 = x
            h1 = y
            self.rect = rect
            if width > height:
                count = 0
                for subtree in self._subtrees:
                    # last element with the rounded up
                    if count == len(self._subtrees) - 1:
                        subtree.update_rectangles((w1, y, width, height))
                        count += 1
                    else:
                        percentage = subtree.data_size / self.data_size
                        percentage = percentage * width
                        percentage = math.floor(percentage)
                        subtree.update_rectangles((w1, y, w1 + percentage, height))
                        w1 = x + percentage
            else:
                count = 0
                for subtree in self._subtrees:
                    if count == len(self._subtrees) - 1:
                        subtree.update_rectangles((x, h1, width, height))
                        count += 1
                    else:
                        percentage = subtree.data_size / self.data_size
                        percentage = percentage * height
                        percentage = math.floor(percentage)
                        h1 = h1 + percentage
                        y = h1
                        subtree.update_rectangles((x, y, width, h1))
            #####
            # x, y, width, height = rect
            # self.rect = (x, y, width, height)
            # if width > height:
            #     # this is opposed to the index looping - this helps to check if
            #     # the subtree is the last element in the subtree
            #     count = 0
            #     # w1 is to keep the progress of the x value
            #     w1 = x
            #     for subtree in self._subtrees:
            #         # the last element of the subtree
            #         if count == len(self._subtrees) - 1:
            #             # subtree.rect = (w1, y, width, height)
            #             subtree.update_rectangles((w1, y, width, height))
            #             count += 1
            #         else:
            #             percentage = subtree.data_size / self.data_size
            #             #
            #             x = w1
            #             w1 = percentage * width
            #             w1 = math.floor(w1)
            #             # subtree.rect = (x, y, w1, height)
            #             subtree.update_rectangles((x, y, x + w1, height))
            #             count += 1
            # else:   # width <= height
            #     count = 0
            #     h1 = y
            #     for subtree in self._subtrees:
            #         if count == len(self._subtrees) - 1:
            #             # subtree.rect = (x, h1, width, height)
            #             subtree.update_rectangles((x, h1, width, height))
            #             count += 1
            #         else:
            #             percentage = subtree.data_size / self.data_size
            #             y = h1
            #             h1 = percentage * height
            #             h1 = math.floor(h1)
            #             # subtree.rect = (x, y, width, h1)
            #             subtree.update_rectangles((x, y, width, y + h1))
            #             count += 1

    def get_rectangles(self) -> List[Tuple[Tuple[int, int, int, int],
                                           Tuple[int, int, int]]]:
        """Return a list with tuples for every leaf in the displayed-tree
        rooted at this tree. Each tuple consists of a tuple that defines the
        appropriate pygame rectangle to display for a leaf, and the colour
        to fill it with.
        """
        # TODO: (Task 2) Complete the body of this method.
        #
        # What are we supposed to do when there is no tuple
        # What about the other triangle
        #
        #
        if self.is_empty():
            return []
        elif len(self._subtrees) == 0 or self._expanded is False:
            return [(self.rect, self._colour)]
        else:
            output = []
            for subtree in self._subtrees:
                output.extend(subtree.get_rectangles())
            return output

    def get_tree_at_position(self, pos: Tuple[int, int]) -> Optional[TMTree]:
        """Return the leaf in the displayed-tree rooted at this tree whose
        rectangle contains position <pos>, or None if <pos> is outside of this
        tree's rectangle.

        If <pos> is on the shared edge between two rectangles, return the
        tree represented by the rectangle that is closer to the origin.
        """
        # TODO: (Task 3) Complete the body of this method
        a, b = pos
        x, y, width, height = self.rect
        if x <= a <= width and y <= b <= height:
            return self._get_tmtree_in_range(pos)
        else:
            return None

    def _get_tmtree_in_range(self, pos: Tuple[int, int]) -> Optional[TMTree]:
        """ Recursively returns the leaf which is in the range.
        """
        if self.is_empty():
            return None
        elif len(self._subtrees) == 0 or self._expanded is False:
            x, y, width, height = self.rect
            if x <= pos[0] <= width and y <= pos[1] <= height:
                return self
            else:
                return None
        else:
            for subtree in self._subtrees:
                val = subtree._get_tmtree_in_range(pos)
                if val is not None:
                    return val
            return None

    def update_data_sizes(self) -> int:
        """Update the data_size for this tree and its subtrees, based on the
        size of their leaves, and return the new size.

        If this tree is a leaf, return its size unchanged.
        """
        # TODO: (Task 4) Complete the body of this method.
        if self.is_empty():
            return 0
        elif len(self._subtrees) == 0:
            return self.data_size
        else:
            size = 0
            for subtree in self._subtrees:
                val = subtree.update_data_sizes()
                size += val
                subtree.data_size += val
            self.data_size = size
            return size

    def move(self, destination: TMTree) -> None:
        """If this tree is a leaf, and <destination> is not a leaf, move this
        tree to be the last subtree of <destination>. Otherwise, do nothing.
        """
        # TODO: (Task 4) Complete the body of this method.
        if len(self._subtrees) == 0 and len(destination._subtrees) > 0:
            remove_subtree = self
            destination._subtrees.append(remove_subtree)
            self._parent_tree.remove(remove_subtree)
        else:
            pass

    def change_size(self, factor: float) -> None:
        """Change the value of this tree's data_size attribute by <factor>.

        Always round up the amount to change, so that it's an int, and
        some change is made.

        Do nothing if this tree is not a leaf.
        """
        # TODO: (Task 4) Complete the body of this method
        val = factor * self.data_size
        val = round(val)
        val2 = self.data_size
        if val + val2 < 1:
            pass
        else:
            self.data_size += val
            self._update_parent()

    def expand_all(self) -> None:
        """ Expands all the corresponding tree and subtrees when the user wants.
        """
        if self.is_empty():
            pass
        elif len(self._subtrees) == 0:
            pass
        else:
            self._expanded = True
            for subtree in self._subtrees:
                subtree.expand_all()

    def expand(self) -> None:
        """ Expands the corresponding subtree as the user wants.
        """
        if self.is_empty():
            pass
        elif len(self._subtrees) == 0:
            pass
        else:
            self._expanded = True

    # collapse and collapse_all doesn't work properly
    def collapse(self) -> None:
        """ Collapses the corresponding tree.
        """
        if self.is_empty():
            pass
        elif len(self._subtrees) == 0:
            pass
        else:
            self._expanded = False
            for subtree in self._subtrees:
                subtree._expanded = False

    def collapse_all(self) -> None:
        """ Collapses the tree selected by the user.
        """
        # could be problematic
        if self.is_empty():
            pass
        else:
            self._collapse_all_helper2()

    def _collapse_all_helper2(self) -> Optional[TMTree]:
        """ Collapses the whole corresponding tree.
        """
        if self.is_empty():
            return None
        elif self._parent_tree is None:
            return self
        else:
            return self._parent_tree._collapse_all_helper2()

    def _collapse_all_helper1(self, depth: int = 0):
        """ Collapses all the rectangles.
        """
        if self.is_empty():
            pass
        else:
            if depth == 0:
                tree = self._collapse_all_helper2()
            else:
                tree = self
            tree._expanded = False
            for subtree in tree._subtrees:
                subtree._collapse_all_helper1(depth+1)


    # TODO: (Task 5) Write the methods expand, expand_all, collapse, and
    # TODO: collapse_all, and add the displayed-tree functionality to the
    # TODO: methods from Tasks 2 and 3

    def _update_parent(self) -> None:
        """ Updates the values of the parent trees through recursion.
        """
        # this condition could be problematic
        if self._parent_tree is None:
            pass
        else:
            self._parent_tree.update_data_sizes()
            self._parent_tree._parent_tree._update_parent()

    # Methods for the string representation
    def get_path_string(self, final_node: bool = True) -> str:
        """Return a string representing the path containing this tree
        and its ancestors, using the separator for this tree between each
        tree's name. If <final_node>, then add the suffix for the tree.
        """
        if self._parent_tree is None:
            path_str = self._name
            if final_node:
                path_str += self.get_suffix()
            return path_str
        else:
            path_str = (self._parent_tree.get_path_string(False) +
                        self.get_separator() + self._name)
            if final_node or len(self._subtrees) == 0:
                path_str += self.get_suffix()
            return path_str

    def get_separator(self) -> str:
        """Return the string used to separate names in the string
        representation of a path from the tree root to this tree.
        """
        raise NotImplementedError

    def get_suffix(self) -> str:
        """Return the string used at the end of the string representation of
        a path from the tree root to this tree.
        """
        raise NotImplementedError


class FileSystemTree(TMTree):
    """A tree representation of files and folders in a file system.

    The internal nodes represent folders, and the leaves represent regular
    files (e.g., PDF documents, movie files, Python source code files, etc.).

    The _name attribute stores the *name* of the folder or file, not its full
    path. E.g., store 'assignments', not '/Users/Diane/csc148/assignments'

    The data_size attribute for regular files is simply the size of the file,
    as reported by os.path.getsize.
    """

    def __init__(self, path: str) -> None:
        """Store the file tree structure contained in the given file or folder.

        Precondition: <path> is a valid path for this computer.

        >>> f = FileSystemTree('/Users/adityagoyal/Documents/csc148/assignments/a2/example-directory')
        >>> f._how_many_trees()
        12
        """
        # Remember that you should recursively go through the file system
        # and create new FileSystemTree objects for each file and folder
        # encountered.
        #
        # Also remember to make good use of the superclass constructor!
        # TODO: (Task 1) Implement the initializer
        n = os.path.basename(path)
        ds = os.path.getsize(path)
        if not os.path.isdir(path):
            subdirectories = []
        else:
            subdirectories = []
            for subdirectory in os.listdir(path):
                # if subdirectory != '.DS_Store':
                #
                # Delete this statement
                #
                if subdirectory == '.DS_Store':
                    continue
                a = FileSystemTree(os.path.join(path, subdirectory))
                subdirectories.append(a)
        TMTree.__init__(self, n, subdirectories, ds)

    def _how_many_trees(self) -> int:
        if self.is_empty():
            return 0
        else:
            count = 1
            for subtree in self._subtrees:
                count += subtree._how_many_trees()
            return count

    def _get_rectangles(self, depth: int = 0) -> None:
        """ Prints out the rectangles of the subsequent tree.

        Precondition: Execute update_rectangles beforehand.

        >>> f = FileSystemTree('/Users/adityagoyal/Documents/csc148/assignments/a2/example-directory')
        >>> f.update_rectangles((0, 0, 200, 100))
        >>> f._get_rectangles()
        """
        if self.is_empty():
            pass
        else:
            print(depth * '   ', self.rect)
            for subtree in self._subtrees:
                subtree._get_rectangles(depth+1)


    def get_separator(self) -> str:
        """Return the file separator for this OS.
        """
        return os.sep

    def get_suffix(self) -> str:
        """Return the final descriptor of this tree.
        """
        if len(self._subtrees) == 0:
            return ' (file)'
        else:
            return ' (folder)'


if __name__ == '__main__':

    # import python_ta
    # python_ta.check_all(config={
    #     'allowed-import-modules': [
    #         'python_ta', 'typing', 'math', 'random', 'os', '__future__'
    #     ]
    # })

    import doctest
    doctest.testmod()

    f = FileSystemTree('/Users/adityagoyal/Documents/csc148/assignments/a2/example-directory')
    f.update_rectangles((0, 0, 200, 100))
    print(f.get_rectangles())
    # print_items('/Users/adityagoyal/Documents/csc148/assignments', '')
    # f._how_many_trees()
    # print(f.get_path_string())
    print(f.get_tree_at_position((90, 100))._name)
