#include <stdio.h>
#include <stdlib.h>
#include "structs.h"

void print_trans_set(struct trans_set *set1);
struct trans_set *build_trans_set(char *file_name);

void sort_trans_item_sets(struct support_set *support1, struct trans_set *transaction1);
void bubbleSort(struct trans_node *start);
void swap(struct trans_node *a, struct trans_node *b);

void items_merge(struct support_set *set1, int l, int m, int r)
{
    int n1 = m - l + 1;
    int n2 = r - m;
    int i, j, k;

    // Create temp arrays

    struct support_node *L[n1];
    struct support_node *R[n2];

    // Copy data to temp arrays L[] and R[]
    for (i = 0; i < n1; i++)
    {
        L[i] = set1->support_list[l + i];
    }

    for (j = 0; j < n2; j++)
    {

        R[j] = set1->support_list[m + 1 + j];
    }
    // Merge the temp arrays back into arr[l..r]

    // Initial index of first subarray
    i = 0;

    // Initial index of second subarray
    j = 0;

    // Initial index of merged subarray
    k = l;

    while (i < n1 && j < n2)
    {
        if (L[i]->count >= R[j]->count)
        {
            set1->support_list[k] = L[i];
            i++;
        }
        else
        {
            set1->support_list[k] = R[j];
            j++;
        }
        k++;
    }

    // Copy the remaining elements of
    // L[], if there are any
    while (i < n1)
    {
        set1->support_list[k] = L[i];
        i++;
        k++;
    }

    // Copy the remaining elements of
    // R[], if there are any
    while (j < n2)
    {
        set1->support_list[k] = R[j];
        j++;
        k++;
    }
}

void sort_item_set(struct support_set *set1, int l, int r)
{
    if (l < r)
    {
        int m = l + (r - l) / 2;

        // Sort first and second halves
        sort_item_set(set1, l, m);
        sort_item_set(set1, m + 1, r);

        items_merge(set1, l, m, r);
    }
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