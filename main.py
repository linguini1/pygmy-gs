import sys
from pygmygs import PygmyGS

__author__ = "Matteo Golin"

def main() -> None:

    if len(sys.argv) < 2:
        raise ValueError("Please provide the serial port of the RN2903 (i.e. /dev/ttyUSB0, COM2, etc.)")

    gs = PygmyGS(sys.argv[1])
    print(gs.receive())

if __name__ == "__main__":
    main()
