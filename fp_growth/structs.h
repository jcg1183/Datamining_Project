

/*************************************************
 * transaction_set linked list
 * 
 * 
 ************************************************/

struct trans_node
{
    int item;
    struct trans_node *pnext;
} trans_node;

struct trans_set
{
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
    struct tree_node *item_in_tree;
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
    struct tree_node *parent;
    struct tree_node **children;
    struct tree_node *next_item;

} tree_node;

struct tree
{
    struct tree_node *tree;
} tree;