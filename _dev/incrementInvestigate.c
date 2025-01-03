#include <stdio.h>

int main() {
    int a = 0;
    printf("a++ = %d at time of execution\n", a++);
    a = 0;
    printf("++a = %d at time of execution\n", ++a);
    a = 0;
    printf("a-- = %d at time of execution\n", a--);
    a = 0;
    printf("--a = %d at time of execution\n", --a);
    return 0;
}