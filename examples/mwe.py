from watlow_f4 import WatlowF4

inst = WatlowF4("/dev/tty.usbserial-AB82P7QL")

print(f"Current temperature: {inst.temperature} °C")
print(f"Current temperature setpoint: {inst.temperature_setpoint} °C")

print("Setting temperature setpoint to 25°C...")
inst.temperature_setpoint = 25
print(f"Current temperature setpoint: {inst.temperature_setpoint} °C")

print("Setting temperature setpoint to 30°C...")
inst.temperature_setpoint = 30
print(f"Current temperature setpoint: {inst.temperature_setpoint} °C")
