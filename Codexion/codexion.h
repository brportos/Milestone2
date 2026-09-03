#ifndef CODEXION_H
#define CODEXION_H

#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <unistd.h>
#include <string.h>

#define MAX_CODERS 400
#define FIFO    "fifo"
#define EDT     "edf"

typedef struct s_data   t_data;
typedef struct s_dongle
{
    t_data          *data;
    long long       cooldown;
    char            id[10];
    pthread_mutex_t lock;
}                   t_dongle;

typedef struct s_coder
{
    t_data          *data;
    t_dongle        *ldongle;
    t_dongle        *rdongle;
    long long       time_burnout;
    int             id;
    int             coder_compiled;
    int             have_done;
    pthread_t       thread;
    pthread_mutex_t mutex_burnout;
    pthread_mutex_t mutex_done;
}                   t_coder;

typedef struct s_queue
{
    t_coder         *coder;
    struct s_queue  *next;
}                   t_queue;

typedef struct s_heap
{
    t_coder         *tree[MAX_CODERS];
    int             size;
    pthread_mutex_t lock;
    pthread_cond_t  cond;
}                   t_heap;

typedef struct s_queue_manager
{
    t_queue         *first;
    t_queue         *last;
    pthread_mutex_t lock;
    pthread_cond_t  cond;

}                   t_queue_manager;

typedef struct s_data
{
    t_coder         *coder;
    t_dongle        *dongle;
    t_heap          heap_ctrl;
    t_queue_manager queue_ctrl;
    long long       max_burnout;
    long  long      time_compile;
    long long       time_debug;
    long long       time_refactor;
    long long       dongle_cooldown;
    long long       start_time;
    char            *scheduler;
    int             ncoder;
    int             ndongle;
    int             required_compile;
    int             active_simulation;
    pthread_t       monitoring_id;
    pthread_mutex_t mutex_print;
    pthread_mutex_t mutex_simul;
}                   t_data;
int display_error(char  *string, char *details, t_data *data);
long long get_time_ms(void);
void init_coders(t_data *data, t_coder *coder, int count);
void	fill_dongle(char *string_id, int index);
long long	get_burnout(t_coder *coder);
int  heap_compare(t_coder *curr, t_coder *coder);
void    scheduler_edf_add(t_data *data, t_coder *coder);
void heap_swap(t_coder **tree, int i, int j);
int	check_burnout(t_data *data, int *done);
int	get_simulation(t_data *data);
int	take_dongle(t_coder *coder);
int scheduler_fifo(t_data *data, t_coder *coder, char *action);
int	isargs_valid(t_data *data, char **argv);
void    set_done(t_coder *coder);
void    init_mutex(t_data *data);
void    init_pthread(t_data *data);
void    stop_simulation(t_data *data);
void    stop_simulation(t_data *data);
void    display_log(int i, char *dongle_id, char *action, t_data *data);
void    join_thread(t_data *data);
void    destroy_mutex(t_data *data);
int isfifo(t_data *data);
int remove_from_queue(t_queue_manager *manager);
void    release_dongles(t_coder *coder, t_data *data);
int *do_action(t_coder *coder, char *action);
void	*coder_start_routine(void *arg);
long long   get_simul_time(t_data *data);
int ispriority(t_data *data, t_coder *coder);
void    heap_pop(t_heap *heap, t_coder *coder);
void    free_momory(t_data *data);
#endif