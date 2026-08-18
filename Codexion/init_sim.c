#include "codexion.h"


int init_simulation(t_sim *sim)
{
    struct timeval tv;
    gettimeofday(&tv, NULL);
    sim->start_time = (tv.tv_sec * 100L) + (tv.tv_usec / 100L);
    sim->stop_flag = 0;
    if (pthread_mutex_init(&sim->stop_lock, NULL) != 0)
        return (0);
    if (pthread_mutex_init(&sim->log_lock, NULL) != 0)
    {
        pthread_mutex_destroy(&sim->stop_lock);
        return (0);
    }
    init_dongles(sim);
    return (1);
}

int alloc_sim_data(t_sim *sim, t_coder **coders, pthread_t ** threads)
{
    *coders = malloc(sizeof(t_coder) * sim->n);
    *threads = malloc(sizeof(pthread_t) * sim->n);
    if (!*coders || !*threads)
        return(free(*coders), free(*threads), 0);
    init_coders(sim, *coders);
    sim->coders = *coders;
    return (1);
}

int run_threads(t_sim *sim, pthread_t *threads)
{
    pthread_t   monitor;
    int         i;

    i = 0;
    while (i < sim->n)
    {
        pthread_create(&threads[i], NULL, coder_routine, &sim->coders[i]);
        i++;
    }
    pthread_create(&monitor, NULL, monitor_routine, sim);
    i = 0;
    while (i < sim->n)
    {
        pthread_join(threads[i], NULL);
        i++;
    }
    pthread_join(monitor, NULL);
    return (1);
}

void set_stop_flag(t_sim *sim)
{
    pthread_mutex_lock(&sim->stop_lock);
    sim->stop_flag = 1;
    pthread_mutex_unlock(&sim->stop_lock);
}