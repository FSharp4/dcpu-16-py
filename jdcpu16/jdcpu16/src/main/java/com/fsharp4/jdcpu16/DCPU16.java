package com.fsharp4.jdcpu16;

/**
 * DCPU-16 class.
 * Emulates a DCPU-16 CPU.
 */
public class DCPU16 {
    public short[] memory = new short[0x10000];
    public RegisterFile registers = new RegisterFile();
    public short programCounter = 0;
    public short stackPointer = 0;
    public boolean overflow = false;
    public static void main( String[] args ) {
        System.out.println( "Hello World!" );
    }
}
