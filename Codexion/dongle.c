#include "codexion.h"


void    take_dongle(t_dongle *d, t_sim *sim)
{
    pthread_mutex_lock(&d->lock);
    while (d->taken || now_ms(sim) < d->free_at_ms)
        pthread_cond_wait(&d->cond, &d->lock);
    d->taken = 1;
    pthread_mutex_unlock(&d->lock);
}

void    release_dongle(t_dongle *d, t_sim *sim)
{
    pthread_mutex_lock(&d->lock);
    d->taken = 0;
    d->free_at_ms = now_ms(sim) + sim->dongle_cooldown;
    pthread_cond_broadcast(&d->cond);
    pthread_mutex_unlock(&d->lock);
}

int check_burnout(t_sim *sim)
{
    int i;
    long   elapsed;

    i = 0;
    while (i < sim->n)
    {
        elapsed = now_ms(sim) - sim->coders[i].last_compile_start;
        if (elapsed > sim->time_to_burnout)
        {
            set_stop_flag(sim);
            log_event(&sim->coders[i], "burned out");
            wake_all_dongles(sim);
            return (1);
        }
        i++;
    }
    return (0);
}

int check_all_compiled(t_sim *sim)
{
    int i;

    i = 0;
    while (i < sim->n)
    {
        if (sim->coders[i].compile_count < sim->compiles_required)
            return (0);
        i++;
    }
    set_stop_flag(sim);
    wake_all_dongles(sim);
    return (1);
}

void *monitor_routine(void *arg)
{
    t_sim   *sim;

    sim = (t_sim *)arg;
    while (1)
    {
        if (check_burnout(sim))
            return (NULL);
        if (check_all_compiled(sim))
            return (NULL);
        usleep(100);
    }
}
