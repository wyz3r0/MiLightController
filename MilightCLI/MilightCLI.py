from argparse import ArgumentParser, Namespace, ArgumentTypeError, FileType
from MilightController import *

def hex_color(color: str) -> str:
    if len(color) == 6:
        return color
    raise ArgumentTypeError("Value must be 6 symbol hex code")

def percentage(percent: str) -> int:
    percent = int(percent)
    if 0 <= percent <= 100:
        return percent
    raise ArgumentTypeError("Value must be between 0 nad 100")

def kelvin(kv: str) -> int:
    kv = int(kv)
    if 2700 <= kv <= 6500:
        return kv
    raise ArgumentTypeError("Value must be between 2700 nad 6500")

def log(info: str) -> None:
    if args.verbose:
        print(info)

parser = ArgumentParser()

target = parser.add_mutually_exclusive_group(required=True)
target.add_argument("-b", "--bridge", help="Selects wifi-bridge as a target", action="store_true")
target.add_argument("-z", "--zone", help="Selects zone as a target", type=int, choices=[1, 2, 3, 4])
#! check
target.add_argument("-l", "--link", help="Link zone", type=int, choices=[1, 2, 3, 4])
target.add_argument("-ul", "--unlink", help="Unlink zone", type=int, choices=[1, 2, 3, 4])
target.add_argument("-p", "--preset", help="Load preset from a file", type=FileType('r'))

command = parser.add_mutually_exclusive_group()
command.add_argument("-on", help="Turn selected target on", action="store_true")
command.add_argument("-off", help="Turn selected target off", action="store_true")
command.add_argument("-c", "--color", "--colour", help="Set light color to rgb", type=hex_color)
command.add_argument("-nl", "--nightlight", help="Sets mode to night light", action="store_true")
command.add_argument("-br", "--brightness", help="Set brightness", type=percentage)
command.add_argument("-s", "--saturation", help="Set saturation", type=percentage)
command.add_argument("-t", "--temperature", "--temp", "-kv", "--kelvin", help="Set color to white with temperature", type=kelvin)
command.add_argument("-m", "--mode", help="Set mode", type=int, choices=[1, 2, 3, 4, 5])
command.add_argument("-mu", "--modeup", help="Speed up animation speed", action="store_true")
command.add_argument("-md", "--modedown", help="Slow down animation speed", action="store_true")

parser.add_argument("-v", "--verbose", help="Makes the output verbose", action="store_true")

args: Namespace = parser.parse_args()


def main() -> None:
    # make sure command is passed when --bridge or --zone selected
    if (args.bridge or args.zone) and not (
        args.on or args.off or args.color or args.nightlight or args.brightness or
        args.saturation or args.temperature or args.mode or args.modeup or args.modedown
    ):
        parser.error("When -b/--bridge or -z/--zone is selected, one of the command options must be specified: [-on | -off | -c COLOR | -nl | -br BRIGHTNESS | -s SATURATION | -t TEMP | -m {1,2,3,4,5} | -mu | -md]")

    if (args.bridge) and (
        args.nightlight or args.saturation or args.temperature
    ):
        parser.error("When -b/--bridge is selected, cannot select [-nl | -s SATURATION | -t TEMP]")
    
    # connect to wifi-bridge
    controller: MilightController = MilightController()
    devices = controller.discover()
    # ! currently using first device
    
    
    # handle bridge commands
    if args.bridge:
        log("Targeting bridge")
        if args.on:
            controller.send_command(devices[0], Commands.wifi_bridge_lamp_on())
        elif args.off:
            controller.send_command(devices[0], Commands.wifi_bridge_lamp_off())
        elif args.color:
            controller.send_command(devices[0], Commands.wifi_bridge_set_color(args.color))
        elif args.nightlight: #! not possible
            controller.send_command(devices[0], )
        elif args.brightness:
            controller.send_command(devices[0], Commands.wifi_bridge_brightness(args.brightness))
        elif args.saturation: #! not possible
            controller.send_command(devices[0], )
        elif args.temperature: #! not possible
            controller.send_command(devices[0], )
        elif args.mode:
            controller.send_command(devices[0], Commands.wifi_bridge_mode_number(args.mode))
        elif args.modeup:
            controller.send_command(devices[0], Commands.wifi_bridge_mode_speed_increase())
        elif args.modedown:
            controller.send_command(devices[0], Commands.wifi_bridge_mode_speed_decrease())

    # handle zone commands
    if args.zone:
        log(f"Targeting zone {args.zone}")
        if args.on:
            controller.send_command(devices[0], Commands.light_on())
        elif args.off:
            controller.send_command(devices[0], Commands.light_off())
        elif args.color:
            controller.send_command(devices[0], Commands.set_color(args.color))
        elif args.nightlight:
            controller.send_command(devices[0], Commands.night_light_on())
        elif args.brightness:
            controller.send_command(devices[0], Commands.brightness(args.brightness))
        elif args.saturation:
            controller.send_command(devices[0], Commands.saturation(args.saturation))
        elif args.temperature:
            controller.send_command(devices[0], Commands.kelvin(args.temperature))
        elif args.mode:
            controller.send_command(devices[0], Commands.mode_number(args.mode))
        elif args.modeup:
            controller.send_command(devices[0], Commands.mode_speed_increase())
        elif args.modedown:
            controller.send_command(devices[0], Commands.mode_speed_decrease())

    # handle link/unlink commands
    if args.link:
        log(f"Linking zone {args.link}")
        controller.send_command(devices[0], )
    elif args.unlink:
        log(f"Unlinking zone {args.unlink}")
        controller.send_command(devices[0], )

    # handle preset command
    if args.preset:
        log(f"Loading preset from file {args.preset.name}")
        controller.send_command(devices[0], )
    
    # print(args)

if __name__ == "__main__":
    main()