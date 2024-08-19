from typing import List, Any, Optional
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

    def log(self, name: Optional[str]=None) -> None:
        if name is not None:
            tests = [name]
        else:
            tests = self.tests.keys()
        for name in tests:
            logger.info(f"Running {name}\n")
            for i, testcase in enumerate(self.tests[name]):
                try:
                    logger.info(f"---------Result of testcase #{i+1}---------")
                    logger.info(f"\t{testcase()}")
                except Exception as e:
                    logger.error(f"Encountered error while running testcase #{i+1}")
                    raise e

    def validate(self, name: Optional[str]=None) -> None:
        if name is not None:
            tests = [name]
        else:
            tests = self.tests.keys()
        for name in tests:
            try:
                self._validate(name, [tc() for tc in self.tests[name]])
            except Exception as e:
                logger.error(f"Encountered error while validating {name}")
                raise e

    def record(self, name: Optional[str]=None) -> None:
        if name is not None:
            tests = [name]
        else:
            tests = self.tests.keys()
        for name in tests:
            logger.info(f"---------Recording results of {name}---------")
            try:
                self._record(name, [tc() for tc in self.tests[name]])
            except Exception as e:
                logger.error(f"Encountered error while retrieving output from {name}.")
                raise e

    def _validate(self, name: str, out: List[Any]) -> None:
        logger.info(f"---------Validating {name}---------")
        with open(os.path.join(self.path, f'{name}.json'), 'r') as fin:
            data = json.load(fin)
        passed = True
        for i, (out, ground_truth) in enumerate(zip(out, data)):
            if out != ground_truth:
                logger.error(f"\tTestcase #{i+1} failed")
                passed = False
        if passed is False:
            logger.warning(f"Some testcases failed for {name}")
        else:
            logger.success(f"All testcases passed for {name}!")

    def _record(self, name: str, out: List[Any]) -> None:
        with open(os.path.join(self.path, f'{name}.json'), 'w') as fout:
            json.dump(out, fout, indent=4)