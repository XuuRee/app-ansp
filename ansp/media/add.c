#include "pb071_io.h"
#include <stdio.h>

double add(double lhs, double rhs) {
    return lhs + rhs;
}

int main(void)
{
    printf("Enter 2 double numbers:\n");

    double lhs = readDouble();
    double rhs = readDouble();

    printf("%.4f + %.4f = %.4f\n", lhs, rhs, add(lhs, rhs));

    return 0;
}

