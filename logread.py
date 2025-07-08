import sys
import struct

from typing import Optional
from io import BufferedReader

from packets import PacketParser
from pygmygs import CALLSIGN_LEN

__author__ = "Matteo Golin"


def get_packet(logfile: BufferedReader, callsign: str) -> Optional[bytes]:

    packet = bytearray()
    callsign_index = 0

    while True:

        # One byte at a time
        newdata = logfile.read(1)
        if len(newdata) < 1:
            return None

        b = newdata[0]

        # If we encounter a call sign, that will indicate the end of the packet and the start of the next one
        if b == callsign[callsign_index].encode("ascii")[0]:
            callsign_index += 1
            packet.append(b)
            if callsign_index >= CALLSIGN_LEN:
                break
        else:
            callsign_index = 0
            packet.append(b)

    # Remove trailing call sign
    packet = packet[:-CALLSIGN_LEN]
    return bytes(packet)


def main() -> None:

    if len(sys.argv) < 3:
        raise ValueError("Please provide a file name of the log file to parse, and the call-sign in the log file.")

    with open(sys.argv[1], "rb") as log:

        while True:
            data = get_packet(log, sys.argv[2])

            # Stream over
            if data is None:
                break

            # Packet too short; must be first packet where we just parse call-sign
            if len(data) < CALLSIGN_LEN:
                continue

            count: int = struct.unpack("<B", data[:1])[0]
            data = data[1:]

            print(f"Call sign: {sys.argv[2]}")
            print(f"Seq number: {count}")

            for block in PacketParser(data):
                print(block)


if __name__ == "__main__":
    main()
