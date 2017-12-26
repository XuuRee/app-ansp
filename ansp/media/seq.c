#include "pb071_io.h"
#include <stdio.h>

void sequence(int number) {
    for (int j = 1 ; ; j++) {
        for (int i = 1; i <= j; i++) {
            printf("%d", i);
            number--;
            if (number == 0) {
                printf("\n");
                return;
            } else {
                printf(",");
            }
        }
    }
}

int main(void)
{
    printf("Number: ");
    unsigned int number = readUInt();

    if (number == 0) {
        printf("No sequence\n");
    } else {
        printf("First N(%d): ", number);
        sequence(number);
    }

    return 0;
}

