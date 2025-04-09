import sys
from packets import PacketParser
from pygmygs import PygmyGS, RadioConfig

__author__ = "Matteo Golin"


def main() -> None:

    if len(sys.argv) < 2:
        raise ValueError("Please provide the serial port of the RN2903 (i.e. /dev/ttyUSB0, COM2, etc.)")

    gs = PygmyGS(sys.argv[1])

    config = RadioConfig(
        mod="lora",
        frequency=902000000,
        spread=7,
        prlen=6,
        bandwidth=125,
    )

    if not gs.configure(config):
        print("Couldn't configure radio.")

    while True:

        data = gs.receive()

        if data is None:
            continue

        # We received a packet, parse it
        call_sign, seq, packet = data
        print(f"Call sign: {call_sign}")
        print(f"Seq number: {seq}")

        for block in PacketParser(packet):
            print(block)


if __name__ == "__main__":
    main()
