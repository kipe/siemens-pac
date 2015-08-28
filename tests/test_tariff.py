# -*- encoding: utf-8 -*-
from __future__ import print_function, unicode_literals, division
from siemens.electricity import Energy, Tariff


def test_add():
    e1 = Energy(1, 1, 1)
    e2 = Energy(1, 1, 1)
    t1 = Tariff(e1, e2)
    t2 = Tariff(e1, e2)
    t_total = t1 + t2

    assert t_total.energy_import.apparent == t1.energy_import.apparent + t2.energy_import.apparent
    assert t_total.energy_import.active == t1.energy_import.active + t2.energy_import.active
    assert t_total.energy_import.reactive == t1.energy_import.reactive + t2.energy_import.reactive
    assert t_total.energy_export.apparent == t1.energy_export.apparent + t2.energy_export.apparent
    assert t_total.energy_export.active == t1.energy_export.active + t2.energy_export.active
    assert t_total.energy_export.reactive == t1.energy_export.reactive + t2.energy_export.reactive


def test_sub():
    e1 = Energy(1, 1, 1)
    e2 = Energy(1, 1, 1)
    t1 = Tariff(e1, e2)
    t2 = Tariff(e1, e2)
    t_total = t1 - t2

    assert t_total.energy_import.apparent == t1.energy_import.apparent - t2.energy_import.apparent
    assert t_total.energy_import.active == t1.energy_import.active - t2.energy_import.active
    assert t_total.energy_import.reactive == t1.energy_import.reactive - t2.energy_import.reactive
    assert t_total.energy_export.apparent == t1.energy_export.apparent - t2.energy_export.apparent
    assert t_total.energy_export.active == t1.energy_export.active - t2.energy_export.active
    assert t_total.energy_export.reactive == t1.energy_export.reactive - t2.energy_export.reactive
