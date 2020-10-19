#include <stdio.h>
#include <stdlib.h>
#include "structs.h"
#include "transaction_sets.c"

int main()
{
    int i, j;

    struct trans_set *set1 = build_trans_set("input.txt");

    print_trans_set(set1);

    return 1;
}