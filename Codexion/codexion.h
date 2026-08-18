#ifndef CODEXION_H
#define CODEXION_H

#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <unistd.h>
#include <string.h>


typedef struct s_dongle
{
    int             id;
    int             taken;
    long       free_at_ms;
    pthread_mutex_t lock;
    pthread_cond_t cond;
} t_dongle;

typedef struct s_sim t_sim;

typedef struct s_coder
{
    int id;
    int compile_count;
    long   last_compile_start;
    t_dongle   *left;
    t_dongle    *right;
    t_sim     *sim;
} t_coder;

typedef struct s_sim
{
    int n;
    long   time_to_burnout;
    long   time_to_compile;
    long   time_to_debug;
    long   time_to_refactor;
    int compiles_required;
    long   dongle_cooldown;
    char    scheduler[5];

    t_dongle    *dongles;
    t_coder     *coders;

    long   start_time;
    int         stop_flag;
    pthread_mutex_t stop_lock;

    pthread_mutex_t log_lock;
}t_sim;

int stopped(t_sim *sim);
void *coder_routine(void *arg);
void    log_event(t_coder *me, const char *msg);
long   now_ms(t_sim *sim);

char *ft_strcpy(char *dest, const char *src);
void    parse_and_validate_args(int argc, char **argv, t_sim *sim);
void    init_dongles(t_sim *sim);
void    init_coders(t_sim *sim, t_coder *coders);

void    destroy_dongle(t_sim *sim);
void *monitor_routine(void *arg);
void set_stop_flag(t_sim *sim);
void wake_all_dongles(t_sim *sim);
void    take_dongle(t_dongle *d, t_sim *sim);
void    release_dongle(t_dongle *d, t_sim *sim);

int init_simulation(t_sim *sim);
int alloc_sim_data(t_sim *sim, t_coder **coders, pthread_t ** threads);
void    cleanup_simulation(t_sim *sim, t_coder *coders, pthread_t *threads);
int run_threads(t_sim *sim, pthread_t *threads);

#endif