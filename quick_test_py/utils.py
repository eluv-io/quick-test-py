import numpy as np

def are_equal(value1, value2):
    try:
        if isinstance(value1, np.ndarray) or isinstance(value2, np.ndarray):
            return np.array_equal(value1, value2)
        else:
            return value1 == value2
    except Exception as e:
        raise ValueError(f"The output and ground truth are not able to be compared directly via the == operator. \
                         It may be worth converting the output of the test case function to a type such that \
                         the == operator returns a bool.") from e