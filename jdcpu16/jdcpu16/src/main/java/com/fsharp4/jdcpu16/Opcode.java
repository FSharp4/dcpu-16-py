package com.fsharp4.jdcpu16;

/**
 * Opcode enum.
 * Represents DCPU-16 simple opcodes.
 * 
 * <p>
 * In a basic instruction, the lower four bits of the first word of the 
 * instruction are the opcode. 
 * </p>
 * 
 * <b>Basic opcodes</b>: (<em>4 bits</em>)
 *
 * <ul>
 *  <li>0x0: Non-basic instruction (these always have their lower four bits unset)</li>
 *  <li>0x1: SET a, b - Sets a to b</li>
 *  <li>0x2: ADD a, b - Sets a to a+b, sets O to 0x0001 if there's an overflow, 0x0 otherwise</li>
 *  <li>0x3: SUB a, b - Sets a to a-b, sets O to 0xffff if there's an underflow, 0x0 otherwise</li>
 *  <li>0x4: MUL a, b - Sets a to a*b, sets O to ((a*b)>>16)&0xffff</li>
 *  <li>0x5: DIV a, b - Sets a to a/b, sets O to ((a<<16)/b)&0xffff. if b==0, sets a and O to 0 instead.</li>
 *  <li>0x6: MOD a, b - Sets a to a%b. if b==0, sets a to 0 instead.</li>
 *  <li>0x7: SHL a, b - Sets a to a<<b, sets O to ((a<<b)>>16)&0xffff</li>
 *  <li>0x8: SHR a, b - Sets a to a>>b, sets O to ((a<<16)>>b)&0xffff</li>
 *  <li>0x9: AND a, b - Sets a to a&b</li>
 *  <li>0xa: BOR a, b - Sets a to a|b</li>
 *  <li>0xb: XOR a, b - Sets a to a^b</li>
 *  <li>0xc: IFE a, b - Performs next instruction only if a==b</li>
 *  <li>0xd: IFN a, b - Performs next instruction only if a!=b</li>
 *  <li>0xe: IFG a, b - Performs next instruction only if a>b</li>
 *  <li>0xf: IFB a, b - Performs next instruction only if (a&b)!=0</li>
 * </ul>
 */
public enum Opcode {
    NON_BASIC,
    SET,
    ADD,
    SUB,
    MUL,
    DIV,
    MOD,
    SHL,
    SHR,
    AND,
    BOR,
    XOR,
    IFE,
    IFN,
    IFG,
    IFB;

    /**
     * Decoding method for opcode 4-bit value (taken from instruction).
     * 
     * @param value
     * @return
     */
    public static Opcode fromValue(int value) {
        return Opcode.values()[value];
    }

    /**
     * Instruction minimum timing getter
     * 
     * SET, AND, BOR and XOR take 1 cycle, plus the cost of a and b
     * ADD, SUB, MUL, SHR, and SHL take 2 cycles, plus the cost of a and b
     * DIV and MOD take 3 cycles, plus the cost of a and b
     * IFE, IFN, IFG, IFB take 2 cycles, plus the cost of a and b, plus 1 if 
     * the test fails.
     * @return
     */
    public int timing() {
        switch (this) {
            case NON_BASIC: return -1;
            case SET: return 1;
            case ADD: return 2;
            case SUB: return 2;
            case MUL: return 2;
            case DIV: return 3;
            case MOD: return 3;
            case SHL: return 2;
            case SHR: return 2;
            case AND: return 1;
            case BOR: return 1;
            case XOR: return 1;
            case IFE: return 2;
            case IFN: return 2;
            case IFG: return 2;
            case IFB: return 2;
            default: throw new IllegalArgumentException("Invalid opcode value");
        }
    }
}
