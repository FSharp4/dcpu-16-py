from ctypes import c_uint16

from dcpu16_py.memory.ram import RAMBank
from dcpu16_py.memory.registers import Registers


class Interconnect:
    def __init__(self, rambank: RAMBank, registers: Registers):
        self.rambank = rambank
        self.registers = registers
        
    def instant_deref(self, regcode: int):
        address = c_uint16(self.registers.instant_register_lookup[regcode].value)
        return self.rambank.read_word(address)
    
    def delay_offset_lookup(self, regcode: int, offset: c_uint16):
        value = self.registers.instant_register_lookup[regcode]
        return c_uint16(value.value + offset.value)
    
    def _pop(self):
        address = self.registers.SP.read()
        self.registers.SP.set(c_uint16(address.value + 1))
        return self.rambank.read_word(address)
    
    def _write_pop(self, result: c_uint16):
        address = self.registers.SP.read()
        self.registers.SP.set(c_uint16(address.value + 1))
        self.rambank.write_word(address, result)
    
    def _peek(self):
        address = self.rambank.SP.read()
        return self.rambank.read_word(address)
    
    def _write_peek(self, result: c_uint16):
        address = self.rambank.SP.read()
        self.rambank.write_word(address, result)
    
    def _push(self):
        self.registers.SP.set(c_uint16(self.registers.SP.read().value - 1))
        return self._peek()
    
    def _write_push(self, result: c_uint16):
        self.registers.SP.set(c_uint16(self.registers.SP.read().value - 1))
        self._write_peek(result)
    
    def _next_word_literal(self):
        address = self.registers.PC.read()
        self.registers.PC.set(c_uint16(address.value + 1))
        return self.rambank.read_word(address)
    
    def do_nothing(self, result: c_uint16 | None = None):
        pass
    
    def _next_word(self):
        address = self._next_word_literal()
        return self.rambank.read_word(address)
    
    def _next_word_write(self, result: c_uint16):
        address = self._next_word_literal()
        self.rambank.write_word(address, result)
    
    def pseudo_register_lookup(self, regcode: int) -> c_uint16:
        lut: tuple[c_uint16] = (
            self._pop(),
            self._peek(),
            self._push(),
            self.registers.SP.read(),
            self.registers.PC.read(),
            self.registers.O.read(), # effectively a status register
            self._next_word(),
            self._next_word_literal()
        )
        
        return lut[regcode]
    
    def complain(self, regcode: int):
        raise RuntimeError(f"Cannot write to this location register {regcode}: not a memory register")
    
    def pseudo_register_write_lookup(self, regcode: int, value: c_uint16):
        lut: tuple = (
            self._write_pop,
            self._write_peek,
            self._write_push,
            self.registers.SP.set,
            self.registers.PC.set,
            self.registers.O.set,
            self._next_word_write,
            self.do_nothing
        )
        
        lut[regcode](value)
