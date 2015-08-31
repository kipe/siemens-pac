from __future__ import unicode_literals, print_function, division
from struct import pack, unpack
from modbus_tk.defines import READ_INPUT_REGISTERS, WRITE_MULTIPLE_REGISTERS

from siemens.electricity import Power, Phase, Energy, Tariff, zero_if_nan


class PAC(object):
    _master = None
    _unit = None

    def __init__(self):
        self.power = Power()
        self.L1 = Phase()
        self.L2 = Phase()
        self.L3 = Phase()
        self.tariff_1 = Tariff()
        self.tariff_2 = Tariff()
        self.frequency = float('nan')

    def _from_float(self, values):
        return [unpack(str('>f'), pack(str('>HH'), *values[i:i + 2]))[0] for i in range(0, len(values), 2)]

    def _from_double(self, values):
        return [unpack(str('>d'), pack(str('>HHHH'), *values[i:i + 4]))[0] for i in range(0, len(values), 4)]

    def read_input_register(self, register_start, count=1):
        if self._master is None or self._unit is None:
            raise ValueError('Connection uninitialized.')

        result = self._master.execute(self._unit, READ_INPUT_REGISTERS, register_start, count)

        if not result:
            raise IOError('Register read failed.')

        return result

    def read_power(self):
        self.power = Power(*self._from_float(self.read_input_register(63, 4)))

    def read_phases(self):
        values = self._from_float(self.read_input_register(1, 30))

        # Note: PAC reports phase powers as NaN, if all phases aren't connected.
        #       However, the total power read with PAC.read_power() is seems valid even then.
        self.L1 = Phase(values[0], values[6], values[9], values[12])
        self.L2 = Phase(values[1], values[7], values[10], values[13])
        self.L3 = Phase(values[2], values[8], values[11], values[14])

    def read_frequency(self):
        self.frequency = self._from_float(self.read_input_register(55, 2))[0]

    def read_energy(self):
        values = self._from_double(self.read_input_register(801, 40))
        self.tariff_1 = Tariff(
            Energy(values[8], values[0], values[4]),
            Energy(values[8], values[2], values[6])
        )
        self.tariff_2 = Tariff(
            Energy(values[9], values[1], values[5]),
            Energy(values[9], values[3], values[7])
        )

    def read(self):
        self.read_power()
        self.read_phases()
        self.read_frequency()
        self.read_energy()

    def clear_tariff(self, tariff):
        if self._master is None or self._unit is None:
            raise ValueError('Connection uninitialized.')

        if tariff == 1:
            start = 801
        if tariff == 2:
            start = 805
        registers = range(start, start + 5 * 8, 8)
        for x in registers:
            self._master.execute(self._unit, WRITE_MULTIPLE_REGISTERS, x, output_value=[0, 0, 0, 0])
        # Read energy to update values...
        self.read_energy()
        
    def close(self):
        if self._master is None or self._unit is None:
            return
        self._master.close()

    @property
    def energy(self):
        return self.tariff_1 + self.tariff_2

    @property
    def energy_balance(self):
        return self.tariff_1.energy_import + self.tariff_2.energy_import - self.tariff_1.energy_export - self.tariff_2.energy_export

    def as_dict(self, replace_nan=False):
        return {
            'power': self.power.as_dict(replace_nan=replace_nan),
            'phases': {
                'L1': self.L1.as_dict(replace_nan=replace_nan),
                'L2': self.L2.as_dict(replace_nan=replace_nan),
                'L3': self.L3.as_dict(replace_nan=replace_nan),
            },
            'energy': self.energy.as_dict(replace_nan=replace_nan),
            'balance': self.energy_balance.as_dict(replace_nan=replace_nan),
            'tariffs': [
                self.tariff_1.as_dict(replace_nan=replace_nan),
                self.tariff_2.as_dict(replace_nan=replace_nan),
            ],
            'frequency': zero_if_nan(self.frequency, replace_nan),
        }


class PAC3100(PAC):
    '''
    Class for connecting to PAC3100 through Modbus RTU.
    Note: Untested.
    '''
    def __init__(self, port, baudrate=4800, unit=1, parity='N', stopbits=1):
        import serial
        import modbus_tk.modbus_rtu as modbus_rtu
        self._unit = unit
        self._master = modbus_rtu.RtuMaster(
            serial.Serial(port=port, baudrate=baudrate, bytesize=8, parity=parity, stopbits=stopbits)
        )

        super(PAC3100, self).__init__()


class PACx200(PAC):
    '''
    Class for connecting to PAC3200 and PAC4200 through Modbus TCP/IP.
    '''
    def __init__(self, host, port=502):
        import modbus_tk.modbus_tcp as modbus_tcp

        self._unit = 1
        self._master = modbus_tcp.TcpMaster(host, port)

        super(PACx200, self).__init__()


class PAC3200(PACx200):
    pass


class PAC4200(PACx200):
    pass
