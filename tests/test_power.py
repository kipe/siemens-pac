# -*- encoding: utf-8 -*-
from __future__ import print_function, unicode_literals, division
from datetime import timedelta
from math import sqrt
from siemens.electricity import Energy, Power


def test_add():
    p1 = Power(1, 1, 1)
    p2 = Power(1, 1, 1)
    p_total = p1 + p2

    assert isinstance(p_total, Power)
    assert p_total.apparent == p1.apparent + p2.apparent
    assert p_total.active == p1.active + p2.active
    assert p_total.reactive != p1.reactive + p2.reactive
    assert p_total.reactive == sqrt((p2.apparent + p1.apparent) ** 2 - (p2.active + p1.active) ** 2)


def test_sub():
    # Reactive power values shouldn't matter -> setting them here to something absurd.
    p2 = Power(3, 2, 3)
    p1 = Power(2, 1, 4)
    p_total = p2 - p1

    assert isinstance(p_total, Power)
    assert p_total.apparent == p2.apparent - p1.apparent
    assert p_total.active == p2.active - p1.active
    assert p_total.reactive != p2.reactive - p1.reactive
    assert p_total.reactive == sqrt((p2.apparent - p1.apparent) ** 2 - (p2.active - p1.active) ** 2)


def test_mul():
    p1 = Power(1000, 1000, 1000)
    p_total = p1 * 7200

    assert isinstance(p_total, Energy)
    assert p_total.apparent == 1000 * 2
    assert p_total.active == p1.active * 2
    assert p_total.reactive == p1.reactive * 2

    p_total = p1 * timedelta(minutes=30)

    assert isinstance(p_total, Energy)
    assert p_total.apparent == 1000 / 2
    assert p_total.active == p1.active / 2
    assert p_total.reactive == p1.reactive / 2
