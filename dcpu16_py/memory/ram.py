from ctypes import c_uint16
import numpy as np

class RAMBank:
    def __init__(self):
        self._ram = np.zeros(0x10000, dtype=np.int16)
    
    def read_word(self, address: c_uint16):
        return c_uint16(self._ram[address.value])
    
    def write_word(self, address: c_uint16, value: c_uint16):
        self._ram[address.value] = value.value
        
    