import pytest
import unittest


# def add(a, b):
#     return a+b
# 
# 
# def test_add():
#     assert add(2+3) == 6
# 
# 
# def f():
#     raise SystemExit(1)
# 
# 
# def test_mytest():
#     with pytest.raises(SystemExit):
#         f()


class TestClass:
    def test_one(self):
        x = 'this'
        assert 'h' in x

    def test_two(self):
        x = 'hello'
        assert hasattr(x, 'check')


