# Watlow F4 
This is an extremely minimal package that provides python bindings to
static temperature set / read modbus registers for the Watlow f4 controller.

## Tests

Non-HW tests:
```bash
uv run pytest
```

To test HW:
```bash
uv run pytest  --device-address "/dev/tty.usbserial-AB82P7QL:1"
```

You can discover the `dev/tty*` address relevant to you using e.g.:
```bash
watch "ls /dev/tty* | column"
```
and unplugging/plugging in the USB cable associated with your RS232-to-serial converter.
