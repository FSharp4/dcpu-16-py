package com.fsharp4.jdcpu16;

public class Assembler {
    /*
     * Possibilities:
     * - Opcode:
     *  - Simple
     *  - Complex
     * - Operand A:
     *  - Literal
     *  - Register
     *  - Memory address (register as pointer)
     *  - Stack pointer POP
     *  - Stack pointer PEEK
     *  - Stack pointer PUSH
     * 
     * - Operand B:
     *  - Literal
     *  - Register
     *  - Memory address (register as pointer)
     */
    public static Instruction assemble(Opcode opcode, byte operandA, byte operandB) {
        // return new Instruction(new short[] {
        //     (short) (opcode.ordinal() << 12 | operandA),
        //     operandB
        // });
        short[] value = new short[3];
        value[0] = (short) (opcode.ordinal());
        value[0] += ((short) operandA) << 4;
        value[0] += ((short) operandB) << 10;
        return new Instruction(value);
    }

    public static Instruction assemble(ComplexOpcode opcode, byte operand) {
        short[] value = new short[3];
        // value[0] = (short) (opcode.ordinal() << 12 | operand);
        value[0] = (short) (opcode.ordinal() << 4);
        value[0] += ((short) operand) << 10;
        return new Instruction(value);
    }

    public static Instruction assemble(Opcode opcode, short memoryAddress, RegisterLabel registerlabel) {
        short[] value = new short[3];
        value[0] = (short) (opcode)
    }
}
