#include <stdio.h>
#include <stdlib.h>
#include "structs.h"

struct trans_set *build_trans_set(char *file_name);
void print_trans_set(struct trans_set *set1);

void sort_trans_item_sets(struct support_set *support1, struct trans_set *transaction1);
void bubbleSort(struct trans_node *start);
void swap(struct trans_node *a, struct trans_node *b);

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
                set1->trans_list[i]->order = 0;
                pcurr = set1->trans_list[i];
            }
            else
            {
                pcurr->pnext = ptemp;
                set1->trans_list[i]->order = 0;
                pcurr = pcurr->pnext;
            }
        }
    }

    return set1;
}

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
            printf("%d, ", pcurr->item);
            pcurr = pcurr->pnext;
        }

        printf("\n");
    }

    printf("\n");
}

void sort_trans_item_sets(struct support_set *support1, struct trans_set *transaction1)
{
    int i;

    struct trans_node *pcurr;

    for (i = 0; i < transaction1->num_trans; i++)
    {
        pcurr = transaction1->trans_list[i];

        while (pcurr != NULL)
        {
            pcurr->order = support1->support_list[pcurr->item]->order;
            pcurr = pcurr->pnext;
        }

        bubbleSort(transaction1->trans_list[i]);
    }

    return;
}

/* Bubble sort the given linked list */
void bubbleSort(struct trans_node *start)
{
    int swapped, i;
    struct trans_node *ptr1;
    struct trans_node *lptr = NULL;

    /* Checking for empty list */
    if (start == NULL)
        return;

    do
    {
        swapped = 0;
        ptr1 = start;

        while (ptr1->pnext != lptr)
        {
            if (ptr1->order > ptr1->pnext->order)
            {
                swap(ptr1, ptr1->pnext);
                swapped = 1;
            }
            ptr1 = ptr1->pnext;
        }
        lptr = ptr1;
    } while (swapped);
}

/* function to swap data of two nodes a and b*/
void swap(struct trans_node *a, struct trans_node *b)
{
    int temp_order = a->order;
    a->order = b->order;
    b->order = temp_order;

    int temp_item = a->item;
    a->item = b->item;
    b->item = temp_item;
}
