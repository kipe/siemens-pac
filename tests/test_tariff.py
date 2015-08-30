# -*- encoding: utf-8 -*-
from __future__ import print_function, unicode_literals, division
from datetime import timedelta
from siemens.electricity import Energy, Tariff, Power


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


def test_div():
    e1 = Energy(1000, 1000, 1000)
    e2 = Energy(1000, 1000, 1000)
    p_import, p_export = Tariff(e1, e2) / 7200

    assert isinstance(p_import, Power)
    assert isinstance(p_export, Power)
    assert p_import.apparent == 1000 / 2
    assert p_export.apparent == 1000 / 2
    assert p_import.active == e1.active / 2
    assert p_export.active == e1.active / 2
    assert p_import.reactive == e1.reactive / 2
    assert p_export.reactive == e1.reactive / 2

    p_import, p_export = Tariff(e1, e2) / timedelta(minutes=30)

    assert isinstance(p_import, Power)
    assert isinstance(p_export, Power)
    assert p_import.apparent == 1000 * 2
    assert p_export.apparent == 1000 * 2
    assert p_import.active == e1.active * 2
    assert p_export.active == e1.active * 2
    assert p_import.reactive == e1.reactive * 2
    assert p_export.reactive == e1.reactive * 2


def test_balance():
    e1 = Energy(1000, 1000, 1000)
    e2 = Energy(1000, 1000, 1000)
    balance = Tariff(e1, e2).balance

    assert isinstance(balance, Energy)
    assert balance.apparent == 0
    assert balance.active == 0
    assert balance.reactive == 0
