import numpy as np

def are_equal(value1, value2):
    if isinstance(value1, np.ndarray) or isinstance(value2, np.ndarray):
        return np.array_equal(value1, value2)
    else:
        return value1 == value2