from ..fire_chicken.internal_unit_testing import *
from talon import Module, actions

def test_assert_actual_equals_expected_fails_properly():
    try:
        assert_actual_equals_expected('actual', 'expected')
        raise Exception('test_assert_actual_equals_expected_fails_properly did not raise proper exception!')
    except TestActualNotExpectedException as exception:
        assert(str(exception) == 'Result:\nExpected:\nexpected\nActual:\nactual')

test_assert_actual_equals_expected_fails_properly()


class TestCaseTest(TestCase):
    def this_should_fail_properly(self):
        raise TestActualNotExpectedException('no actual value', 'failed without crashing')
        
    def this_will_crash(self):
        raise ValueError('crash')
    def _another_test_that_should_not_be_included(self):
        pass

    def two_plus_two_equals_four(self):
        assert_actual_equals_expected(2+2, 4)

    def failed_version_of_two_plus_two_equals_four(self):
        assert_actual_equals_expected(2+1, 4)

    def true_is_true(self):
        assert_true(True)

    def failed_version_of_true_is_true(self):
        assert_true(False)

    def false_is_false(self):
        assert_false(False)

    def failed_version_of_false_is_false(self):
        assert_false(True)

    def test_assert_failure_with_expected_exception(self):
        def raise_value_error():
            raise ValueError()
        assert_function_fails_with_exception_given_arguments(raise_value_error, ValueError)

    def test_assert_failure_without_exception(self):
        def raised_no_exceptions():
            return 5
        assert_function_fails_with_exception_given_arguments(raised_no_exceptions, ValueError)

    def test_assert_failure_with_argument_and_expected_exception(self):
        def raise_value_error(argument):
            raise ValueError()
        assert_function_fails_with_exception_given_arguments(raise_value_error, ValueError, 14)

    def test_assert_failure_with_argument_without_exception(self):
        def raise_value_error(argument):
            return argument
        assert_function_fails_with_exception_given_arguments(raise_value_error, ValueError, 14)

    def _this_method_should_not_get_tested(self):
        pass

def test_test_case():
    test_test_case_results()
    test_test_case_excludes_proper_method_names()

def test_test_case_results():
    results = get_test_results(TestCaseTest)

    test_this_should_fail_properly_fails_properly(results)
    test_this_will_crash_crashes(results)
    test_two_plus_two_equals_four_passes(results, TestCaseTest)
    test_failed_version_of_two_plus_two_equals_four_fails_properly(results)
    test_true_is_true_passes(results, TestCaseTest)
    test_failed_version_of_true_is_true_fails_properly(results)
    test_false_is_false_passes(results, TestCaseTest)
    test_failed_version_of_false_is_false_fails_properly(results)
    test_test_assert_failure_with_expected_exception_passes(results, TestCaseTest)
    test_test_assert_failure_without_exception_fails_properly(results)
    test_test_assert_failure_with_argument_and_expected_exception_passes(results, TestCaseTest)
    test_test_assert_failure_with_argument_without_exception_fails_properly(results)

def test_this_should_fail_properly_fails_properly(results):
    function_name = 'this_should_fail_properly'
    assert_test_fails_properly(results, function_name)

def test_this_will_crash_crashes(results):
    function_name = 'this_will_crash'
    assert_test_crashes(results, function_name)

def test_two_plus_two_equals_four_passes(results, class_name):
    function_name = 'two_plus_two_equals_four'
    assert_test_passed(results, function_name, class_name)

def test_failed_version_of_two_plus_two_equals_four_fails_properly(results):
    function_name = 'failed_version_of_two_plus_two_equals_four'
    assert_test_fails_properly(results, function_name)

def test_true_is_true_passes(results, class_name):
    function_name = 'true_is_true'
    assert_test_passed(results, function_name, class_name)

def test_failed_version_of_true_is_true_fails_properly(results):
    function_name = 'failed_version_of_true_is_true'
    assert_test_fails_properly(results, function_name)

def test_false_is_false_passes(results, class_name):
    function_name = 'false_is_false'
    assert_test_passed(results, function_name, class_name)

def test_failed_version_of_false_is_false_fails_properly(results):
    function_name = 'failed_version_of_false_is_false'
    assert_test_fails_properly(results, function_name)

def test_test_assert_failure_with_expected_exception_passes(results, class_name):
    function_name = 'test_assert_failure_with_expected_exception'
    assert_test_passed(results, function_name, class_name)

def test_test_assert_failure_without_exception_fails_properly(results):
    function_name = 'test_assert_failure_without_exception'
    assert_test_fails_properly(results, function_name)

def test_test_assert_failure_with_argument_and_expected_exception_passes(results, class_name):
    function_name = 'test_assert_failure_with_argument_and_expected_exception'
    assert_test_passed(results, function_name, class_name)

def test_test_assert_failure_with_argument_without_exception_fails_properly(results):
    function_name = 'test_assert_failure_with_argument_without_exception'
    assert_test_fails_properly(results, function_name)


def assert_test_fails_properly(results, name):
    assert_test_failed(results, name)
    assert(results[name].failure_type == FailureType.ACTUAL_NOT_EXPECTED)

def assert_test_crashes(results, name):
    assert_test_failed(results, name)
    assert(results[name].failure_type == FailureType.CRASH)

def assert_test_failed(results, name):
    assert(name in results)

def assert_test_passed(results, method_name, class_name):
    assert(method_name not in results)
    assert_class_has_attribute(class_name, method_name)

def assert_class_has_attribute(class_name, method_name: str):
    assert(hasattr(class_name, method_name))

def get_test_results(test_case_class):
    test_results_list = test_case_class._private_private_test_methods()
    test_results_dictionary = {}
    for result in test_results_list:
        test_results_dictionary[result.test_name] = result
    return test_results_dictionary


def test_test_case_excludes_proper_method_names():
    method_name = "_this_method_should_not_get_tested"
    test_case_class = TestCaseTest

    assert_method_not_in_failed_test_results(method_name, test_case_class)
    assert_method_not_in_methods_to_test(method_name, test_case_class)
    assert_method_in_test_case_methods(method_name, test_case_class)

def assert_method_not_in_failed_test_results(method_name, test_case_class):
    results = test_case_class._private_private_test_methods()
    assert(method_name not in results)

def assert_method_not_in_methods_to_test(method_name, test_case_class):
    methods_to_test = test_case_class._private_private_get_methods_to_test_names()
    assert(method_name not in methods_to_test)

def assert_method_in_test_case_methods(method_name, test_case_class):
    methods = test_case_class._private_private_get_methods()
    assert(method_name in methods)

test_test_case()

class SetupTestCaseSimpleTest(SetupTestCase):
    def this_should_pass(self):
        pass

    def this_should_crash(self):
        raise Exception()
    
    def this_should_fail_normally(self):
        assert_true(False)


class SetupTestCaseTest(SetupTestCase):
    def _before_all(self):
        self.method_call_number = 0
        self.before_each_called = False
        self.before_all_called = True
        self.after_all_called = False
        self.after_each_called = False

    def _before_each(self):
        self.method_call_number += 1
        self.before_each_called = True
    
    def _after_each(self):
        self.after_each_called = True
    
    def _after_all(self):
        self.after_all_called = True
        self._assert_all_conditions_true()

    def _assert_all_conditions_true(self):
        assert_true(self.before_each_called)
        assert_true(self.before_all_called)
        assert_true(self.after_all_called)
        assert_true(self.after_each_called)

    def test_one(self):
        self._assert_correct_conditions()
    
    def test_two(self):
        self._assert_correct_conditions()
    
    def _assert_correct_conditions(self):
        if self.method_call_number == 1:
            self._assert_only_before_all_and_before_each_called()
        elif self.method_call_number == 2:
            self._assert_only_before_all_before_each_and_after_each_called()

    def _assert_only_before_all_and_before_each_called(self):
        assert_true(self.before_each_called)
        assert_true(self.before_all_called)
        assert_false(self.after_all_called)
        assert_false(self.after_each_called)

    def _assert_only_before_all_before_each_and_after_each_called(self):
        assert_true(self.before_each_called)
        assert_true(self.before_all_called)
        assert_true(self.after_each_called)
        assert_false(self.after_all_called)
        

def test_setup_test_case():
    test_simple_parent_class_functionality_still_works()
    test_setup_functionality()

def test_simple_parent_class_functionality_still_works():
    class_name = SetupTestCaseSimpleTest
    results = get_test_results(class_name)
    
    assert_test_passed(results, 'this_should_pass', class_name)
    assert_test_crashes(results, 'this_should_crash')
    assert_test_fails_properly(results, 'this_should_fail_normally')

def test_setup_functionality():
    class_name = SetupTestCaseTest
    results = get_test_results(class_name)

    assert_test_passed(results, 'test_one', class_name)
    assert_test_passed(results, 'test_two', class_name)


test_setup_test_case()

class TestDraftTextTestCase(DraftTextTestCase):
    def test_equals_expected(self):
        expected_text = 'expected'
        actions.insert(expected_text)
        assert_draft_window_test_equals(expected_text)

    def test_equals_incorrect_expectation_should_fail(self):
        actions.insert('the wrong text')
        assert_draft_window_test_equals('incorrect expectation')

    def test_this_can_handle_longer_text(self):
        expected_text = 'This is a longer text to be inserted to see if the code will accidentally close the draft window too soon.'

        actions.insert(expected_text)
        assert_draft_window_test_equals(expected_text)

    def test_prefix_results_in_failure(self):
        prefix = 'this is the start'
        expected = prefix + ' and this is the ending'

        actions.insert(prefix)
        assert_draft_window_test_equals(expected)

module = Module()
@module.action_class
class Actions:
    def fire_chicken_library_testing_test_draft_text_test_case():
        '''Tests TestSetupTestCase'''
        classname = TestDraftTextTestCase
        results = get_test_results(classname)
        assert_test_passed(results, 'test_equals_expected', classname)
        assert_test_passed(results, 'test_this_can_handle_longer_text', classname)
        assert_test_fails_properly(results, 'test_equals_incorrect_expectation_should_fail')
        assert_test_fails_properly(results, 'test_prefix_results_in_failure')
