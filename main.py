import sys
from rn2903 import RN2903

__author__ = "Matteo Golin"

def main() -> None:

    if len(sys.argv) < 2:
        raise ValueError("Please provide the serial port of the RN2903 (i.e. /dev/ttyUSB0, COM2, etc.)")

    gs = RN2903(sys.argv[1])
    print(gs.snr())
    print(gs.version())

if __name__ == "__main__":
    main()
