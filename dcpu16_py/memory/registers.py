from ctypes import c_uint16

from traitlets import Callable

class _Register:
    def __init__(self, value: c_uint16 = c_uint16(0)):
        self.value = value
        
    def read(self):
        return c_uint16(self.value.value)
    
    def set(self, value: c_uint16):
        self.value = c_uint16(value.value)

class Registers:
    def __init__(self):
        # General Purpose Registers
        self.A = _Register()
        self.B = _Register()
        self.C = _Register()
        self.X = _Register()
        self.Y = _Register()
        self.Z = _Register()
        self.I = _Register()
        self.J = _Register()
        
        # Specialized Registers
        
        self.SP = _Register(c_uint16(0xFFFF))
        self.PC = _Register()
        self.O = _Register() # Status register
        
        self.instant_register_lookup: tuple[c_uint16] = (
            self.A.read(),
            self.B.read(),
            self.C.read(),
            self.X.read(),
            self.Y.read(),
            self.Z.read(),
            self.I.read(),
            self.J.read(),
        )
        
        self.instant_register_write_lookup: tuple[Callable[..., None]] (
            self.A.set(),
            self.B.set(),
            self.C.set(),
            self.X.set(),
            self.Y.set(),
            self.Z.set(),
            self.I.set(),
            self.J.set()
        )
