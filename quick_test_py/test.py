from typing import List, Any
import json
import os
from loguru import logger

class Tester():
    def __init__(self, path: str):
        self.path = path
        self.tests = {}
        if not os.path.exists(path):
            os.makedirs(path)

    def register(self, name: str, test_cases: List[callable]) -> None:
        self.tests[name] = test_cases

    def log(self, name: str) -> None:
        logger.info(f"Running {name}\n")
        for i, testcase in enumerate(self.tests[name]):
            logger.info(f"---------Result of testcase #{i}---------")
            logger.info(f"\t{testcase()}")

    def validate(self, name: str) -> None:
        self._validate(name, [tc() for tc in self.tests[name]])

    def record(self, name: str) -> None:
        logger.info(f"---------Recording results of {name}---------")
        self._record(name, [tc() for tc in self.tests[name]])

    def _validate(self, name: str, out: List[Any]) -> None:
        logger.info(f"---------Validating {name}---------")
        with open(os.path.join(self.path, name), 'r') as fin:
            data = json.load(fin)
        passed = True
        for i, (out, ground_truth) in enumerate(zip(out, data)):
            if out != ground_truth:
                logger.error(f"\tTestcase #{i} failed")
                passed = False
        if passed is False:
            logger.warn(f"Some testcases failed for {name}")
        else:
            logger.success(f"All testcases passed for {name}! Have a nice day.")

    def _record(self, name: str, out: List[Any]) -> None:
        with open(os.path.join(self.path, f'{name}.json'), 'w') as fout:
            json.dump(out, fout, indent=4)