import struct
from enum import IntEnum
from typing import Protocol, Self, Iterable
from dataclasses import dataclass


class BlockType(IntEnum):
    """Possible packet block types"""

    PRESS = 0x0
    TEMP = 0x1
    ALT = 0x2
    COORDS = 0x3


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
    pressure: int  # Pressure in Pascals

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
    temperature: int  # Temperature in millidegrees Celsius

    @classmethod
    def from_bytes(cls, data: bytes) -> Self:
        """Constructs a temperature data block from bytes."""

        time, temperature = struct.unpack("<Ii", data[:8])

        return cls(
            time=time,
            temperature=temperature,
        )

    def size(self) -> int:
        return 8


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
            case _:
                raise ValueError("Block type not implemented")

        # Remove bytes just parsed
        self._packet = self._packet[block.size() :]
        print(len(self._packet))
        return block


def packet_get_type(packet: bytes) -> tuple[int, bytes]:
    """Parse the next block type in the packet."""

    block_type: int = struct.unpack("<B", packet[:1])[0]
    remaining: bytes = packet[1:]
    return BlockType(block_type), remaining
