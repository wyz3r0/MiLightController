import time
from MilightController import MilightController, Commands, Zone

if __name__ == "__main__":
    controller: MilightController = MilightController()
    devices: list[dict[str, str]] = controller.discover()
    
    if devices:
        for device in devices:
            controller.send_command(device, Commands.light_on(), Zone.ZONE_1)
            time.sleep(1)
            controller.send_command(device, Commands.light_on(), Zone.ZONE_2)
            time.sleep(1)
            controller.send_command(device, Commands.light_on(), Zone.ZONE_3)
            time.sleep(1)
            controller.send_command(device, Commands.light_on(), Zone.ZONE_4)
            time.sleep(1)
            controller.send_command(device, Commands.light_off(), Zone.ALL)
            time.sleep(1)
            controller.send_command(device, Commands.light_on())
            time.sleep(1)
            controller.send_command(device, Commands.set_color("#af00ff"))
            time.sleep(1)
            controller.send_command(device, Commands.set_color("17 70 13"))
            time.sleep(1)
            controller.send_command(device, Commands.saturation(20))
            time.sleep(1)
            controller.send_command(device, Commands.saturation(100))
            time.sleep(1)
            controller.send_command(device, Commands.white_light_on())
            time.sleep(1)
            controller.send_command(device, Commands.brightness(20))
            time.sleep(1)
            controller.send_command(device, Commands.brightness(100))
            time.sleep(1)
            controller.send_command(device, Commands.kelvin(2700))
            time.sleep(1)
            controller.send_command(device, Commands.kelvin(6500))
            time.sleep(1)
            controller.send_command(device, Commands.night_light_on())
            time.sleep(1)
            controller.send_command(device, Commands.light_on())
            time.sleep(1)
            controller.send_command(device, Commands.mode_number(1))
            time.sleep(1)
            controller.send_command(device, Commands.mode_number(2))
            time.sleep(1)
            controller.send_command(device, Commands.mode_number(3))
            time.sleep(1)
            controller.send_command(device, Commands.mode_number(4))
            time.sleep(1)
            controller.send_command(device, Commands.mode_number(5))
            time.sleep(1)
            controller.send_command(device, Commands.mode_speed_decrease())
            time.sleep(1)
            controller.send_command(device, Commands.mode_speed_increase())
            time.sleep(1)
            controller.send_command(device, Commands.light_off())