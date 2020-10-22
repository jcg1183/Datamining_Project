#include <stdio.h>
#include <stdlib.h>
#include "structs.h"
#include "transaction_sets.c"
#include "support_count.c"

int main()
{
    int i, j;

    struct trans_set *transaction_set = build_trans_set("input.txt");

    print_trans_set(transaction_set);

    struct support_set *support1 = build_support_set(transaction_set);

    add_support_order(support1, transaction_set);

    print_support_set(support1);

    sort_trans_item_sets(support1, transaction_set);

    print_trans_set(transaction_set);

    return 1;
}