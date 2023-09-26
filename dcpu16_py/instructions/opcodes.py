from ctypes import c_ubyte, c_bool, c_uint16
import numpy as np

from dcpu16_py.enums.opcode_modes import OpcodeMode

__B0__ = c_ubyte(1)
__B1__ = c_ubyte(2)
__B2__ = c_ubyte(4)
__B3__ = c_ubyte(8)
__B4__ = c_ubyte(16)
__B5__ = c_ubyte(32)
__B6__ = c_ubyte(64)
__B7__ = c_ubyte(128)

def _assert_b0(byte: c_ubyte) -> c_bool:
    return c_bool(np.bitwise_and(byte, __B0__) > 0)

def _assert_b1(byte: c_ubyte) -> c_bool:
    return c_bool(np.bitwise_and(byte, __B1__) > 0)

def _assert_b2(byte: c_ubyte) -> c_bool:
    return c_bool(np.bitwise_and(byte, __B2__) > 0)

def _assert_b3(byte: c_ubyte) -> c_bool:
    return c_bool(np.bitwise_and(byte, __B3__) > 0)

def _assert_b4(byte: c_ubyte) -> c_bool:
    return c_bool(np.bitwise_and(byte, __B4__) > 0)

def _assert_b5(byte: c_ubyte) -> c_bool:
    return c_bool(np.bitwise_and(byte, __B5__) > 0)

def _assert_b6(byte: c_ubyte) -> c_bool:
    return c_bool(np.bitwise_and(byte, __B6__) > 0)

def _assert_b7(byte: c_ubyte) -> c_bool:
    return c_bool(np.bitwise_and(byte, __B7__) > 0)

def _invalid_value(opcode: c_ubyte) -> c_bool:
    return c_bool(opcode.value >= __B6__.value)


def evaluate_mode(value: c_ubyte):
    return OpcodeMode(np.bitwise_and(value, c_ubyte(0x18)) >> 3)

def is_literal(value: c_ubyte):
    return _assert_b5(value)