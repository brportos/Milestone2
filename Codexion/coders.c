#include "codexion.h"


int stopped(t_sim *sim)
{
    int val;

    pthread_mutex_lock(&sim->stop_lock);
    val = sim->stop_flag;
    pthread_mutex_unlock(&sim->stop_lock);
    return (val);
}

void    log_event(t_coder *me, const char *msg)
{
    long   elapsed;

    pthread_mutex_lock(&me->sim->log_lock);
    elapsed = now_ms(me->sim) - me->sim->start_time;
    printf("%ld %d %s\n", elapsed, me->id, msg);
    pthread_mutex_unlock(&me->sim->log_lock);
}

long   now_ms(t_sim *sim)
{
    struct timeval  tv;
    gettimeofday(&tv, NULL);
    return ((tv.tv_sec *100L) + (tv.tv_usec / 100L) - sim->start_time);
}

void *coder_routine(void *arg)
{
    t_coder *me;
    
    me =(t_coder *)arg;
    while (!stopped(me->sim))
    {
        take_dongle(me->left, me->sim);
        take_dongle(me->right, me->sim);
        log_event(me, "is compiling");
        me->last_compile_start = now_ms(me->sim);
        usleep(me->sim->time_to_compile * 100);
        me->compile_count++;
        release_dongle(me->left, me->sim);
        release_dongle(me->right, me->sim);

        log_event(me, "is debugging");
        usleep(me->sim->time_to_debug * 100);

        log_event(me, "is refactoring");
        usleep(me->sim->time_to_refactor * 100);
    }
    return (NULL);
}

void    wake_all_dongles(t_sim *sim)
{
    int i;

    i = 0;
    while (i < sim->n)
    {
        pthread_mutex_lock(&sim->dongles[i].lock);
        pthread_cond_broadcast(&sim->dongles[i].cond);
        pthread_mutex_unlock(&sim->dongles[i].lock);
        i++;
    }
}
