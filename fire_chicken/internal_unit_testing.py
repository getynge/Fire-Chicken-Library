from dataclasses import dataclass
from enum import Enum
from .knausj_boundary import *
from .path_utilities import *
from talon import actions

class TestSuite:
    available_default_instance_list = [1]
    def __init__(self, name="", *, directory="", display_results=True, notify=True):
        self.test_cases = []
        if name != "":
            self.name = name
        else:
            self.name = self._get_default_name()
        self._test_output_directory = directory
        self.display_results = display_results
        self.notify = notify

    def __del__(self):
        if self.name.isdigit():
            TestSuite.available_default_instance_list.append(int(self.name))


    def _get_default_name(self):
        next_instance = min(TestSuite.available_default_instance_list)
        if len(TestSuite.available_default_instance_list) == 1:
            TestSuite.available_default_instance_list[0] = next_instance + 1
        else:
            TestSuite.available_default_instance_list.remove(next_instance)
        return str(next_instance)

    def insert(self, test_case):
        self.test_cases.append(test_case)
    
    def run_tests(self):
        failed_test_results = []
        for test_case in self.test_cases:            
            failed_test_results.extend(test_case._private_private_test_methods())
        if failed_test_results != []:
            _output_test_results(self.name,failed_test_results,self._test_output_directory,self.display_results)
            if self.notify:
                actions.app.notify('Test Suite ' + self.name + ' reported failure!')

def _output_test_results(name, results, directory="", display_results=True):
    output_directory = _prepare_output_directory(directory)
    output_file = _compute_output_filepath_in_directory_with_filename(output_directory, name)
    _output_test_results_to_file(results, output_file)
    if display_results:
        actions.user.edit_text_file(output_file)


def _compute_output_filepath_in_directory_with_filename(directory, test_name):
    output_filepath = join_path(directory, test_name + ".txt")
    return output_filepath

def _prepare_output_directory(directory=""):
    if directory == "":
        data_directory = _get_data_directory()
        test_output_directory = join_path(data_directory, "test_output")
    else:
         test_output_directory = directory
    create_directory_if_nonexistent(test_output_directory)
    return test_output_directory

def _get_data_directory():
    python_file_directory = compute_file_directory(__file__)
    data_directorydata_directory = join_path(python_file_directory, "data")
    return data_directorydata_directory

def _output_test_results_to_file(results, output_file):
    with open(output_file, 'w') as test_result_file:
        test_result_file.write(f"{len(results)} tests failed")
        for result in results:
            test_result_file.write("\n\n")
            if _test_failed_normally(result):
                test_result_file.write(_compute_failed_test_result_output(result.exception, result.test_name))
            elif _test_crashed_unexpectedly(result):
                test_result_file.write(_compute_crashed_test_result_output(result.exception, result.test_name))

def _compute_failed_test_result_output(exception: Exception, test_name: str):
    return f'The following test failed: {test_name}.\n{exception}'

def _compute_crashed_test_result_output(exception: Exception, test_name: str):
    return f'The following test crashed: {test_name}.\nIt gave the following crash error: {exception}'

def _test_failed_normally(test_result):
    return test_result.failure_type == FailureType.ACTUAL_NOT_EXPECTED

def _test_crashed_unexpectedly(test_result):
    return test_result.failure_type == FailureType.CRASH


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
        failed_test_results = instantiation._private_private_test_methods_of_instantiation()
        return failed_test_results

    def _private_private_test_methods_of_instantiation(self):
        failed_test_results = []
        methods = self._private_private_get_methods_to_test_names()
        for method in methods:
            self._private_private_add_method_test_result_to_list(method, failed_test_results)
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
        self._before_each()
        test_result = super()._private_private_test_method(method_name)
        self._after_each()
        return test_result

    @classmethod
    def _private_private_test_methods(cls):
        instantiation = cls()
        instantiation._before_all()
        failed_test_results = instantiation._private_private_test_methods_of_instantiation()
        instantiation._after_all()
        return failed_test_results

    def _before_each(self):
        pass

    def _after_each(self):
        pass

    def _before_all(self):
        pass

    def _after_all(self):
        pass

class DraftTextTestCase(SetupTestCase):
    def _before_each(self):
        # open draft window and delete all text
        open_empty_draft_window()

    
    def _after_each(self):
        # delete all text from draft window and hide it
        discard_draft_window_draft()

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

def assert_draft_window_test_equals(expected: str):
    previous_draft_text = ''
    current_draft_text = None
    while current_draft_text != previous_draft_text :
        previous_draft_text = get_draft_window_text()
        actions.sleep('500ms')
        current_draft_text = get_draft_window_text()
    actual = current_draft_text
    assert_actual_equals_expected(actual, expected)

class ProperTestFailureException(Exception):
    def __init__(self, exception):
        super().__init__(exception)

class TestActualNotExpectedException(ProperTestFailureException):
    def __init__(self, actual, expected):
        message = f'Result:\nExpected:\n{expected}\nActual:\n{actual}'
        super().__init__(Exception(message))

class TestDidNotRaiseExpectedExceptionException(ProperTestFailureException):
    pass
