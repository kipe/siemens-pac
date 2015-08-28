# -*- encoding: utf-8 -*-
from __future__ import print_function, unicode_literals, division
from datetime import timedelta
from siemens.electricity import Energy, Power


def test_add():
    e1 = Energy(1, 1, 1)
    e2 = Energy(1, 1, 1)
    e_total = e1 + e2

    assert isinstance(e_total, Energy)
    assert e_total.apparent == e1.apparent + e2.apparent
    assert e_total.active == e1.active + e2.active
    assert e_total.reactive == e1.reactive + e2.reactive


def test_sub():
    e1 = Energy(1, 1, 1)
    e2 = Energy(1, 1, 1)
    e_total = e2 - e1

    assert isinstance(e_total, Energy)
    assert e_total.apparent == e1.apparent - e2.apparent
    assert e_total.active == e1.active - e2.active
    assert e_total.reactive == e1.reactive - e2.reactive


def test_div():
    e1 = Energy(1000, 1000, 1000)
    e_total = e1 / 7200

    assert isinstance(e_total, Power)
    assert e_total.apparent == 1000 / 2
    assert e_total.active == e1.active / 2
    assert e_total.reactive == e1.reactive / 2

    e_total = e1 / timedelta(minutes=30)

    assert isinstance(e_total, Power)
    assert e_total.apparent == 1000 * 2
    assert e_total.active == e1.active * 2
    assert e_total.reactive == e1.reactive * 2
