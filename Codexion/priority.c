#include "codexion.h"


long long   get_burnout(t_coder *coder)
{
    long long   burnout;

    burnout = 0;
    pthread_mutex_lock(&coder->mutex_burnout);
    burnout = coder->time_burnout;
    pthread_mutex_unlock(&coder->mutex_burnout);
    return (burnout);
}

int  heap_compare(t_coder *curr, t_coder *coder)
{
    return (get_burnout(curr) < get_burnout(coder));
}

void heap_swap(t_coder **tree, int i, int j)
{
    t_coder *tmp;

    tmp = tree[i];
    tree[i] = tree[j];
    tree[j] = tmp;
}

void    heap_push(t_heap *heap, t_coder *coder)
{
    int i;

    i = heap->size;
    heap->tree[i] = coder;
    heap->size += 1;
    while (i > 0)
    {
        if (heap_compare(heap->tree[i], heap->tree[(i - 1) / 2]))
        {
            heap_swap(heap->tree, i, (i - 1) / 2);
            i = (i - 1) / 2;
        }
        else
            break;
    }
}

void    scheduler_edf_add(t_data *data, t_coder *coder)
{
    t_heap  *heap;

    heap = &data->heap_ctrl;
    pthread_mutex_lock(&heap->lock);
    heap_push(heap, coder);
    pthread_cond_broadcast(&heap->cond);
    pthread_mutex_unlock(&heap->lock);
    while (get_simulation(data) == 1)
    {
        if (ispriority(data, coder))
        {
            if (take_dongle(coder) == 0)
                break;
        }
        usleep(500);
    }
    pthread_mutex_lock(&heap->lock);
    heap_pop(heap, coder);
    pthread_cond_broadcast(&heap->cond);
    pthread_mutex_unlock(&heap->lock);
}