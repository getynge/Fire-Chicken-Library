class TestSuite:
    def __init__(self):
        self.test_cases = []

    def insert(self, test_case):
        self.test_cases.append(test_case)
    
    def run_tests(self):
        print(self.test_cases)
        for test_case in self.test_cases:            
            test_case._private_private_test_methods()

class RunOnLoadTestSuite(TestSuite):
    def __init__(self):
        self.super().__init__()
        self.run_tests()

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
        methods = cls._private_private_get_methods_to_test_names()
        for method in methods:
            instantiation._private_private_test_method(method)
        
    
    def _private_private_test_method(self, method_name: str):
        try:
            self._private_private_run_method(method_name)
        except ProperTestFailureException as exception:
            _output_failed_test_result_with_name(exception, method_name)
        except Exception as exception:
            _output_crashed_test_exception_with_name(exception, method_name)

    def _private_private_run_method(self, method_name: str):
        method = getattr(self, method_name)
        method()

class ProperTestFailureException(Exception):
    def __init__(self, exception):
        super().__init__(exception)

class TestActualNotExpectedException(ProperTestFailureException):
    def __init__(self, actual, expected):
        message = f'Result:\nExpected:\n{expected}\nActual:\n{actual}'
        super().__init__(Exception(message))

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
        
class TestDidNotRaiseExpectedExceptionException(ProperTestFailureException):
    pass