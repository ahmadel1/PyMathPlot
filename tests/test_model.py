import pytest
import numpy as np
from src.model import FunctionModel
from sympy import Symbol

@pytest.fixture
def function_model():
    return FunctionModel()

def test_set_fx_none(function_model):
    res, err = function_model.set_fx(None)
    assert res is True
    assert err is None
    assert function_model.fx is None

def test_set_fx_empty(function_model):
    res, err = function_model.set_fx("")
    assert res is False
    assert "cannot be empty" in err

def test_set_fx_whitespace(function_model):
    res, err = function_model.set_fx("   ")
    assert res is False
    assert "cannot be empty" in err

def test_set_fx_invalid_expression(function_model):
    res, err = function_model.set_fx("x+y+1")
    assert res is False
    assert "Error parsing expression" in err

def test_set_fx_valid_expression(function_model):
    res, err = function_model.set_fx("x^2 + x + 1")
    assert res is True
    assert err is None
    assert function_model.fx is not None

def test_set_fx_with_invalid_variable(function_model):
    res, err = function_model.set_fx("y^2 + y + 1")
    assert res is False
    assert "Unknown symbol(s) used" in err

def test_set_gx_none(function_model):
    res, err = function_model.set_gx(None)
    assert res is True
    assert err is None
    assert function_model.gx is None

def test_set_gx_empty(function_model):
    res, err = function_model.set_gx("")
    assert res is False
    assert "cannot be empty" in err

def test_set_gx_valid_expression(function_model):
    res, err = function_model.set_gx("2*x + 1")
    assert res is True
    assert err is None
    assert function_model.gx is not None

def test_evaluate_none_function(function_model):
    y_vals, err = function_model.evaluate(None, [1, 2, 3])
    assert y_vals is None
    assert err is None

def test_evaluate_valid_function(function_model):
    function_model.set_fx("x^2")
    y_vals, err = function_model.evaluate(function_model.fx, [0, 1, 2])
    assert err is None
    np.testing.assert_array_almost_equal(y_vals, [0, 1, 4])

def test_evaluate_with_invalid_input(function_model):
    function_model.set_fx("x^2")
    y_vals, err = function_model.evaluate(function_model.fx, ["a", "b"])
    assert y_vals is None
    assert "Error evaluating function" in err

def test_evaluate_complex_expression(function_model):
    function_model.set_fx("sin(x) + cos(x)")
    y_vals, err = function_model.evaluate(function_model.fx, [0, np.pi/2])
    assert err is None
    np.testing.assert_array_almost_equal(y_vals, [1, 1])


def test_find_intersections_no_functions(function_model):
    intersections, err = function_model.find_intersections([0, 1, 2])
    assert len(intersections) == 0
    assert err is None

def test_find_intersections_with_intersection(function_model):
    function_model.set_fx("x")
    function_model.set_gx("-x")
    intersections, err = function_model.find_intersections([-10, 0, 10])
    assert err is None
    assert len(intersections) > 0
    assert (0.0,0.0) in intersections 

def test_find_intersections_no_intersection(function_model):
    function_model.set_fx("x + 1")
    function_model.set_gx("x - 1")
    intersections, err = function_model.find_intersections([0, 1])
    assert err is None
    assert len(intersections) == 0

def test_find_intersections_outside_range(function_model):
    function_model.set_fx("x")
    function_model.set_gx("x")
    intersections, err = function_model.find_intersections([1, 2])  # intersection at x=0 is outside range
    assert err is None
    assert len(intersections) == 0

def test_get_intersection_view_bounds_no_intersections(function_model):
    bounds = function_model.get_intersection_view_bounds()
    assert bounds is None

def test_get_intersection_view_bounds_single_intersection(function_model):
    function_model.intersections = [(1, 1)]
    bounds = function_model.get_intersection_view_bounds()
    assert bounds['x_min'] == -1
    assert bounds['x_max'] == 3
    assert bounds['y_min'] == -1
    assert bounds['y_max'] == 3

def test_get_intersection_view_bounds_multiple_intersections(function_model):
    function_model.intersections = [(0, 0), (1, 1), (2, 2)]
    bounds = function_model.get_intersection_view_bounds()
    assert bounds['x_min'] < 0
    assert bounds['x_max'] > 2
    assert bounds['y_min'] < 0
    assert bounds['y_max'] > 2

def test_parse_expression_valid(function_model):
    expr = function_model._parse_expression("x^2 + 1")
    assert expr is not None
    assert Symbol('x') in expr.free_symbols

def test_parse_expression_with_constants(function_model):
    expr = function_model._parse_expression("pi*x + e")
    assert expr is not None
    assert Symbol('x') in expr.free_symbols