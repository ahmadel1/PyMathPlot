import pytest
import numpy as np
from src.model import FunctionModel

@pytest.fixture
def function_model():
    return FunctionModel()

def test_set_fx(function_model):
    function_model.set_fx("x**2 + 2*x + 1")
    assert function_model.fx is not None
    assert str(function_model.fx) == "x**2 + 2*x + 1"

def test_set_gx(function_model):
    function_model.set_gx("x+1")
    assert function_model.gx is not None
    assert str(function_model.gx) == "x + 1"

def test_evaluate_fx(function_model):
    function_model.set_fx("x**2")
    x_values = [0, 1, 2, 3]
    expected_values = np.array([0, 1, 4, 9])
    np.testing.assert_array_equal(function_model.evaluate(function_model.fx, x_values), expected_values)

def test_evaluate_gx(function_model):
    function_model.set_gx("2*x + 3")
    x_values = [0, 1, 2, 3]
    expected_values = np.array([3, 5, 7, 9])
    np.testing.assert_array_equal(function_model.evaluate(function_model.gx, x_values), expected_values)

def test_find_intersections(function_model):
    function_model.set_fx("x**2 - 4")
    function_model.set_gx("x - 2")
    intersections = function_model.find_intersections(range(-10, 10))
    expected_intersections = [(-1.0, -3.0), (2.0, 0.0)]
    intersections = [(round(x, 5), round(y, 5)) for x, y in intersections]
    expected_intersections = [(round(x, 5), round(y, 5)) for x, y in expected_intersections]
    assert intersections is not None
    assert len(intersections) == 2  
    assert set(intersections) == set(expected_intersections)


def test_parase_function(function_model):
    expression = ""
    function_model.parse_function(expression)