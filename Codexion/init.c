#include "codexion.h"

static void init_dongles_mutex(t_data *data)
{
    int i;

    i = 0;
    while (i != data->ncoder)
    {
        pthread_mutex_init(&data->dongle[i].lock, NULL);
        pthread_mutex_init(&data->coder[i].mutex_burnout, NULL);
        pthread_mutex_init(&data->coder[i].mutex_done, NULL);
        i++;
    }
}

static void init_mutex_cond(t_data *data)
{
    pthread_cond_init(&data->queue_ctrl.cond, NULL);
    pthread_cond_init(&data->heap_ctrl.cond, NULL);
}
void    init_mutex(t_data *data)
{
    pthread_mutex_init(&data->mutex_print, NULL);
    pthread_mutex_init(&data->mutex_simul, NULL);
    pthread_mutex_init(&data->queue_ctrl.lock, NULL);
    pthread_mutex_init(&data->heap_ctrl.lock, NULL);
    init_dongles_mutex(data);
    init_mutex_cond(data);
}

void    *monitoring_simulation(void *arg)
{
    t_data  *data;
    int done;

    data = (t_data *)arg;
    while (get_simulation(data) == 1)
    {
        if (check_burnout(data, &done) == 1) 
            return (NULL);
        if (done == data->ncoder)
        {
            stop_simulation(data);
            pthread_mutex_lock(&data->mutex_print);
            printf("All succed compile\n");
            pthread_mutex_unlock(&data->mutex_print);
            return (NULL);
        }
        usleep(100);
    }
    return (NULL);
}

void    init_pthread(t_data *data)
{
    int i;

    i = 0;
    pthread_create(&data->monitoring_id, NULL, &monitoring_simulation, data);
    while (i != data->ncoder)
    {
        pthread_create(&data->coder[i].thread, NULL, &coder_start_routine, &data->coder[i]);
        i++;
    }
}
