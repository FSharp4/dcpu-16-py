package com.fsharp4.jdcpu16;

public class StackPointer {
    public short value = 0;
    public StackPointer() {
        value = 0;
    }

    public short peekPointerValue() {
        return value;
    }

    public short popPointerValue() {
        return value++;
    }

    public short pushPointerValue() {
        return --value;
    }
}
