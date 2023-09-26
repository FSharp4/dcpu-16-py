from ctypes import c_uint16

import numpy as np

NULL_VALUE = c_uint16(0)
OVERFLOW = c_uint16(1)
UNDERFLOW = c_uint16(0xFFFF)

class ALU:
    def __init__():
        pass
    
        # -- Basic Instructions -- 
    def do_basic_instruction(self, instcode: int, a: c_uint16, b: c_uint16) -> (c_uint16, c_uint16, bool):
        basic_instruction_lut = [
            self.nonbasic, #0x0
            self.set,      #0x1
            self.add,      #0x2
            self.sub,      #0x3
            self.mul,      #0x4
            self.div,      #0x5
            self.mod,      #0x6
            self.shl,      #0x7
            self.shr,      #0x8
            self._and,     #0x9
            self.bor,      #0xA
            self.xor,      #0xB
            self.ife,      #0xC
            self.ifn,      #0xD
            self.ifg,      #0xE
            self.ifb       #0xF
        ]
        
        x, y, z = basic_instruction_lut[instcode](a, b)
        return x, y, z
        
    
    def nonbasic(self, a: c_uint16, b: c_uint16) -> (c_uint16, c_uint16, bool):
        raise RuntimeError("Undefined opcode (at basic instruction)") # not supposed to run this!
        
    def set(self, a: c_uint16, b: c_uint16) -> (c_uint16, c_uint16, bool):
        return b, NULL_VALUE, False

    def add(self, a: c_uint16, b: c_uint16) -> (c_uint16, c_uint16, bool):
        raw = a.value + b.value
        over = NULL_VALUE
        flag = False
        if raw > c_uint16(-1).value:
            over = OVERFLOW
            flag = True
        
        return c_uint16(raw), c_uint16(over), flag

    def sub(self, a: c_uint16, b: c_uint16) -> (c_uint16, c_uint16, bool):
        raw = a.value - b.value
        under = NULL_VALUE
        flag = False
        if raw < 0:
            under = UNDERFLOW
            flag = True
        
        return c_uint16(raw), c_uint16(under), flag

    def mul(self, a: c_uint16, b: c_uint16) -> (c_uint16, c_uint16, bool):
        raw = a.value * b.value
        over = np.bitwise_and(np.right_shift(raw, 16), 0xFFFF)
        return c_uint16(raw), c_uint16(over), True

    def div(self, a: c_uint16, b: c_uint16) -> (c_uint16, c_uint16, bool):
        if b.value == 0:
            return NULL_VALUE, NULL_VALUE, True
        raw = a.value // b.value
        compress = np.bitwise_and(np.left_shift(a.value, 16) / b.value, 0xFFFF)
        return c_uint16(raw), c_uint16(compress), True

    def mod(self, a: c_uint16, b: c_uint16) -> (c_uint16, c_uint16, bool):
        if b = 0:
            return NULL_VALUE, NULL_VALUE, False
        raw = a.value % b.value
        return c_uint16(raw), NULL_VALUE, False

    def shl(self, a: c_uint16, b: c_uint16) -> (c_uint16, c_uint16, bool):
        raw = np.left_shift(a.value, b.value)
        carry = np.bitwise_and(np.right_shift(raw, 16), 0xFFFF)
        return c_uint16(raw), c_uint16(carry), True

    def shr(self, a: c_uint16, b: c_uint16) -> (c_uint16, c_uint16, bool):
        raw = np.right_shift(a.value, b.value)
        carry = np.bitwise_and(np.right_shift(np.left_shift(a.value, 16), b.value), 0xFFFF)
        return c_uint16(raw), c_uint16(carry), True

    def _and(self, a: c_uint16, b: c_uint16) -> (c_uint16, c_uint16, bool):
        return c_uint16(np.bitwise_and(a.value, b.value)), NULL_VALUE, False

    def bor(self, a: c_uint16, b: c_uint16) -> (c_uint16, c_uint16, bool):
        return c_uint16(np.bitwise_or(a.value, b.value)), NULL_VALUE, False

    def xor(self, a: c_uint16, b: c_uint16) -> (c_uint16, c_uint16, bool):
        return c_uint16(np.bitwise_xor(a.value, b.value)), NULL_VALUE, False

    def ife(self, a: c_uint16, b: c_uint16) -> (c_uint16, c_uint16, bool):
        return c_uint16(a.value == b.value), NULL_VALUE, False

    def ifn(self, a: c_uint16, b: c_uint16) -> (c_uint16, c_uint16, bool):
        return c_uint16(a.value != b.value), NULL_VALUE, False

    def ifg(self, a: c_uint16, b: c_uint16) -> (c_uint16, c_uint16, bool):
        return c_uint16(a.value > b.value), NULL_VALUE, False

    def ifb(self, a: c_uint16, b: c_uint16) -> (c_uint16, c_uint16, bool):
        return c_uint16(np.bitwise_and(a.value, b.value) != 0), NULL_VALUE, False