import pytest
from pytest import fixture

from easy_framework.exception import AuthMissingError
from easy_framework.validator import BaseValidator


class TestBaseValidator():
    @fixture
    def testTrueValidator(self):
        class TrueValidator(BaseValidator):
            def validate(self) -> bool:
                pass
        return TrueValidator

    @fixture
    def testFalseValidator(self):
        class FalseValidator(BaseValidator):
            def validate(self) -> bool:
                raise AuthMissingError()
        return FalseValidator

    @fixture
    def testParamValidator(self):
        class ParamValidator(BaseValidator):
            def validate(self, shouldRaise: bool) -> bool:
                if shouldRaise:
                    raise AuthMissingError()
        return ParamValidator

    class ObjectiveClass():
        def __new__(cls) -> str:
            return True

    def test_validade_the_objective_function_and_return_true_with_a_valid_validator(self, testTrueValidator):
        @testTrueValidator()
        class _ObjectiveClass(self.ObjectiveClass):
            pass

        assert _ObjectiveClass() is True

    def test_validade_the_objective_function_and_catch_exception_with_an_invalid_validator(self, testFalseValidator):
        @testFalseValidator()
        class _ObjectiveClass(self.ObjectiveClass):
            pass
        with pytest.raises(AuthMissingError) as exc_info:
            assert _ObjectiveClass() is not True
            assert exc_info is AuthMissingError

    def test_validate_the_objective_function_with_decorator_with_params_and_get_true(self, testParamValidator):
        @testParamValidator(False)
        class _ObjectiveClass(self.ObjectiveClass):
            pass
        assert _ObjectiveClass() is True

    def test_validate_the_objective_function_with_decorator_with_params_and_catch_exception(self, testParamValidator):
        @testParamValidator(True)
        class _ObjectiveClass(self.ObjectiveClass):
            pass

        with pytest.raises(AuthMissingError) as exc_info:
            assert _ObjectiveClass() is not True
            assert exc_info is AuthMissingError

    def test_validade_the_objective_function_with_params_and_get_true_with_a_valid_validator(self, testParamValidator):
        @testParamValidator(False)
        class _ObjectiveClass():
            def __init__(self, foo: bool, bar: str, eggs: int):
                pass

            def func(self):
                return True

        assert _ObjectiveClass(True, 'test', 100).func() is True

    def test_validade_the_objective_function_with_internal_funciton_with_params_and_get_true_with_a_valid_validator(self, testParamValidator):
        @testParamValidator(False)
        class _ObjectiveClass():
            def __init__(self):
                pass

            def func(self, foo: bool, bar: str, eggs: int):
                return True

        assert _ObjectiveClass().func(True, 'test', 100) is True

    def test_validade_the_objective_function_with_internal_funciton_with_params_and_validate_internal_params_with_a_valid_validator(self, testParamValidator):
        @testParamValidator(False)
        class _ObjectiveClass():
            def __init__(self):
                pass

            def func(self, foo: bool, bar: str, eggs: int):
                self.foo = foo
                self.bar = bar
                self.eggs = eggs

        func = _ObjectiveClass()
        func.func(True, 'test', 100)

        assert func.foo == True
        assert func.bar == 'test'
        assert func.eggs == 100