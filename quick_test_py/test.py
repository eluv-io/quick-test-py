from typing import List, Any, Optional, Callable
import os
import pickle as pkl
import json
from loguru import logger

from .utils import are_equal

class Tester():
    def __init__(self, path: str):
        self.path = path
        self.tests = {}
        if not os.path.exists(path):
            os.makedirs(path)

    def register(self, name: str, test_cases: List[Callable]) -> None:
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
                    logger.error(f"Encountered error while running testcase #{i+1}:\n {e}")
                    continue

    def validate(self, name: Optional[str]=None) -> None:
        if name is not None:
            tests = [name]
        else:
            tests = self.tests.keys()
        failed = []
        successful = []
        for name in tests:
            passed = self._validate(name, [tc for tc in self.tests[name]])
            if passed:
                successful.append(name)
            else:
                failed.append(name)
        if len(failed) == 0:
            logger.success("All tests passed!")
        else:
            if len(successful) > 0:
                logger.info(f"Tests passed: {successful}")
            logger.error(f"Tests failed: {failed}")
            
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
                logger.error(f"Encountered error while retrieving output from {name}")
                raise e

    def _validate(self, name: str, cases: List[Callable]) -> bool:
        logger.info(f"---------Validating {name}---------")
        if os.path.exists(os.path.join(self.path, f'{name}.json')):
            with open(os.path.join(self.path, f'{name}.json'), 'rb') as fin:
                data = json.load(fin)
        elif os.path.exists(os.path.join(self.path, f'{name}.pkl')):
            with open(os.path.join(self.path, f'{name}.pkl'), 'rb') as fin:
                data = pkl.load(fin)
        else:
            raise FileNotFoundError(f"Recorded output for {name} not found. Please run Tester with record() method first.")
        passed = True
        for i, (tc, ground_truth) in enumerate(zip(cases, data)):
            try:
                out = tc()
            except Exception as e:
                logger.error(f"\tTestcase #{i+1} failed")
                logger.error(f"\tEncountered error while running testcase #{i+1}:\n {e}")
                passed = False
                continue
            if not are_equal(out, ground_truth):
                logger.error(f"\tTestcase #{i+1} failed")
                passed = False
                logger.error(f"\tExpected: {ground_truth}")
                logger.error(f"\tGot: {out}")
        if passed is False:
            logger.warning(f"Some testcases failed for {name}")
        else:
            logger.success(f"All testcases passed for {name}!")
        return passed

    def _record(self, name: str, out: List[Any]) -> None:
        try:
            with open(os.path.join(self.path, f'{name}.json'), 'w') as fout:
                json.dump(out, fout, indent=4)
        except TypeError:
            logger.warning(f"Can't save test ground truth as json, pickling instead.")
            os.remove(os.path.join(self.path, f'{name}.json'))
            with open(os.path.join(self.path, f'{name}.pkl'), 'wb') as fout:
                pkl.dump(out, fout)