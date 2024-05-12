import time
import sys
sys.path.append('../')
from MilightController import MilightController, Commands

if __name__ == "__main__":
    controller = MilightController({"type": "all"})
    devices = controller.discover()
    
    if devices:
        for device in devices:
            controller.send_command(device, Commands.wifi_bridge_lamp_on())
            time.sleep(1)
            controller.send_command(device, Commands.wifi_bridge_brightness(0))
            time.sleep(1)
            controller.send_command(device, Commands.wifi_bridge_brightness(100))
            time.sleep(1)
            controller.send_command(device, Commands.wifi_bridge_set_color("#af00ff"))
            time.sleep(1)
            controller.send_command(device, Commands.wifi_bridge_set_color("17 70 13"))
            time.sleep(1)
            controller.send_command(device, Commands.wifi_bridge_mode_number(1))
            time.sleep(1)
            controller.send_command(device, Commands.wifi_bridge_mode_number(2))
            time.sleep(1)
            controller.send_command(device, Commands.wifi_bridge_mode_number(3))
            time.sleep(1)
            controller.send_command(device, Commands.wifi_bridge_mode_number(4))
            time.sleep(1)
            controller.send_command(device, Commands.wifi_bridge_mode_number(5))
            time.sleep(1)
            controller.send_command(device, Commands.wifi_bridge_mode_speed_increase())
            time.sleep(1)
            controller.send_command(device, Commands.wifi_bridge_mode_speed_decrease())
            time.sleep(1)
            controller.send_command(device, Commands.wifi_bridge_lamp_off())