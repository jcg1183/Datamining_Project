#ifndef HEADER_FILE
#define HEADER_FILE

/*************************************************
 * transaction_set linked list
 * 
 * 
 ************************************************/

struct trans_node
{
    int item;
    int order;
    struct trans_node *pnext;
} trans_node;

struct trans_set
{
    int num_items;
    int num_trans;
    struct trans_node **trans_list;
} trans_set;

/*************************************************
 * support_count linked list
 * 
 * 
 ************************************************/

struct support_node
{
    int item;
    int count;
    int order;
    struct tree_node *head_tree;
    struct tree_node *end_tree;
} support_node;

struct support_set
{
    int num_items;
    struct support_node **support_list;
} support_set;

/*************************************************
 * tree linked list
 * 
 * 
 ************************************************/

struct tree_node
{
    int item;
    int count;
    int num_children;
    struct tree_node *parent;
    struct tree_node **children;
    struct tree_node *next_item;

} tree_node;

struct tree
{
    struct tree_node *tree;
} tree;

#endif