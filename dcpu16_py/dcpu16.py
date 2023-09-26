from ctypes import c_ubyte, c_uint16

import numpy as np
from dcpu16_py.enums.opcode_modes import OpcodeMode
from dcpu16_py.instructions.opcodes import evaluate_mode
from dcpu16_py.logic.alu import ALU
from dcpu16_py.memory.interconnect import Interconnect
from dcpu16_py.memory.ram import RAMBank
from dcpu16_py.memory.registers import Registers


class DCPU16:
    def __init__(self):
        self.stall = False
        self.nop = False
        self.clock_time = 0
        self._interconnect = Interconnect(RAMBank(), Registers())
        self.alu = ALU()
    
    def ram(self):
        return self._interconnect.rambank
    
    def registers(self):
        return self._interconnect.registers
        
    def do_clock_cycle(self):
        self.clock_time = 1
        self.nop = False
        
    def decode_valuecodes(self, a: c_ubyte, b: c_ubyte):
        _a = self.decode_valuecode(a)
        _b = self.decode_valuecode(b)
        
    def decode_valuecode(self, valuecode: c_ubyte):
        if np.bitwise_and(valuecode, c_ubyte(0x20)) > 0:
            return c_uint16(valuecode.value - 0x20)
            
        mode = evaluate_mode(valuecode)
        lookup_code = int(np.bitwise_and(valuecode, c_ubyte(0x07)))
        if mode is OpcodeMode.REG:
            return self.registers().instant_register_lookup[lookup_code]
        elif mode is OpcodeMode.DEREF:
            return self._interconnect.instant_deref(lookup_code)
        elif mode is OpcodeMode.DEREF_OFF():
            next_word = self._interconnect._next_word()
            self.do_clock_cycle()
            address = self._interconnect.delay_offset_lookup(lookup_code, next_word)
            return self.ram().read_word(address)
        else: # elif mode is OpcodeMode.SPECIAL():
            if lookup_code >= 6:
                self.do_clock_cycle()
            
            return self._interconnect.pseudo_register_lookup(lookup_code)
    
    def do_instruction(self):
        current_address = self.registers().PC.read()
        self.registers().PC.set(c_uint16(current_address.value + 1))
        instruction = self.ram().read_word(current_address)
        basic_opcode = np.bitwise_and(0x000F, instruction)
        if basic_opcode != 0:
            b_valcode = c_ubyte(np.bitwise_and(0xFB00, instruction))
            a_valcode = c_ubyte(np.bitwise_and(0x03F0, instruction))
            _a, _b = self.decode_valuecodes(a_valcode, b_valcode)
            result, carryout, do_carry = self.alu.do_basic_instruction(basic_opcode, _a, _b)
        
            if basic_opcode >= 0xC:
                self.nop = True
            else:
                if do_carry:
                    self.registers().O.set(carryout)
                
                self.do_write(a_valcode, result)
    
    def do_write(self, valuecode: c_ubyte, result: c_uint16):
        if np.bitwise_and(valuecode, c_ubyte(0x20)) > 0:
            return
        
        mode = evaluate_mode(valuecode)
        lookup_code = int(np.bitwise_and(valuecode, c_ubyte(0x07)))
        if mode is OpcodeMode.REG:
            return self.registers().instant_register_write_lookup[lookup_code](result)
        elif mode is OpcodeMode.DEREF:
            address = self._interconnect.instant_deref(lookup_code)
            self.ram().write_word(address, result)
        elif mode is OpcodeMode.DEREF_OFF():
            next_word = self._interconnect._next_word()
            # self.do_clock_cycle()
            address = self._interconnect.delay_offset_lookup(lookup_code, next_word)
            return self.ram().write_word(address, result)
        else: # elif mode is OpcodeMode.SPECIAL():
            if lookup_code >= 6:
                self.do_clock_cycle()
            
            return self._interconnect.pseudo_register_write_lookup(lookup_code, result)
    
    # -- SPECIAL --
    
    def jsr(self, a: c_uint16):
        pass
    
    def complain(self, a: c_uint16):
        raise RuntimeError("Undefined opcode (at nonbasic instruction)")
    
    def nonbasic_lookup(self, opcode: c_ubyte):
        table = [
            self.complain,
            self.jsr
        ]
        if opcode.value > 1:
            return table[0]
        
        return table[opcode.value]