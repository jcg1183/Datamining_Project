#include <stdio.h>
#include <stdlib.h>
#include "structs.h"

int main()
{
    int i, j;

    struct trans_set transaction_list;
    struct trans_node *pcurr;

    transaction_list.num_trans = 3;
    transaction_list.trans_list = (struct trans_node **)malloc(transaction_list.num_trans * sizeof(struct trans_list *));

    if (transaction_list.trans_list == NULL)
    {
        printf("Transaction list memory allocation fail.\n");
        return -1;
    }

    for (i = 0; i < transaction_list.num_trans; i++)
    {
        for (j = 0; j < 5; j++)
        {
            if (j == 0)
            {
                transaction_list.trans_list[i] = (struct trans_node *)malloc(sizeof(struct trans_node));
                pcurr = transaction_list.trans_list[i];
                pcurr->item = j;
                pcurr->pnext = NULL;
            }
            else
            {
                pcurr->pnext = (struct trans_node *)malloc(sizeof(struct trans_node));
                pcurr = pcurr->pnext;
                pcurr->item = j;
                pcurr->pnext = NULL;
            }
        }
    }

    for (i = 0; i < transaction_list.num_trans; i++)
    {
        pcurr = transaction_list.trans_list[i];

        printf("[%d] : ", i);

        for (j = 0; j < 5; j++)
        {
            printf("%d ", pcurr->item);
            pcurr = pcurr->pnext;
        }

        printf("\n");
    }

    return 1;
}