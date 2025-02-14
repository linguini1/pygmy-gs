from rn2903 import RN2903, RadioConfig
from typing import Self, Optional
import struct

__author__ = "Matteo Golin"

CALLSIGN_LEN: int = 6

class PygmyGS:

    def __init__(self, serial_port: str) -> None:
        """
        Constructs a new instance of the PygmyGS.
        `serial_port`: The string representing the serial port of the PygmyGS (i.e. /dev/ttyUSB0)
        """

        self.radio = RN2903(serial_port=serial_port)

    def receive(self) -> Optional[tuple[str, int, bytes]]:

        """
        Puts the ground station in continuous receive mode until data is received, at which point the data is
        returned in binary format.
        If entering receive mode fails or times out, None is returned.
        """

        data = self.radio.receive()
        if data is None:
            return None

        callsign = data[0:CALLSIGN_LEN].decode('ascii')
        count: int = struct.unpack("B", data[CALLSIGN_LEN:CALLSIGN_LEN + 1])[0]
        return (callsign, count,data[CALLSIGN_LEN + 1:])

    def transmit(self, data: bytes) -> bool:
        """
        Transmit data over the radio.
        Returns false on failure, true otherwise.
        """

        return self.radio.transmit(data)

    def configure(self, config: RadioConfig) -> bool:
        """Configure the ground station radio."""
        return self.radio.configure(config)
