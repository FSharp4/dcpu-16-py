package com.fsharp4.jdcpu16;

/**
 * Non-basic opcode enum.
 * Represents DCPU-16 non-basic opcodes.
 * 
 * <p>Non-basic opcodes always have their lower four bits unset.</p>
 * <ul>
 *  <li>0x00: Reserved for future expansion</li>
 *  <li>0x01: JSR a - Pushes the address of the next instruction to the stack, then sets PC to a</li>
 *  <li>0x02-0x3f: Reserved</li>
 * </ul>
 * 
 */
public enum ComplexOpcode {
    RESERVED_EXPANSION,
    JSR,
    RESERVED;

    /**
     * Decoding method for complex opcode 6-bit value (taken from instruction).
     * 
     * @param value Opcode to decode
     * @return Decoded opcode enum value
     */
    public static ComplexOpcode fromValue(int value) {
        switch (value) {
            case 0x00: return RESERVED_EXPANSION;
            case 0x01: return JSR;
            default: if (value >= 0x02 && value <= 0x3f) return RESERVED;
            throw new IllegalArgumentException("Invalid opcode value");
        }
    }

    public int timing() {
        switch (this) {
            case RESERVED_EXPANSION: return -1;
            case RESERVED: return -1;
            case JSR: return 2;
            default: throw new IllegalArgumentException("Invalid opcode value");
        }
    }
}
