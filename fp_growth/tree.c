#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "structs.h"

struct tree *build_tree(struct support_set *support1, struct trans_set *transaction1);
void add_trans_to_tree(struct tree *tree1, struct trans_node *head, struct support_set *support1);
struct tree_node *child_exists(int item, struct tree_node *children);
void print_fp_tree(struct tree *tree, struct support_set *support1);
void rec_fp_print(struct tree_node *tree, struct support_set *support1);

struct tree *build_tree(struct support_set *support1, struct trans_set *transaction1)
{
    int i, j, k;

    struct tree *tree1;

    tree1 = (struct tree *)malloc(sizeof(struct tree));

    tree1->tree = (struct tree_node *)malloc(sizeof(struct tree_node));

    tree1->tree->item = -1;
    tree1->tree->count = -1;
    tree1->tree->parent = NULL;

    tree1->tree->children = (struct tree_node **)malloc(support1->num_items * sizeof(struct tree_node *));
    memset(tree1->tree->children, 0, support1->num_items * sizeof(struct tree_node *));

    tree1->tree->next_item = NULL;

    for (i = 0; i < transaction1->num_trans; i++)
    {
        add_trans_to_tree(tree1, transaction1->trans_list[i], support1);
    }

    return tree1;
}

void add_trans_to_tree(struct tree *tree1, struct trans_node *head, struct support_set *support1)
{
    struct trans_node *p_trans_linked;
    struct tree_node *p_tree_parent;
    struct tree_node *p_tree_node;
    struct tree_node *p_children;
    struct tree_node *new_tree_node;

    p_trans_linked = head;
    p_tree_node = tree1->tree;

    while (p_trans_linked != NULL)
    {
        if (p_tree_node->children[p_trans_linked->item] != NULL)
        {
            p_tree_node = p_tree_node->children[p_trans_linked->item];
            p_tree_node->count += 1;
            p_trans_linked = p_trans_linked->pnext;
        }
        else
        {
            //build new tree_node
            new_tree_node = (struct tree_node *)malloc(sizeof(struct tree_node));

            p_tree_node->children[p_trans_linked->item] = new_tree_node;
            p_tree_node->num_children += 1;
            p_tree_node = new_tree_node;

            new_tree_node->item = p_trans_linked->item;
            p_trans_linked = p_trans_linked->pnext;

            new_tree_node->count = 1;

            new_tree_node->num_children = 0;

            new_tree_node->parent = p_tree_node;

            new_tree_node->children = (struct tree_node **)malloc(support1->num_items * sizeof(struct tree_node *));
            memset(new_tree_node->children, 0, support1->num_items * sizeof(struct tree_node *));

            new_tree_node->next_item = NULL;

            if (support1->support_list[new_tree_node->item]->head_tree == NULL)
            {
                support1->support_list[new_tree_node->item]->head_tree = new_tree_node;
                support1->support_list[new_tree_node->item]->end_tree = new_tree_node;
            }
            else
            {
                support1->support_list[new_tree_node->item]->end_tree->next_item = new_tree_node;
                support1->support_list[new_tree_node->item]->end_tree = support1->support_list[new_tree_node->item]->end_tree->next_item;
            }
        }
    }
}

void print_fp_tree(struct tree *tree, struct support_set *support1)
{
    int i;

    struct tree_node *pcurr;

    rec_fp_print(tree->tree, support1);

    printf("\nSupport Set\n");

    for (i = 0; i < support1->num_items; i++)
    {
        printf("item[%d]: ", i);
        pcurr = support1->support_list[i]->head_tree;

        while (pcurr != NULL)
        {
            printf("(%d, %d), ", pcurr->item, pcurr->count);
            pcurr = pcurr->next_item;
        }

        printf("\n");
    }
}

void rec_fp_print(struct tree_node *tree, struct support_set *support1)
{
    int i;

    printf("(%d, %d): ", tree->item, tree->count);

    for (i = 0; i < support1->num_items; i++)
    {
        if (tree->children[i] != NULL)
        {
            printf("(%d, %d), ", tree->children[i]->item, tree->children[i]->count);
        }
    }

    printf("\n");

    for (i = 0; i < support1->num_items; i++)
    {
        if (tree->children[i] != NULL)
        {
            rec_fp_print(tree->children[i], support1);
        }
    }

    return;
}