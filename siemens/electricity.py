from __future__ import unicode_literals, print_function, division
from math import isnan, sqrt
from numbers import Number
from datetime import timedelta


def zero_if_nan(value, replace_nan):
    return 0 if isnan(value) and replace_nan else value


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

    def __mul__(self, t):
        ''' Multiplies Power with timedelta or seconds, to allow easy calculation of average Energy. '''
        if not isinstance(t, timedelta) and not isinstance(t, Number):
            raise TypeError('division allowed only by timedelta or number')
        if isinstance(t, timedelta):
            t = t.total_seconds()

        return Energy(
            apparent=self.apparent / 3600 * abs(t),
            active=self.active / 3600 * abs(t),
            reactive=self.reactive / 3600 * abs(t),
        )

    @property
    def reactive(self):
        if not isnan(self._reactive):
            return self._reactive
        return sqrt(self.apparent ** 2 - self.active ** 2)

    @property
    def power_factor(self):
        return self.active / self.apparent

    def as_dict(self, replace_nan=False):
        return {
            'apparent': {
                'unit': 'VA',
                'value': zero_if_nan(self.apparent, replace_nan),
            },
            'active': {
                'unit': 'W',
                'value': zero_if_nan(self.active, replace_nan),
            },
            'reactive': {
                'unit': 'VAR',
                'value': zero_if_nan(self.reactive, replace_nan),
            },
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
        ''' Divides Energy with timedelta or seconds, to allow easy calculation of average Power. '''
        if not isinstance(t, timedelta) and not isinstance(t, Number):
            raise TypeError('division allowed only by timedelta or number')
        if isinstance(t, timedelta):
            t = t.total_seconds()

        return Power(
            apparent=self.apparent / abs(t) * 3600,
            active=self.active / abs(t) * 3600,
            reactive=self.reactive / abs(t) * 3600,
        )

    def __truediv__(self, t):
        ''' Divides Energy with timedelta or seconds, to allow easy calculation of average Power. '''
        return self.__div__(t)

    def as_dict(self, replace_nan=False):
        return {
            'apparent': {
                'unit': 'VAh',
                'value': zero_if_nan(self.apparent, replace_nan),
            },
            'active': {
                'unit': 'Wh',
                'value': zero_if_nan(self.active, replace_nan),
            },
            'reactive': {
                'unit': 'VARh',
                'value': zero_if_nan(self.reactive, replace_nan),
            },
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

    def __div__(self, t):
        ''' Divides Tariff with timedelta or seconds, to allow easy calculation of average import and export Powers. '''
        if not isinstance(t, timedelta) and not isinstance(t, Number):
            raise TypeError('division allowed only by timedelta or number')
        if isinstance(t, timedelta):
            t = t.total_seconds()

        return [self.energy_import / t, self.energy_export / t]

    def __truediv__(self, t):
        ''' Divides Energy with timedelta or seconds, to allow easy calculation of average Power. '''
        return self.__div__(t)

    @property
    def balance(self):
        return self.energy_import - self.energy_export

    def as_dict(self, replace_nan=False):
        return {
            'import': self.energy_import.as_dict(replace_nan=replace_nan),
            'export': self.energy_export.as_dict(replace_nan=replace_nan),
        }


class Phase(object):
    def __init__(self, voltage=float('nan'), current=float('nan'), apparent=float('nan'), active=float('nan')):
        self.voltage = voltage
        self.current = current

        # If both apparent and active powers are NaN, calculate Power according to voltage and current
        # Not really exact, but at least gives apparent power...
        if isnan(apparent) and isnan(active):
            self.power = Power(self.voltage * current, float('nan'))
        else:
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
        return {
            'power': self.power.as_dict(replace_nan=replace_nan),
            'voltage': {
                'unit': 'V',
                'value': zero_if_nan(self.voltage, replace_nan),
            },
            'current': {
                'unit': 'A',
                'value': zero_if_nan(self.current, replace_nan),
            },
        }
