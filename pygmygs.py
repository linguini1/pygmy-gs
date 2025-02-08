from rn2903 import RN2903
from typing import Self, Optional

__author__ = "Matteo Golin"

class PygmyGS:

    def __init__(self, serial_port: str) -> None:
        """
        Constructs a new instance of the PygmyGS.
        `serial_port`: The string representing the serial port of the PygmyGS (i.e. /dev/ttyUSB0)
        """

        self.radio = RN2903(serial_port=serial_port)

    def receive(self) -> Optional[bytes]:

        """
        Puts the ground station in continuous receive mode until data is received, at which point the data is
        returned in binary format.
        If entering receive mode fails or times out, None is returned.
        """

        return self.radio.receive()

    def transmit(self, data: bytes) -> bool:
        """
        Transmit data over the radio.
        Returns false on failure, true otherwise.
        """

        return self.radio.transmit(data)
