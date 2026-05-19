import logging
import time

import minimalmodbus

log = logging.getLogger(__name__)


def _int_to_temp(val):
    """
    Interpret integer with implied decimal points as decimal
    """
    return val / 10


def _temp_to_int(val):
    """
    inverse _int_to_temp
    """
    return int(round(val * 10))


class WatlowF4:
    REG_TEMP_MEAS = 100
    REG_TEMP_SETPOINT = 300

    def __init__(self, port, addr=1, temp_limit=(-42, 130), **kwargs):
        """Initialize an instance of the Watlow F4 Temperature Controller

        Parameters
        ----------
        port : str
            e.g. "/dev/ttyUSB1"
        addr : int
            modbus address. Defaults to 1 (in this function and on F4
            controllers)
        temp_limit : tuple of int or float
            Tuple containing lower and upper temperature limit. This
            is used only as a validator in the temperature_setpoint
            setter. Defaults to (-42, 130), the temperature limits of
            a TestEquity Model 107 Chamber

        Returns
        -------
        WatlowF4 Object


        """
        self.instrument = minimalmodbus.Instrument(port, addr, **kwargs)
        self.instrument.serial.baudrate = 9600
        self.instrument.serial.timeout = 0.5
        self.temp_limit = temp_limit
        log.info(
            f"Successfuly initialized WatlowF4 Temperature controller at {port}:{addr}"
        )

    def _read_reg(self, reg):
        return self.instrument.read_register(reg, 0, signed=True)

    def _write_reg(self, reg, value):
        return self.instrument.write_register(reg, value, 0, signed=True)

    @property
    def temperature(self):
        """Get the current temperature reading (read only)

        Returns
        -------
        float
            Temperature in degrees Celsius

        """
        val = _int_to_temp(self._read_reg(self.REG_TEMP_MEAS))
        log.debug(f"Read temperature: {val} °C")
        return val

    @property
    def temperature_setpoint(self):
        """Control the static temperature setpoint for the controller

        Returns
        -------
        int
            Temperature setpoint in degrees Celsius

        """
        val = _int_to_temp(self._read_reg(self.REG_TEMP_SETPOINT))
        log.debug(f"Read temperature set point: {val} °C")
        return val

    @temperature_setpoint.setter
    def temperature_setpoint(self, value, validate=True):
        if value < self.temp_limit[0]:
            raise ValueError(
                f"Can't set temperature to {value:.1f} °C, min. is {self.temp_limit[0]} °C"
            )
        if value > self.temp_limit[1]:
            raise ValueError(
                f"Can't set temperature to {value:.1f} °C, max. is {self.temp_limit[1]} °C"
            )
        self._write_reg(self.REG_TEMP_SETPOINT, _temp_to_int(value))
        if validate:
            time.sleep(0.1)
            readback = self.temperature_setpoint
            if readback != value:
                raise ValueError("Write to temperature_setpoint failed. Wrote {}")
        log.info(f"Set Temperature set point to {value} °C")
