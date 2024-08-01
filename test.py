"""
Test file to test the tester
"""
from quick_test_py import Tester

def main():
    tester = Tester("tests")
    tests = ["test1", "test2"]
    tester.register("test1", [lambda: 1+1, lambda: 2+3, lambda: 5+8])
    tester.register("test2", [lambda: {"hello":"world"}, lambda: "hello", lambda: {"hello": [1, 2, 3]}])
    for test in tests:
        tester.log(test)
        tester.record(test)
        
    for test in tests:
        tester.validate(test)

if __name__ == "__main__":
    main()