#include "codexion.h"


int isfifo(t_data *data)
{
    if (strcmp(FIFO, data->scheduler) == 0)
        return (1);
    return (0);
}

int add_to_queue(t_queue_manager *manager, t_coder *coder)
{
    t_queue *queue;

    queue = malloc(sizeof(t_queue));
    if (!queue)
        return (1);
    queue->coder = coder;
    queue->next = NULL;
    if (manager->first == NULL)
    {
        manager->first = queue;
        manager->last = queue;
    }
    else
    {
        manager->last->next = queue;
        manager->last = queue;
    }
    return (0);
}

static void fifo_add_queue(t_data *data, t_coder *coder)
{
    add_to_queue(&data->queue_ctrl, coder);
    while ((get_simulation(data) == 1) && (data->queue_ctrl.first->coder != coder || take_dongle(coder) == 1))
    {
        if (get_simulation(data) == 1 && data->queue_ctrl.first->coder == coder)
        {
            pthread_mutex_unlock(&data->queue_ctrl.lock);
            usleep(1000);
            pthread_mutex_lock(&data->queue_ctrl.lock);
        }
        else
            pthread_cond_wait(&data->queue_ctrl.cond, &data->queue_ctrl.lock);
    }
}

int scheduler_fifo(t_data *data, t_coder *coder, char *action)
{
    pthread_mutex_lock(&data->queue_ctrl.lock);
    if (strcmp(action, "add_queue") == 0)
        fifo_add_queue(data, coder);
    else if (strcmp(action, "remove_queue") == 0)
    {
        remove_from_queue(&data->queue_ctrl);
        pthread_cond_broadcast(&data->queue_ctrl.cond);
    }
    pthread_mutex_unlock(&data->queue_ctrl.lock);
    return (0);
}

int remove_from_queue(t_queue_manager *manager)
{
    t_queue *tmp;

    if (manager->first == NULL)
        return (1);
    tmp = manager->first;
    manager->first = tmp->next;
    if (manager->first == NULL)
        manager->last = NULL;
    free (tmp);
    return (0);
}