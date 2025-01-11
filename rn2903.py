"""
The PygmyGS is based on the RN2903 radio module. To see its command specifications, please consult the command
reference: https://ww1.microchip.com/downloads/en/DeviceDoc/40001811A.pdf
"""

from serial import Serial
from typing import Self, Optional

__author__ = "Matteo Golin"

BAUD_RATE: int = 57600 # Baud rate of the RN2903
MAX_TIMEOUT: str =  "4294967245"

class RN2903:
    """Represents the RN2903 radio module."""

    def __init__(self, serial_port: str) -> None:

        """
        Constructs a new instance of the RN2903 radio module.
        `serial_port`: The string representing the serial port of the PygmyGS (i.e. /dev/ttyUSB0)
        """

        self.serial: Serial = Serial(
            port=serial_port,
            baudrate=BAUD_RATE,
        )

    def __write(self, data: str) -> None:
        """Write some data (string command) to the radio module."""

        self.serial.write(f"{data}\r\n".encode("utf-8"))
        self.serial.flush()

    def __wait_for_ok(self) -> bool:
        """Returns true if okay, false otherwise."""

        line = self.serial.readline()
        return "ok" in str(line)

    def __mac_pause(self) -> bool:
        """Pauses the radio MAC layer. Returns true if pause and false otherwise."""
        self.__write("mac pause")
        line = self.serial.readline()
        return MAX_TIMEOUT in str(line)

    def receive(self) -> Optional[bytes]:
        """
        Puts the ground station in continuous receive mode until data is received, at which point the data is
        returned in binary format.
        If entering receive mode fails or times out, None is returned.
        """

        if not self.__mac_pause():
            return None

        # Enter infinite receive

        self.__write("radio rx 0")
        if not self.__wait_for_ok():
            return None

        # Have to convert from ASCII hex representation (i.e. 0xDEADBEEF) into actual bytes

        data = self.serial.readline().decode("ascii")[8:].strip()
        return bytes.fromhex(data)

    def snr(self) -> int:
        """
        Gets the SNR from the radio module.
        See the command reference sheet for numerical meanings.
        """

        self.__write("radio get snr")
        return int(self.serial.readline())

    def version(self) -> str:
        """Return the RN2903 version string."""

        self.__write("sys get ver")
        return self.serial.readline().decode("ascii").strip()
