package com.fsharp4.jdcpu16;

/**
 * Instruction class.
 * Represents a single DCPU-16 instruction
 */
public class Instruction {
    public short[] value = new short[3];

    /**
     * Instruction constructor.
     * 
     * Instructions are 1-3 words (1 word = 16 bits) long and are fully defined 
     * by the first word.
     * 
     * @param value The instruction words. First word (value[0]) contains 
     *              definition.
     */
    public Instruction(short[] value) {
        this.value = value;
    }
    
    /**
     * Instruction opcode getter
     * 
     * In a basic instruction, the lower four bits of the first word of the 
     * instruction are the opcode.
     * 
     * @return Instruction opcode
     */
    public short opcode() {
        return (short) (value[0] & 0x0F);
    }

    /**
     * Instruction A operand getter
     * 
     * In a basic instruction, the lower six bits of the first word (after the 
     * opcode) is the "A" value which is handled first by the processor 
     * (before a second six-bit value "B").
     * @return "A"
     */
    public short operandA() {
        return (short) ((value[0] & 0b0000001111110000) >> 4);
    }

    /**
     * Instruction B operand getter
     * 
     * In a basic instruction, the highest six bits of the first word is the 
     * "B" value which is handled second by the processor (after "A")
     * @return
     */
    public short operandB() {
        return (short) ((value[0] & 0b1111110000000000) >> 10);
    }

    

    /**
     * Interprets a six-bit operand of an instruction
     * 
     * Values (6 bits):
     * - 0x00-0x07: register (A, B, C, X, Y, Z, I or J, in that order)
     * - 0x08-0x0f: [register]
     * - 0x10-0x17: [next word + register]
     * - 0x18: POP / [SP++]
     * - 0x19: PEEK / [SP]
     * - 0x1a: PUSH / [--SP]
     * - 0x1b: SP
     * - 0x1c: PC
     * - 0x1d: O
     * - 0x1e: [next word]
     * - 0x1f: next word (literal)
     *
     * "next word" == [PC++] (an increase of instruction length by 1 word)
     * 
     * If any instruction tries to assign a literal value, the assignment fails 
     * silently. Other than that, the instruction behaves as normal.
     * 
     * @param value
     * @return
     */
    public static String debugInterpret(byte value) {
        if (value >= 0 && value <= 7) {
            switch (value) {
                case 0: return "A";
                case 1: return "B";
                case 2: return "C";
                case 3: return "X";
                case 4: return "Y";
                case 5: return "Z";
                case 6: return "I";
                case 7: return "J";
            }
        } else if (value >= 8 && value <= 0x0f) {
            switch (value) {
                case 0x8: return "[A]";
                case 0x9: return "[B]";
                case 0xA: return "[C]";
                case 0xB: return "[X]";
                case 0xC: return "[Y]";
                case 0xD: return "[Z]";
                case 0xE: return "[I]";
                case 0xF: return "[J]";
            }
        } else if (value >= 0x10 && value <= 0x17) {
            switch (value) {
                case 0x10: return "[next word + A]";
                case 0x11: return "[next word + B]";
                case 0x12: return "[next word + C]";
                case 0x13: return "[next word + X]";
                case 0x14: return "[next word + Y]";
                case 0x15: return "[next word + Z]";
                case 0x16: return "[next word + I]";
                case 0x17: return "[next word + J]";
            }
        } else if (value >= 0x18 && value <= 0x1f) {
            switch (value) {
                case 0x18: return "POP";
                case 0x19: return "PEEK";
                case 0x1a: return "PUSH";
                case 0x1b: return "SP";
                case 0x1c: return "PC";
                case 0x1d: return "O";
                case 0x1e: return "[next word]";
                case 0x1f: return "next word (literal)";
            }
        } else if (value >= 0x20 && value <= 0x3f) {
            return String.format("literal value 0x%02x", value - 0x20);
        }

        return "?";
    }
}
