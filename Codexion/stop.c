#include "codexion.h"


void    stop_simulation(t_data *data)
{
    pthread_mutex_lock(&data->mutex_simul);
    data->active_simulation = 0;
    pthread_mutex_unlock(&data->mutex_simul);
    pthread_mutex_lock(&data->queue_ctrl.lock);
    pthread_cond_broadcast(&data->queue_ctrl.cond);
    pthread_mutex_unlock(&data->queue_ctrl.lock);
    pthread_mutex_lock(&data->heap_ctrl.lock);
    pthread_cond_broadcast(&data->heap_ctrl.cond);
    pthread_mutex_unlock(&data->heap_ctrl.lock);
}

void    display_log(int i, char *dongle_id, char *action, t_data *data)
{
    long long time;

    pthread_mutex_lock(&data->mutex_print);
    time = get_time_ms() - data->start_time;
    if (strcmp(action, "takedongle") == 0)
        printf("[%lld] Coder %d has taken dongle %s\n", time, i, dongle_id);
    else if (strcmp(action, "compile") == 0)
        printf("[%lld] Coder %d is compiling (%d)\n", time, i, data->coder[i -1].coder_compiled + 1);
    else if (strcmp(action, "debug") == 0)
        printf("[%lld] Coder %d is debugging\n", time, i);
    else if (strcmp(action, "refactor") == 0)
        printf("[%lld] Coder %d is refactoring\n", time, i);
    else if(strcmp(action, "burns_out") == 0)
        printf("[%lld] Coder %d burned out\n", time, i);
    pthread_mutex_unlock(&data->mutex_print);

}

void    join_thread(t_data *data)
{
    int i;

    i = 0;
    pthread_join(data->monitoring_id, NULL);
    while (i != data->ncoder)
    {
        pthread_join(data->coder[i].thread, NULL);
        i++;
    }
}

static void destroy_mutex_cond(t_data *data)
{
    pthread_cond_destroy(&data->queue_ctrl.cond);
    pthread_cond_destroy(&data->heap_ctrl.cond);
}

void    destroy_mutex(t_data *data)
{
    int i;

    i = 0;
    while (i != data->ncoder)
    {
        pthread_mutex_destroy(&data->dongle[i].lock);
        pthread_mutex_destroy(&data->coder[i].mutex_burnout);
        pthread_mutex_destroy(&data->coder[i].mutex_done);
        i++;
    }
    pthread_mutex_destroy(&data->mutex_print);
    pthread_mutex_destroy(&data->mutex_simul);
    pthread_mutex_destroy(&data->queue_ctrl.lock);
    pthread_mutex_destroy(&data->heap_ctrl.lock);
    destroy_mutex_cond(data);
}