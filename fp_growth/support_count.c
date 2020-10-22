#include <stdio.h>
#include <stdlib.h>
#include "structs.h"

struct support_set *build_support_set(struct trans_set *transaction_set);
void print_support_set(struct support_set *set1);

void sort_support_set(struct support_set *set1, int l, int r);
void merge(struct support_set *set1, int l, int m, int r);

void unmerge(struct support_set *set1, int l, int m, int r);
void unsort_support_set(struct support_set *set1, int l, int r);

struct trans_node *sort_trans_items(struct support_set *support_set1, struct trans_set *trans_set1);
void add_support_order(struct support_set *support_set1, struct trans_set *trans_set1);

struct trans_node *sort_trans_items(struct support_set *support_set1, struct trans_set *trans_set1)
{
    int i;

    struct trans_node *head;

    for (i = 0; i < trans_set1->num_trans; i++)
    {
        head = trans_set1->trans_list[i];
    }

    return NULL;
}

void add_support_order(struct support_set *support_set1, struct trans_set *trans_set1)
{

    sort_support_set(support_set1, 0, support_set1->num_items - 1);

    int i;

    for (i = 0; i < support_set1->num_items; i++)
    {
        support_set1->support_list[i]->order = i;
    }

    unsort_support_set(support_set1, 0, support_set1->num_items - 1);

    return;
}

void merge(struct support_set *set1, int l, int m, int r)
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

void sort_support_set(struct support_set *set1, int l, int r)
{
    if (l < r)
    {
        int m = l + (r - l) / 2;

        // Sort first and second halves
        sort_support_set(set1, l, m);
        sort_support_set(set1, m + 1, r);

        merge(set1, l, m, r);
    }
}

void unmerge(struct support_set *set1, int l, int m, int r)
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
        if (L[i]->item <= R[j]->item)
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

void unsort_support_set(struct support_set *set1, int l, int r)
{
    if (l < r)
    {
        int m = l + (r - l) / 2;

        // Sort first and second halves
        unsort_support_set(set1, l, m);
        unsort_support_set(set1, m + 1, r);

        unmerge(set1, l, m, r);
    }
}

void print_support_set(struct support_set *set1)
{
    int i;

    printf("\n-----Support Set-----\n");

    for (i = 0; i < set1->num_items; i++)
    {
        printf("Item %d: count: %d order %d\n", set1->support_list[i]->item, set1->support_list[i]->count, set1->support_list[i]->order);
    }

    return;
}

struct support_set *build_support_set(struct trans_set *transaction_set)
{
    int i, j;
    struct trans_node *pcurr;

    struct support_set *support_set;

    support_set = (struct support_set *)malloc(sizeof(struct support_set));

    support_set->num_items = transaction_set->num_items;

    support_set->support_list = (struct support_node **)malloc(support_set->num_items * sizeof(struct support_node *));

    for (i = 0; i < support_set->num_items; i++)
    {
        support_set->support_list[i] = (struct support_node *)malloc(sizeof(struct support_node));

        support_set->support_list[i]->item = i;
        support_set->support_list[i]->count = 0;
        support_set->support_list[i]->order = 0;
        support_set->support_list[i]->item_in_tree = NULL;
    }

    for (i = 0; i < transaction_set->num_trans; i++)
    {
        pcurr = transaction_set->trans_list[i];

        while (pcurr != NULL)
        {
            support_set->support_list[pcurr->item]->count += 1;
            pcurr = pcurr->pnext;
        }
    }

    return support_set;
}