# pylint: disable=missing-function-docstring, missing-module-docstring, missing-class-docstring
import pytest
import numpy as np
import modules.expose_classes as mod
from pyccel.epyccel import epyccel

RTOL = 2e-14
ATOL = 1e-15

@pytest.fixture(scope="module")
def modnew(language):
    return epyccel(mod, language = language)

def test_class_import(language):
    class A:
        def __init__(self : 'A'):
            pass

    epyc_A = epyccel(A, language = language)

    assert isinstance(epyc_A, type)


def test_class_return(modnew):
    a = modnew.get_A()
    assert isinstance(a, modnew.A)
    a_new, i = modnew.get_A_int()
    a_new2, i2 = mod.get_A_int()
    assert isinstance(a_new, modnew.A)
    assert isinstance(a_new2, mod.A)
    assert i == i2

    b = modnew.get_B(3.0)
    assert isinstance(b, modnew.B)


def test_class_argument(modnew):
    b = modnew.get_B(3.0)
    assert isinstance(b, modnew.B)

    x = modnew.get_x_from_B(b)
    assert x == 3.0
    x = modnew.get_an_x_from_B(b)
    assert x == 3.0
    x = modnew.get_an_x_from_B()
    assert x == -2.0

def test_class_function(modnew):
    c = modnew.C()
    assert c.get_3() == 3

@pytest.mark.parametrize( 'language', (
        pytest.param("fortran", marks = [
            pytest.mark.skip(reason="Argument reference count not increased. See #1586"),
            pytest.mark.fortran]
        ),
        pytest.param("c", marks = [
            pytest.mark.skip(reason="Argument reference count not increased. See #1586"),
            pytest.mark.c]
        ),
        pytest.param("python", marks = pytest.mark.python)
    )
)
def test_classes_1(language):
    import classes.classes_1 as mod
    modnew = epyccel(mod, language = language)

    x1 = np.array([0.,0.,0.])
    x2 = np.array([0.,0.,0.])
    a = np.array([1.,1.,1.])

    p1_py = mod.Point(x1)
    p1_l  = modnew.Point(x2)

    assert np.isclose(p1_py.get_x(), p1_l.get_x(), rtol=RTOL, atol=ATOL)
    assert p1_py.get_X() == p1_l.get_X()

    p1_py.translate(a)
    p1_l.translate(a)

    assert np.isclose(p1_py.get_x(), p1_l.get_x(), rtol=RTOL, atol=ATOL)
    assert p1_py.get_X() == p1_l.get_X()
    assert np.allclose(x1, x2, rtol=RTOL, atol=ATOL)

    p2_py = mod.Point(np.array([6.,6.,6.]))
    p2_l  = modnew.Point(np.array([6.,6.,6.]))

    print(p2_py.get_x(), p2_l.get_x())

    assert np.allclose(p2_py.get_x(), p2_l.get_x())
    print(p2_py.get_x(), p2_l.get_x())
    assert p2_py.get_X() == p2_l.get_X()

    print(p2_py.get_x(), p2_l.get_x())
    p2_py.translate(a)
    print(p2_py.get_x(), p2_l.get_x())
    p2_l.translate(a)
    print(p2_py.get_x(), p2_l.get_x())

    assert np.isclose(p2_py.get_x(), p2_l.get_x(), rtol=RTOL, atol=ATOL)
    assert p2_py.get_X() == p2_l.get_X()
    assert np.allclose(x1, x2, rtol=RTOL, atol=ATOL)

    l_py = mod.Line(p1_py)
    l_l  = mod.Line(p1_l)

    assert p1_py.get_X() == p1_l.get_X()
    assert l_py.get_x() == l_l.get_x()

def test_classes_2(language):
    import classes.classes_2 as mod
    modnew = epyccel(mod, language = language)

    p_py = mod.Point()
    p_l  = modnew.Point()

    x = np.ones(4)
    y = np.full(4, 3.0)

    a_py = p_py.addition(1.1, 2.0)
    b_py = p_py.subtraction(y, x)

    a_l  = p_l.addition(1.1, 2.0)
    b_l  = p_l.subtraction(y, x)

    assert a_py == a_l
    assert isinstance(a_py, type(a_l))

    assert np.allclose(b_py, b_l, rtol=RTOL, atol=ATOL)

def test_classes_3(language):
    import classes.classes_3 as mod
    modnew = epyccel(mod, language = language)

    p2_py = mod.Point2(2.2)
    p2_l  = modnew.Point2(2.2)
    assert p2_py.test_func() == p2_l.test_func()

    p2_py = mod.Point2(6.5)
    p2_l  = modnew.Point2(6.5)
    assert p2_py.test_func() == p2_l.test_func()

    p_py = mod.Point(3.5, 0.1)
    p_l  = modnew.Point(3.5, 0.1)

    assert p_py.get_coordinates() == p_l.get_coordinates()

    p_py.set_coordinates(2.3, 5.1)
    p_l.set_coordinates(2.3, 5.1)

    assert p_py.get_coordinates() == p_l.get_coordinates()

def test_classes_4(language):
    import classes.classes_4 as mod
    modnew = epyccel(mod, language = language)

    x1 = np.array([0.,0.,0.])
    x2 = np.array([0.,0.,0.])
    a = np.array([1.,1.,1.])

    p1_py = mod.Point(x1)
    p1_l  = modnew.Point(x2)

    assert np.isclose(p1_py.get_x(), p1_l.get_x(), rtol=RTOL, atol=ATOL)

    p1_py.translate(a)
    p1_l.translate(a)

    assert np.isclose(p1_py.get_x(), p1_l.get_x(), rtol=RTOL, atol=ATOL)
    assert np.allclose(x1, x2, rtol=RTOL, atol=ATOL)

    p1_py = mod.Point()

def test_classes_6(language):
    import classes.classes_6 as mod
    modnew = epyccel(mod, language = language)

    p_py = mod.Point(0.0, 0.0)
    p_l  = modnew.Point(0.0, 0.0)

    assert p_py.get_attributes(3) == p_l.get_attributes(3)
    assert p_py.get_attributes(4.5) == p_l.get_attributes(4.5)

    p_py.translate(1.0, 2.0)
    p_l.translate(1.0, 2.0)

    assert p_py.get_attributes(3) == p_l.get_attributes(3)
    assert p_py.get_attributes(4.5) == p_l.get_attributes(4.5)

def test_generic_methods(language):
    import classes.generic_methods as mod
    modnew = epyccel(mod, language = language)

    p_py = mod.Point(0.0, 0.0)
    p_l  = modnew.Point(0.0, 0.0)

    assert p_py.get_x() == p_l.get_x()
    assert p_py.get_y() == p_l.get_y()

    p_py.translate(1.0, 2.0)
    p_l.translate(1.0, 2.0)

    assert p_py.get_x() == p_l.get_x()
    assert p_py.get_y() == p_l.get_y()

    p_py.translate(1, 2)
    p_l.translate(1, 2)

    assert p_py.get_x() == p_l.get_x()
    assert p_py.get_y() == p_l.get_y()
