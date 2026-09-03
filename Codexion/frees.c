#include "codexion.h"

void    free_momory(t_data *data)
{
    t_queue *curr;
    t_queue *next;

    curr = data->queue_ctrl.first;
    if (data->coder != NULL)
        free(data->coder);
    if (data->dongle != NULL)
        free(data->dongle);
    
    while (curr != NULL)
    {
        next = curr->next;
        free(curr);
        curr = next;
    }
}

int display_error(char  *string, char *details, t_data *data)
{
    if (data != NULL)
        free_momory(data);
    fprintf(stderr, "\033[31mError\033[0m: %s", string);
    if (details != NULL)
        fprintf(stderr, "%s", details);
    fprintf(stderr, "\n");
    return (1);
}

long long   get_simul_time(t_data *data)
{
    return (get_time_ms() - data->start_time);
}

void    set_done(t_coder *coder)
{
    pthread_mutex_lock(&coder->mutex_done);
    coder->have_done = 1;
    pthread_mutex_unlock(&coder->mutex_done);
}

void    release_dongles(t_coder *coder, t_data *data)
{
    long long   curr_time;

    curr_time = get_simul_time(data);
    coder->ldongle->cooldown = curr_time + data->dongle_cooldown;
    if (coder->rdongle != NULL)
        coder->rdongle->cooldown = curr_time + data->dongle_cooldown;
    pthread_mutex_unlock(&coder->ldongle->lock);
    if (coder->rdongle != NULL)
        pthread_mutex_unlock(&coder->rdongle->lock);
    if (isfifo(data))
    {
        pthread_mutex_lock(&data->queue_ctrl.lock);
        pthread_cond_broadcast(&data->queue_ctrl.cond);
        pthread_mutex_unlock(&data->queue_ctrl.lock);
    }
    else
    {
        pthread_mutex_lock(&data->heap_ctrl.lock);
        pthread_cond_broadcast(&data->heap_ctrl.cond);
        pthread_mutex_unlock(&data->heap_ctrl.lock);
    }
}
