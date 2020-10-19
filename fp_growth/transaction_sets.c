#include <stdio.h>
#include <stdlib.h>
#include "structs.h"

void print_trans_set(struct trans_set *set1);
struct trans_set *build_trans_set(char *file_name);

void print_trans_set(struct trans_set *set1)
{
    int i;
    struct trans_node *pcurr;

    if (set1 == NULL)
    {
        return;
    }

    printf("\n-----Transaction Set-----\n\n");
    printf("num transactions: %d\n", set1->num_trans);
    printf("num unique items: %d\n\n", set1->num_items);

    for (i = 0; i < set1->num_trans; i++)
    {
        pcurr = set1->trans_list[i];

        printf("set[%d]: ", i + 1);

        while (pcurr != NULL)
        {
            printf("%d ", pcurr->item);
            pcurr = pcurr->pnext;
        }

        printf("\n");
    }

    printf("\n");
}

struct trans_set *build_trans_set(char *file_name)
{
    int i, j, num, temp, count;

    FILE *file = fopen(file_name, "r");

    struct trans_set *set1;

    struct trans_node *pcurr;
    struct trans_node *ptemp;

    if (file == NULL)
    {
        printf("Could not open file: %s\n", file_name);
        return NULL;
    }

    set1 = (struct trans_set *)malloc(sizeof(struct trans_set));

    if (set1 == NULL)
    {
        printf("Could not allocate transaction set memory.\n");
        return NULL;
    }

    // Read number of unique items in transaction list
    count = fscanf(file, "%d", &set1->num_items);

    if (count == 0)
    {
        printf("Could not read number of unique items in file: %s\n", file_name);
    }

    // Read number of transactions in transaction list
    count = fscanf(file, "%d", &set1->num_trans);

    if (count == 0)
    {
        printf("Could not read number of transactions in file: %s\n", file_name);
    }

    set1->trans_list = (struct trans_node **)malloc(set1->num_trans * sizeof(struct trans_node *));

    if (set1->trans_list == NULL)
    {
        printf("Could not allocate memory for transaction list\n");
    }

    for (i = 0; i < set1->num_trans; i++)
    {
        set1->trans_list[i] = NULL;

        count = fscanf(file, "%d", &num);

        for (j = 0; j < num; j++)
        {
            ptemp = (struct trans_node *)malloc(sizeof(trans_node));

            if (ptemp == NULL)
            {
                printf("Could not allocate trans_node memory.\n");
                exit(0);
            }

            count = fscanf(file, "%d", &ptemp->item);
            ptemp->pnext = NULL;

            if (j == 0)
            {
                set1->trans_list[i] = ptemp;
                pcurr = set1->trans_list[i];
            }
            else
            {
                pcurr->pnext = ptemp;
                pcurr = pcurr->pnext;
            }
        }
    }

    return set1;
}