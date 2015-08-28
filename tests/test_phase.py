# -*- encoding: utf-8 -*-
from __future__ import print_function, unicode_literals, division
from math import isnan
from siemens.electricity import Phase, Power


def test_add():
    L1 = Phase(230, 1, 2, 1)
    L2 = Phase(230, 1, 2, 1)
    L3 = Phase(230, 1, 2, 1)
    L_total = L1 + L2 + L3

    assert isinstance(L_total, Phase)
    assert L_total.voltage == 230
    assert L_total.current == 3
    assert isinstance(L_total.power, Power)
    assert L_total.power.apparent == 3 * 2
    assert L_total.power.active == 3


def test_sub():
    L1 = Phase(230, 1, 2, 1)
    L2 = Phase(230, 1, 2, 1)
    L3 = Phase(230, 1, 2, 1)
    L_total = L1 - L2 - L3

    assert isinstance(L_total, Phase)
    assert L_total.voltage == 230
    assert L_total.current == -1
    assert isinstance(L_total.power, Power)
    assert L_total.power.apparent == -2
    assert L_total.power.active == -1


def test_power_calc():
    L1 = Phase(230, 1)
    assert isinstance(L1.power, Power)
    assert L1.power.apparent == 230
    assert isnan(L1.power.active)
    assert isnan(L1.power.reactive)
