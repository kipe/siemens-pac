from __future__ import unicode_literals, print_function, division
from math import isnan, sqrt
from numbers import Number
from datetime import timedelta


class Power(object):
    def __init__(self, apparent=float('nan'), active=float('nan'), reactive=float('nan')):
        self.apparent = apparent
        self.active = active
        self._reactive = reactive

    def __repr__(self):
        return '<Power: %s VA, %s W, %s VAR>' % (self.apparent, self.active, self.reactive)

    def __str__(self):
        return self.__repr__()

    def __add__(self, other):
        if not isinstance(other, Power):
            raise TypeError('unsupported operand type(s) for +')
        return Power(apparent=self.apparent + other.apparent, active=self.active + other.active)

    def __sub__(self, other):
        if not isinstance(other, Power):
            raise TypeError('unsupported operand type(s) for -')
        return Power(apparent=self.apparent - other.apparent, active=self.active - other.active)

    @property
    def reactive(self):
        if not isnan(self._reactive):
            return self._reactive
        return sqrt(self.apparent ** 2 - self.active ** 2)

    @property
    def power_factor(self):
        return self.active / self.apparent

    def as_dict(self, replace_nan=False):
        if replace_nan:
            return {
                'apparent': self.apparent if not isnan(self.apparent) else 0,
                'active': self.active if not isnan(self.active) else 0,
                'reactive': self.reactive if not isnan(self.reactive) else 0,
            }

        return {
            'apparent': self.apparent,
            'active': self.active,
            'reactive': self.reactive,
        }


class Phase(object):
    power = Power()
    voltage = float('nan')
    current = float('nan')

    def __init__(self, voltage=float('nan'), current=float('nan'), apparent=float('nan'), active=float('nan')):
        self.voltage = voltage
        self.current = current
        self.power = Power(apparent, active)

    def __repr__(self):
        return '<Phase: %s V, %s A, %s>' % (self.voltage, self.current, self.power.__repr__())

    def __str__(self):
        return self.__repr__()

    def __add__(self, other):
        if not isinstance(other, Phase):
            raise TypeError('unsupported operand type(s) for +')
        return Phase(
            voltage=(self.voltage + other.voltage) / 2,
            current=self.current + other.current,
            apparent=self.power.apparent + other.power.apparent,
            active=self.power.active + other.power.active)

    def __sub__(self, other):
        if not isinstance(other, Phase):
            raise TypeError('unsupported operand type(s) for -')
        return Phase(
            voltage=(self.voltage + other.voltage) / 2,
            current=self.current - other.current,
            apparent=self.power.apparent - other.power.apparent,
            active=self.power.active - other.power.active)

    def as_dict(self, replace_nan=False):
        if replace_nan:
            return {
                'power': self.power.as_dict(replace_nan=True),
                'voltage': self.voltage if not isnan(self.voltage) else 0,
                'current': self.current if not isnan(self.current) else 0,
            }

        return {
            'power': self.power.as_dict(replace_nan=False),
            'voltage': self.voltage,
            'current': self.current,
        }


class Energy(object):
    def __init__(self, apparent=float('nan'), active=float('nan'), reactive=float('nan')):
        self.apparent = apparent
        self.active = active
        self.reactive = reactive

    def __repr__(self):
        return '<Energy: %s VAh, %s Wh, %s VARh>' % (self.apparent, self.active, self.reactive)

    def __str__(self):
        return self.__repr__()

    def __add__(self, other):
        if not isinstance(other, Energy):
            raise TypeError('unsupported operand type(s) for +')
        return Energy(
            apparent=self.apparent + other.apparent,
            active=self.active + other.active,
            reactive=self.reactive + other.reactive)

    def __sub__(self, other):
        if not isinstance(other, Energy):
            raise TypeError('unsupported operand type(s) for -')
        return Energy(
            apparent=self.apparent - other.apparent,
            active=self.active - other.active,
            reactive=self.reactive - other.reactive)

    def __div__(self, t):
        ''' Divides Energy with timedelta or seconds, to allow easy calculation of average power '''
        if not isinstance(t, timedelta) and not isinstance(t, Number):
            raise TypeError('division allowed only by timedelta or number')
        if isinstance(t, timedelta):
            t = t.total_seconds()

        return Power(
            apparent=self.apparent / t * 3600,
            active=self.active / t * 3600,
            reactive=self.reactive / t * 3600,
        )

    def __truediv__(self, t):
        return self.__truediv__(t)

    def as_dict(self, replace_nan=False):
        if replace_nan:
            return {
                'apparent': self.apparent if not isnan(self.apparent) else 0,
                'active': self.active if not isnan(self.active) else 0,
                'reactive': self.reactive if not isnan(self.reactive) else 0,
            }

        return {
            'apparent': self.apparent,
            'active': self.active,
            'reactive': self.reactive,
        }


class Tariff(object):
    def __init__(self, energy_import=Energy(), energy_export=Energy()):
        self.energy_import = energy_import
        self.energy_export = energy_export

    def __repr__(self):
        return '<Tariff: import: %s, export: %s>' % (self.energy_import.__repr__(), self.energy_export.__repr__())

    def __str__(self):
        return self.__repr__()

    def __add__(self, other):
        if not isinstance(other, Tariff):
            raise TypeError('unsupported operand type(s) for +')
        return Tariff(
            energy_import=self.energy_import + other.energy_import,
            energy_export=self.energy_export + other.energy_export)

    def __sub__(self, other):
        if not isinstance(other, Tariff):
            raise TypeError('unsupported operand type(s) for -')
        return Tariff(
            energy_import=self.energy_import - other.energy_import,
            energy_export=self.energy_export - other.energy_export)

    @property
    def balance(self):
        return self.energy_import - self.energy_export

    def as_dict(self, replace_nan=False):
        return {
            'import': self.energy_import.as_dict(replace_nan=replace_nan),
            'export': self.energy_export.as_dict(replace_nan=replace_nan),
        }
