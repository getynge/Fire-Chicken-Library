from dataclasses import dataclass
from enum import Enum
from talon import actions

class TestSuite:
    def __init__(self):
        self.test_cases = []

    def insert(self, test_case):
        self.test_cases.append(test_case)
    
    def run_tests(self):
        failed_test_results = []
        for test_case in self.test_cases:            
            failed_test_results.extend(test_case._private_private_test_methods())
        _output_test_results(failed_test_results)

def _output_test_results(results):
    for result in results:
        if result.failure_type == FailureType.ACTUAL_NOT_EXPECTED:
            _output_failed_test_result_with_name(result.exception, result.test_name)
        elif result.failure_type == FailureType.CRASH:
            _output_crashed_test_exception_with_name(result.exception, result.test_name)

def _output_failed_test_result_with_name(exception: Exception, test_name: str):
    print(f'The following test failed: {test_name}.')
    print(exception)

def _output_crashed_test_exception_with_name(exception: Exception, test_name: str):
    print(f'The following test crashed: {test_name}')
    print(f'It gave the following crash error: {exception}')

class TestCase:
    @classmethod
    def _private_private_get_methods_to_test_names(cls):
        method_names = cls._private_private_get_methods()
        methods_to_test_names = [method_name for method_name in method_names if cls._private_private_should_test_method(method_name)]
        return methods_to_test_names
    @classmethod
    def _private_private_get_methods(cls):
        return dir(cls)
    @classmethod
    def _private_private_should_test_method(cls, method_name: str):
        return not method_name.startswith('_')

    @classmethod
    def _private_private_test_methods(cls):
        instantiation = cls()
        failed_test_results = []
        methods = cls._private_private_get_methods_to_test_names()
        for method in methods:
                instantiation._private_private_add_method_test_result_to_list(method, failed_test_results)
        return failed_test_results
    
    
    def _private_private_add_method_test_result_to_list(self, method, list):
            test_result = self._private_private_test_method(method)
            if self._private_private_should_add_test_result(test_result):
                list.append(test_result)

    def _private_private_should_add_test_result(self, result):
        return result is not None

    def _private_private_test_method(self, method_name: str):
        try:
            self._private_private_run_method(method_name)
        except ProperTestFailureException as exception:
            return FailedTestResult(exception, method_name, FailureType.ACTUAL_NOT_EXPECTED)
        except Exception as exception:
            return FailedTestResult(exception, method_name, FailureType.CRASH)

    def _private_private_run_method(self, method_name: str):
        method = getattr(self, method_name)
        method()

class SetupTestCase(TestCase):
    def _private_private_test_method(self, method_name: str):
        self._setup()
        test_result = super()._private_private_test_method(method_name)
        self._teardown()
        return test_result

    def _setup(self):
        pass

    def _teardown(self):
        pass

FailureType = Enum('FailureType', 'ACTUAL_NOT_EXPECTED CRASH')

@dataclass
class FailedTestResult:
    exception: Exception
    test_name: str
    failure_type: FailureType


def assert_false(condition):
    assert_actual_equals_expected(condition, False)

def assert_true(condition):
    assert_actual_equals_expected(condition, True)

def assert_actual_equals_expected(actual, expected):
    if actual != expected:
        raise TestActualNotExpectedException(actual, expected)

def assert_function_fails_with_exception_given_arguments(function, exception, *args):
    try:
        function(*args)
        raise TestDidNotRaiseExpectedExceptionException('The test failed to raise any exceptions!')
    except exception as expected_exception:
        pass
        

class ProperTestFailureException(Exception):
    def __init__(self, exception):
        super().__init__(exception)

class TestActualNotExpectedException(ProperTestFailureException):
    def __init__(self, actual, expected):
        message = f'Result:\nExpected:\n{expected}\nActual:\n{actual}'
        super().__init__(Exception(message))

class TestDidNotRaiseExpectedExceptionException(ProperTestFailureException):
    pass

class DraftTextTestCase(SetupTestCase):
    def _setup(self):
        # open draft window and delete all text
        actions.user.draft_show("")

    
    def _teardown(self):
        # delete all text from draft window and hide it
        actions.user.draft_show("")
        actions.user.draft_hide()


def assert_draft_window_test_equals(expected: str):
    actual = actions.user.draft_get_text()
    assert_actual_equals_expected(actual,expected)
