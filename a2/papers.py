"""Assignment 2: Modelling CS Education research paper data

=== CSC148 Winter 2019 ===
This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

All of the files in this directory and all subdirectories are:
Copyright (c) 2019 Bogdan Simion, David Liu, Diane Horton, Jacqueline Smith

=== Module Description ===
This module contains a new class, PaperTree, which is used to model data on
publications in a particular area of Computer Science Education research.
This data is adapted from a dataset presented at SIGCSE 2019.
You can find the full dataset here: https://www.brettbecker.com/sigcse2019/

Although this data is very different from filesystem data, it is still
hierarchical. This means we are able to model it using a TMTree subclass,
and we can then run it through our treemap visualisation tool to get a nice
interactive graphical representation of this data.

# WE COMPLETED THE STEPS BELOW
Recommended steps:
1. Start by reviewing the provided dataset in cs1_papers.csv. You can assume
   that any data used to generate this tree has this format,
   i.e., a csv file with the same columns (same column names, same order).
   The categories are all in one column, separated by colons (':').
   However, you should not make assumptions about what the categories are, how
   many categories there are, the maximum number of categories a paper can have,
   or the number of lines in the file.

2. Read through all the docstrings in this file once. There is a lot to take in,
   so don't feel like you need to understand it all the first time.
   Draw some pictures!
   We have provided the headers of the initializer as well as of some helper
   functions we suggest you implement. Note that we will not test any
   private top-level functions, so you can choose not to implement these
   functions, and you can add others if you want to for your solution.
   For this task, we will be testing that you are building the correct tree,
   not that you are doing it in a particular way. We will access your class
   in the same way as in the client code in the visualizer.

3. Plan out what you'll need to do to implement the PaperTree initializer.
   In particular, think about how to use the boolean parameters to do different
   things in setting up the tree. You may also find it helpful to review the
   Python documentation about the csv module, which you are permitted and
   encouraged to use. You should have a good plan, including what your subtasks
   are, before you begin writing any code.

4. Write the code for the PaperTree initializer and any helper functions you
   want to use in your design. You should not make any changes to the public
   interface of this module, or of the PaperTree class, but you can add private
   attributes and helpers as needed.

5. Tidy and test your code, and try it with the visualizer client code. Make
   sure you have documented any new private attributes, and that PyTA passes
   on your code.
"""
import csv
from typing import List, Dict, Union
from tm_trees import TMTree

# Filename for the dataset
DATA_FILE = 'cs1_papers.csv'


class PaperTree(TMTree):
    """A tree representation of Computer Science Education research paper data.

    === Private Attributes ===
    # WE IMPLEMENTED IT
    These should store information about this paper's <authors> and <doi>.

    _authors: a str for the authors of the paper

    _doi: A Digital Object Identifier for the paper/ the url of the paper

    _citations: the number of citations of a paper
        * citations is for acknowledging the paper *

    _by_year: puts year in the base of the name if _by_year is True and if False
        then doesn't care

    === Inherited Attributes ===
    rect:
        The pygame rectangle representing this node in the treemap
        visualization.
    data_size:
        The size of the data represented by this tree.
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
    - All TMTree RIs are inherited.
    """

    # WE IMPLEMENTED IT

    _authors: str
    _doi: str
    _citations: int
    _by_year: bool
    _all_papers: bool

    def __init__(self, name: str, subtrees: List[TMTree], authors: str = '',
                 doi: str = '', citations: int = 0, by_year: bool = True,
                 all_papers: bool = False) -> None:
        """Initialize a new PaperTree with the given <name> and <subtrees>,
        <authors> and <doi>, and with <citations> as the size of the data.

        If <all_papers> is True, then this tree is to be the root of the paper
        tree. In that case, load data about papers from DATA_FILE to build the
        tree.

        If <all_papers> is False, Do NOT load new data.

        <by_year> indicates whether or not the first level of subtrees should be
        the years, followed by each category, subcategory, and so on. If
        <by_year> is False, then the year in the dataset is simply ignored.
        """
        # WE IMPLEMENTED IT
        self._authors = authors
        self._doi = doi
        self._citations = citations
        self._by_year = by_year
        self._all_papers = all_papers
        if all_papers:
            diction = _load_papers_to_dict(self._by_year)
            generated_subtrees = _build_tree_from_dict(diction)
            TMTree.__init__(self, name, generated_subtrees, citations)
        else:
            TMTree.__init__(self, name, subtrees, citations)

    def get_separator(self) -> str:
        """Return the string used to separate names in the string
        representation of a path from the tree root to this tree.
        """
        return ':'

    def get_suffix(self) -> str:
        """Return the string used at the end of the string representation of
        a path from the tree root to this tree.
        """
        if len(self._subtrees) == 0:
            return ' (Research Paper)'
        else:
            return ' (Category)'


def _load_papers_to_dict(by_year: bool = True) -> Dict:
    """Return a nested dictionary of the data read from the papers dataset file.

    If <by_year>, then use years as the roots of the subtrees of the root of
    the whole tree. Otherwise, ignore years and use categories only.
    """
    # WE IMPLEMENTED IT
    dic = {}
    lst = []
    if not by_year:
        with open(DATA_FILE, 'r') as csvfile:
            my_file = csv.reader(csvfile)
            for rows in my_file:
                lst.append(rows)
            lst = lst[1:]
            for l in lst:
                categories = l[3].split(':')
                for i in range(len(categories)):
                    categories[i] = categories[i].strip()
                tup = (l[0], l[1], l[2], l[3], l[4], l[5])
                _recursive_dict_update(dic, categories, tup)
        return dic

    else:
        with open(DATA_FILE, 'r') as csvfile:
            dic1 = {}
            my_file = csv.reader(csvfile)
            for rows in my_file:
                lst.append(rows)
            lst = lst[1:]
            for line in lst:
                year = line[2]
                if year in dic1:
                    dic1[year].append(line)
                else:
                    dic1[year] = [line]
            for ls in dic1:
                dic2 = {}
                for l in dic1[ls]:
                    categories = l[3].split(':')
                    for i in range(len(categories)):
                        categories[i] = categories[i].strip()
                    tup = (l[0], l[1], l[2], l[3], l[4], l[5])
                    _recursive_dict_update(dic2, categories, tup)
                dic1[ls] = dic2
        return dic1


def _recursive_dict_update(dic: dict, lst: list, tup: tuple) -> None:
    """ Actual recursive dictionary.
    """
    if len(lst) == 0:
        dic[tup[4]] = tup
    else:
        if lst[0] in dic:
            _recursive_dict_update(dic[lst[0]], lst[1:], tup)
        else:
            new_dict = _recursive_dictionary(lst[1:], tup)
            dic[lst[0]] = new_dict


def _recursive_dictionary(lst: list, tup: tuple) -> Union[dict, tuple]:
    """ The actual nested dictionary."""
    if len(lst) == 0:
        return {tup[4]: tup}
    else:
        dic = {lst[0]: {}}
        val = _recursive_dictionary(lst[1:], tup)
        if isinstance(val, tuple):
            dic[lst[0]][tup[4]] = val
        else:
            dic[lst[0]].update(val)
        return dic


def _build_tree_from_dict(nested_dict: Dict) -> Union[List[PaperTree], tuple]:
    """Return a list of trees from the nested dictionary <nested_dict>.
    """
    # WE IMPLEMENTED IT
    if isinstance(nested_dict, tuple):
        d = nested_dict
        return [PaperTree(d[1], [], d[0], d[4], int(d[5]))]
    else:
        lst = []
        for val in nested_dict:
            subtrees = []
            if isinstance(nested_dict[val], tuple):
                d = nested_dict[val]
                p = PaperTree(d[1], [], d[0], d[4], int(d[5]))
                lst.append(p)
            else:
                subtrees.extend(_build_tree_from_dict(nested_dict[val]))
                lst.append(PaperTree(val, subtrees))
        return lst


if __name__ == "__main__":
    import python_ta
    python_ta.check_all(config={
        'allowed-import-modules': ['python_ta', 'typing', 'csv', 'tm_trees'],
        'allowed-io': ['_load_papers_to_dict'],
        'max-args': 8
    })
