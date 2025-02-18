import sys
from pygmygs import PygmyGS, RadioConfig

__author__ = "Matteo Golin"

def main() -> None:

    if len(sys.argv) < 2:
        raise ValueError("Please provide the serial port of the RN2903 (i.e. /dev/ttyUSB0, COM2, etc.)")

    gs = PygmyGS(sys.argv[1])

    config = RadioConfig(
        mod = "lora",
    )

    if not gs.configure(config):
        print("Couldn't configure radio.")

    while True:
        data = gs.receive()
        if data is not None:
            print(f"Call sign: {data[0]}")
            print(f"Seq number: {data[1]}")
            print(f"Data: {data[2].decode('ascii')}")

if __name__ == "__main__":
    main()
