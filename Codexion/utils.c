#include "codexion.h"


int ispriority(t_data *data, t_coder *coder)
{
    int lelf_i;
    int right_i;
    long long   my_time;

    lelf_i = (coder->id - 2 + data->ncoder) % data->ncoder;
    right_i = coder->id % data->ncoder;
    my_time = get_burnout(coder);
    if (get_burnout(&data->coder[lelf_i]) < my_time)
        return (0);
    if (get_burnout(&data->coder[right_i]) < my_time)
        return (0);
    return (1);
}

void    heap_check_deadline(t_heap *heap, int i)
{
    int lft;
    int rgt;
    int small;

    while ((i * 2) + 1 < heap->size)
    {
        lft = (i * 2) + 1;
        rgt = (i * 2) + 1;
        small = lft;
        if (rgt < heap->size && heap_compare(heap->tree[rgt], heap->tree[lft]))
            small = rgt;
        if (heap_compare(heap->tree[small], heap->tree[i]))
        {
            heap_swap(heap->tree, i, small);
            i = small;
        }
        else
            break;
    }
}
void    heap_pop(t_heap *heap, t_coder *coder)
{
    int i;

    i = 0;
    while (i < heap->size)
    {
        if (heap->tree[i] == coder)
            break;
        i++;
    }
    if (i == heap->size)
        return ;
    heap->size--;
    heap->tree[i] = heap->tree[heap->size];
    while (i > 0 && heap_compare(heap->tree[i], heap->tree[(i - 1) / 2]))
    {
        heap_swap(heap->tree, i, (i - 1) / 2);
        i = (i - 1) / 2;
    }
    heap_check_deadline(heap, i);
}

void    set_burnout(t_coder *coder)
{
    pthread_mutex_lock(&coder->mutex_burnout);
    coder->time_burnout = get_time_ms();
    pthread_mutex_unlock(&coder->mutex_burnout);
}

int *do_action(t_coder *coder, char *action)
{
    if (get_simulation(coder->data) == 0)
        return (NULL);
    else if (strcmp(action, "compile") == 0)
    {
        set_burnout(coder);
        display_log(coder->id, 0, "compile", coder->data);
        usleep(coder->data->time_compile * 1000);
        coder->coder_compiled+= 1;
        if (coder->coder_compiled >= coder->data->required_compile)
            set_done(coder);
        release_dongles(coder, coder->data);
    }
    else if (strcmp(action, "debug") == 0)
    {
        display_log(coder->id, 0, "debug", coder->data);
        usleep(coder->data->time_debug * 1000);
    }
    else if (strcmp(action, "refactor") == 0)
    {
        display_log(coder->id, 0, "refactor", coder->data);
        usleep(coder->data->time_refactor * 1000);
    }
    return (0);
}
