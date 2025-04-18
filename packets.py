import struct
from enum import IntEnum
from typing import Protocol, Self
from dataclasses import dataclass


class BlockType(IntEnum):
    """Possible packet block types"""

    PRESS = 0x0
    TEMP = 0x1
    ALT = 0x2
    COORDS = 0x3
    ACCEL = 0x4
    GYRO = 0x5
    MAG = 0x6
    VOLT = 0x7


class Block(Protocol):
    """Represents a block of a packet, containing data about rocket flight."""

    time: int  # Mission time in milliseconds

    def size(self) -> int:
        """Returns the total size of the block in bytes."""
        ...


@dataclass
class PressureBlock:
    """
    Represents a pressure block containing pressure data.
    """

    time: int
    pressure: float  # Pressure in Pascals

    @classmethod
    def from_bytes(cls, data: bytes) -> Self:
        """Constructs a pressure data block from bytes."""

        time, pressure = struct.unpack("<Ii", data[:8])

        return cls(
            time=time,
            pressure=pressure,
        )

    def size(self) -> int:
        return 8


@dataclass
class TemperatureBlock:
    """
    Represents a temperature block containing temperature data.
    """

    time: int
    temperature: float  # Temperature in degrees Celsius

    @classmethod
    def from_bytes(cls, data: bytes) -> Self:
        """Constructs a temperature data block from bytes."""

        time, temperature = struct.unpack("<Ii", data[:8])

        return cls(
            time=time,
            temperature=temperature / 1000,
        )

    def size(self) -> int:
        return 8


@dataclass
class AltitudeBlock:
    """
    Represents an altitude block containing altitude data.
    """

    time: int
    altitude: float  # Altitude above sea level in m

    @classmethod
    def from_bytes(cls, data: bytes) -> Self:
        """Constructs an altitude data block from bytes."""

        time, altitude = struct.unpack("<Ii", data[:8])

        return cls(
            time=time,
            altitude=altitude / 100,
        )

    def size(self) -> int:
        return 8


@dataclass
class AccelerationBlock:
    """
    Represents an acceleration block containing linear acceleration data.
    """

    time: int
    x: float  # Acceleration in X in m/s^2
    y: float  # Acceleration in Y in m/s^2
    z: float  # Acceleration in Z in m/s^2

    @classmethod
    def from_bytes(cls, data: bytes) -> Self:
        """Constructs an acceleration data block from bytes."""

        time, x, y, z = struct.unpack("<Ihhh", data[:10])

        return cls(
            time=time,
            x=x / 100,
            y=y / 100,
            z=z / 100,
        )

    def size(self) -> int:
        return 10


@dataclass
class GyroBlock:
    """
    Represents a gyroscope block containing angular velocity data.
    """

    time: int
    x: float  # Angular velocity in X in dps
    y: float  # Angular velocity in Y in dps
    z: float  # Angular velocity in Z in dps

    @classmethod
    def from_bytes(cls, data: bytes) -> Self:
        """Constructs a gyroscope data block from bytes."""

        time, x, y, z = struct.unpack("<Ihhh", data[:10])

        return cls(
            time=time,
            x=x / 10,
            y=y / 10,
            z=z / 10,
        )

    def size(self) -> int:
        return 10


@dataclass
class MagBlock:
    """
    Represents a magnetometer block containing magnetic field data.
    """

    time: int
    x: float  # Magnetic field in X in micro Teslas
    y: float  # Magnetic field in Y in micro Teslas
    z: float  # Magnetic field in Z in micro Teslas

    @classmethod
    def from_bytes(cls, data: bytes) -> Self:
        """Constructs a magnetometer data block from bytes."""

        time, x, y, z = struct.unpack("<Ihhh", data[:10])

        return cls(
            time=time,
            x=x / 10,
            y=y / 10,
            z=z / 10,
        )

    def size(self) -> int:
        return 10


@dataclass
class BatteryBlock:
    """
    Represents a battery voltage block containing battery voltage data.
    """

    time: int
    voltage: float  # Battery voltage in volts

    @classmethod
    def from_bytes(cls, data: bytes) -> Self:
        """Constructs a battery voltage data block from bytes."""

        time, voltage = struct.unpack("<IH", data[:6])

        return cls(time=time, voltage=voltage / 1000)

    def size(self) -> int:
        return 6


class PacketParser:
    """Parses a packet into its blocks. Intended to be iterated over."""

    def __init__(self, packet: bytes) -> None:
        self._packet: bytes = packet

    def __iter__(self):
        return self

    def __next__(self):

        # Stop when there's no more data left
        if len(self._packet) == 0:
            raise StopIteration

        # Get block type
        block_type, remaining = packet_get_type(self._packet)
        self._packet = remaining

        match block_type:
            case BlockType.PRESS:
                block = PressureBlock.from_bytes(self._packet)
            case BlockType.TEMP:
                block = TemperatureBlock.from_bytes(self._packet)
            case BlockType.ALT:
                block = AltitudeBlock.from_bytes(self._packet)
            case BlockType.ACCEL:
                block = AccelerationBlock.from_bytes(self._packet)
            case BlockType.GYRO:
                block = GyroBlock.from_bytes(self._packet)
            case BlockType.MAG:
                block = MagBlock.from_bytes(self._packet)
            case BlockType.VOLT:
                block = BatteryBlock.from_bytes(self._packet)
            case _:
                raise ValueError("Block type not implemented")

        # Remove bytes just parsed
        self._packet = self._packet[block.size() :]
        return block


def packet_get_type(packet: bytes) -> tuple[int, bytes]:
    """Parse the next block type in the packet."""

    block_type: int = struct.unpack("<B", packet[:1])[0]
    remaining: bytes = packet[1:]
    return BlockType(block_type), remaining
