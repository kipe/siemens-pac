# Siemens SENTRON PAC
[![Build Status](https://travis-ci.org/kipe/siemens-pac.svg?branch=master)](https://travis-ci.org/kipe/siemens-pac)

A Python library for reading [Siemens SENTRON PAC -series](http://w3.siemens.com/powerdistribution/global/en/lv/product-portfolio/sentron/measuring-devices-energy-monitoring/measuring-devices/7kt-pac3200-measuring-devices/pages/7km-pac3200-measuring-devices.aspx) measuring devices.


## Installation
```
pip install git+https://github.com/kipe/siemens-pac.git
```

## Usage
To read PACx200 -devices through Modbus TCP/IP:
```python
from siemens.pac import PACx200
p = PACx200('192.168.0.80')
p.read()  # Reads all values from PAC
# Print whole PAC as dictionary, with NaN values replaced with 0 (useful for JSON dumping).
print(p.as_dict(replace_nan=True))
```

## Issues
- PAC3100 is supported only in theory, as I haven't got a device to test on. Might or might not work.
- According to tests done on PAC3200, if only one (might be also only two?) phase is connected, phase specific powers are reported as NaN.

> However, total power, accessible via `PACx200.power`, is reported correctly.
> In this case, Phase.voltage and Phase.current are used to calculate Power.apparent.
> Power.active and Power.reactive are left as NaN, to indicate invalid input.
