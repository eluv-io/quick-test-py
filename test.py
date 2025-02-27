"""
Test file to test the tester
"""
from quick_test_py import Tester

class CustomClass():
    def __init__(self):
        self.a = 1
        self.b = 2
    def __eq__(self, value: object) -> bool:
        return self.a == value.a and self.b == value.b

def main():
    # Passing tests
    tester = Tester("tests")
    tests = ["test1", "test2"]
    def test1():
        return [lambda: 1+1, lambda: 2+3, lambda: 5+8]
    def test2():
        return [lambda: {"hello":"world"}, lambda: "hello", lambda: {"hello": [1, 2, 3]}]
    tester.register(test1)
    tester.register(test2)

    for test in tests:
        tester.log([test])
        tester.record([test])
    
    for test in tests:
        tester.validate([test])

    # Test without specifying test name
    tester = Tester("tests")
    tester.register(test1)
    tester.register(test2)
    tester.log()
    tester.record()
    tester.validate()

    # Failing tests
    tester = Tester("tests")
    def test1():
        return [lambda: 1+1, lambda: 2+4, lambda: 5+8]
    tester.register(test1)
    tester.register(test2)
    tester.validate()

    # Error in test case
    tester = Tester("tests")
    def test1():
        return [lambda: 1+1, lambda: 1/0, lambda: 5+8]
    def test2():
        return [lambda: {"hello":"world"}, lambda: "hello", lambda: {"hello": 1/0}]
    tester.register(test1)
    tester.register(test2)
    tester.log()
    tester.validate()

    tester = Tester("tests")
    def pickle_test():
        return [lambda: 1+1, lambda: CustomClass()]
    tester.register(pickle_test) # non json-able result in test case #2
    tester.record()
    tester.validate()

    # Failing test with dictionary result
    tester = Tester("tests")
    def test1():
        return [lambda: 1+1, lambda: 2+3, lambda: {"a": 1, "b": 2, "c": {"d": [1, 2, 3]}}]
    tester.register(test1)
    tester.record()
    tester = Tester("tests")
    def test1():
        return [lambda: 1+1, lambda: 2+3, lambda: {"a": 1, "b": 2, "c": {"d": [1, 2, 3, 4]}}]
    tester.register(test1)
    tester.validate()

if __name__ == "__main__":
    main()