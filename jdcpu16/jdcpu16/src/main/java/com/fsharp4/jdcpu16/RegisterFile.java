package com.fsharp4.jdcpu16;

public class RegisterFile {
    // public short A = 0;
    // public short B = 0;
    // public short C = 0;
    // public short X = 0;
    // public short Y = 0;
    // public short Z = 0;
    // public short I = 0;
    // public short J = 0;
    public short[] registers = new short[8];
    public RegisterFile() {
        registers[0] = 0;
        registers[1] = 0;
        registers[2] = 0;
        registers[3] = 0;
        registers[4] = 0;
        registers[5] = 0;
        registers[6] = 0;
        registers[7] = 0;
    }

    public short getRegister(RegisterLabel label) {
        return registers[label.ordinal()];
    }

    public void setRegister(RegisterLabel label, short value) {
        registers[label.ordinal()] = value;
    }
}
