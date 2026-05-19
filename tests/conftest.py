import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--device-address",
        "--device-addr",
        action="store",
        default=None,
        help="Device address as 'port:addr' e.g. '/dev/ttyUSB1:1' or 'port' e.g. '/dev/ttyUSB1' for hardware integration tests",
    )


@pytest.fixture
def device_address(request):
    addr = request.config.getoption("--device-address")
    if addr is None:
        pytest.skip("--device-address not provided")
    try:
        port, modbus_addr = addr.rsplit(":", 1)
    except ValueError:
        port = addr
        addr = 1
    return port, int(modbus_addr)
