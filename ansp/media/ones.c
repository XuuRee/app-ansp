#include "pb071_io.h"
#include <stdio.h>

int ones(unsigned long long number) {
    int sum = 0;

    while (number) {
        if (number & 1) {
            sum++;
        }
        number >>= 1;
    }

    return sum;
}

int main(void)
{
    printf("Number: ");
    unsigned long long number = readULongLong();

    printf("Number 0x%llx has %d ones.\n", number, ones(number));

    return 0;
}

