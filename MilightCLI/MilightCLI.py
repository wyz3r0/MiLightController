from argparse import ArgumentParser, Namespace, ArgumentTypeError, FileType
from MilightController import *

def hex_color(color: str) -> str:
    if len(color) == 6:
        return color
    raise ArgumentTypeError("Value must be 6 symbol hex code")

def percentage(percent: int) -> int:
    if percent in range(0, 101):
        return percent
    raise ArgumentTypeError("Value must be between 0 nad 100")

def kelvin(kv: int) -> int:
    if kv in range(2700, 6501):
        return kv
    raise ArgumentTypeError("Value must be between 2700 nad 6500")

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
command.add_argument("-c", "--color", "--colour", help="Set light color in rgb", type=hex_color)
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
        args.saturation or args.temp or args.mode or args.modeup or args.modedown
    ):
        parser.error("When -b/--bridge or -z/--zone is selected, one of the command options must be specified: [-on | -off | -c COLOR | -nl | -br BRIGHTNESS | -s SATURATION | -t TEMP | -m {1,2,3,4,5} | -mu | -md]")

    print(args)

if __name__ == "__main__":
    main()