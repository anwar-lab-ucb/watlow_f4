import pytest

from watlow_f4.watlow_f4 import WatlowF4, _int_to_temp, _temp_to_int


# ---------------------------------------------------------------------------
# Helper function tests
# ---------------------------------------------------------------------------


class TestIntToTemp:
    def test_positive(self):
        assert _int_to_temp(250) == 25.0

    def test_negative(self):
        assert _int_to_temp(-420) == -42.0

    def test_zero(self):
        assert _int_to_temp(0) == 0.0

    def test_fractional_result(self):
        assert _int_to_temp(255) == 25.5

    def test_roundtrip(self):
        for val in [-420, -100, 0, 1, 100, 255, 1300]:
            assert _temp_to_int(_int_to_temp(val)) == val


class TestTempToInt:
    def test_positive(self):
        assert _temp_to_int(25.0) == 250

    def test_negative(self):
        assert _temp_to_int(-42.0) == -420

    def test_zero(self):
        assert _temp_to_int(0.0) == 0

    def test_rounds_correctly(self):
        assert _temp_to_int(25.5) == 255
        assert _temp_to_int(-10.3) == -103

    def test_integer_input(self):
        assert _temp_to_int(25) == 250


# ---------------------------------------------------------------------------
# Hardware integration tests (only run when --device-address is provided)
# ---------------------------------------------------------------------------


class TestHardwareIntegration:
    """These tests require a real Watlow F4 connected via serial.

    Run with: pytest --device-address /dev/ttyUSB1:1
    """

    @pytest.fixture
    def hw_controller(self, device_address):
        port, addr = device_address
        return WatlowF4(port, addr)

    def test_read_temperature(self, hw_controller):
        temp = hw_controller.temperature
        assert isinstance(temp, (int, float))
        assert -50 < temp < 300

    def test_read_setpoint(self, hw_controller):
        sp = hw_controller.temperature_setpoint
        assert isinstance(sp, (int, float))
        assert -50 < sp < 300

    @pytest.mark.parametrize(
        "val",
        [25, 25.1, 0, -1, -20, 100, 100.1, 105],
    )
    def test_set_and_read_setpoint(self, hw_controller, val):
        original = hw_controller.temperature_setpoint
        try:
            hw_controller.temperature_setpoint = val
            assert hw_controller.temperature_setpoint == val
        finally:
            hw_controller.temperature_setpoint = original
