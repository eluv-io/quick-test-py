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
    tester.register("test1", [lambda: 1+1, lambda: 2+3, lambda: 5+8])
    tester.register("test2", [lambda: {"hello":"world"}, lambda: "hello", lambda: {"hello": [1, 2, 3]}])
    for test in tests:
        tester.log(test)
        tester.record(test)
        
    for test in tests:
        tester.validate(test)

    # Test without specifying test name
    tester = Tester("tests")
    tester.register("test1", [lambda: 1+1, lambda: 2+3, lambda: 5+8])
    tester.register("test2", [lambda: {"hello":"world"}, lambda: "hello", lambda: {"hello": [1, 2, 3]}])
    tester.log()
    tester.record()
    tester.validate()

    # Failing tests
    tester = Tester("tests")
    tester.register("test1", [lambda: 1+1, lambda: 2+4, lambda: 5+8]) # changed test case #2
    tester.register("test2", [lambda: {"hello":"world"}, lambda: "hello", lambda: {"hello": [1, 2, 3]}])
    tester.validate()

    # Error in test case
    tester = Tester("tests")
    tester.register("test1", [lambda: 1+1, lambda: 1/0, lambda: 5+8]) # error in test case #2
    tester.register("test2", [lambda: {"hello":"world"}, lambda: "hello", lambda: {"hello": 1/0}]) # error in test case #3
    tester.log()
    tester.validate()

    tester = Tester("tests")
    tester.register("pickle_test", [lambda: 1+1, lambda: CustomClass()]) # non json-able result in test case #2
    tester.record()
    tester.validate()

    # Failing test with dictionary result
    tester = Tester("tests")
    tester.register("test1", [lambda: 1+1, lambda: 2+3, lambda: {"a": 1, "b": 2, "c": {"d": [1, 2, 3]}}])
    tester.record()
    tester = Tester("tests")
    tester.register("test1", [lambda: 1, lambda: 2+3, lambda: {"a": 1, "b": 2, "c": {"d": [1, 2, 3, 4]}}])
    tester.validate()

if __name__ == "__main__":
    main()