import pytest
from RedBlackTree import RedBlackTree

def test_insert():
    rbt = RedBlackTree()
    rbt.insert(2)
    rbt.insert(0)
    rbt.insert(1)
    assert [node[0] for node in rbt.inorder()] == [0,1,2]
    assert rbt.find_count(0) == 1
    assert rbt.find_count(1) == 1
    assert rbt.find_count(2) == 1

def test_search_repeat():
    rbt = RedBlackTree()
    rbt.insert(2)
    rbt.insert(0)
    rbt.insert(1)
    rbt.insert(1)
    rbt.insert(1)
    assert rbt.find_count(0) == 1
    assert rbt.find_count(-1) == 0
    assert rbt.find_count(1) == 3

def test_inorder():
    rbt = RedBlackTree()
    rbt.insert(2)
    rbt.insert(0)
    rbt.insert(1)
    rbt.insert(1)
    rbt.insert(1)
    assert rbt.inorder() == [(0,1),(1,3),(2,1)]
