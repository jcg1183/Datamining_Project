#include <stdio.h>
#include <stdlib.h>
#include "structs.h"
#include "transaction_sets.c"
#include "support_count.c"
#include "tree.c"

int main()
{
    int i, j;

    struct trans_set *transaction_set = build_trans_set("fp_growth167.txt");

    print_trans_set(transaction_set);

    struct support_set *support1 = build_support_set(transaction_set);

    add_support_order(support1, transaction_set);

    print_support_set(support1);

    sort_trans_item_sets(support1, transaction_set);

    print_trans_set(transaction_set);

    struct tree *tree1 = build_tree(support1, transaction_set);

    print_fp_tree(tree1, support1);

    return 1;
}
