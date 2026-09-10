#include "codexion.h"
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
void    display_log(int i, char *dongle_id, char *action, t_data *data);
int display_error(char  *string, char *details, t_data *data);

long long get_time_ms(void);
long long   get_simul_time(t_data *data);

long long	get_burnout(t_coder *coder);
int	check_burnout(t_data *data, int *done);
void    set_burnout(t_coder *coder);

void    heap_pop(t_heap *heap, t_coder *coder);
void    heap_push(t_heap *heap, t_coder *coder);

void    scheduler_edf_add(t_data *data, t_coder *coder);
int scheduler_fifo(t_data *data, t_coder *coder, char *action);
int isfifo(t_data *data);


void	fill_dongle(char *string_id, int index);
int	take_dongle(t_coder *coder);
void    release_dongles(t_coder *coder, t_data *data);
void init_dongles_mutex(t_data *data);

int	isargs_valid(t_data *data, char **argv);
int add_to_queue(t_queue_manager *manager, t_coder *coder);
int ispriority(t_data *data, t_coder *coder);
void    join_thread(t_data *data);
int *do_action(t_coder *coder, char *action);
int get_have_done(t_coder *coder);

void create_coders_and_dongles(t_data *data);

void    init_mutex(t_data *data);
void    init_pthread(t_data *data);
int	init_struct(t_data *data);
void	init_basic_data(t_data *data, t_coder *coder, int count);

void    stop_simulation(t_data *data);
int	get_simulation(t_data *data);

void	*coder_start_routine(void *arg);
void    *monitoring_simulation(void *arg);

void    destroy_mutex(t_data *data);
void    free_momory(t_data *data);
int remove_from_queue(t_queue_manager *manager);
#endif

int	main(int argc, char **argv)
{
	t_data	data;

	memset(&data, 0, sizeof(t_data));
	if (argc != 9)
		return (display_error("Argument invalid", NULL, &data));
	if (isargs_valid(&data, argv) == 1)
		return (1);
	init_mutex(&data);
	init_pthread(&data);
	join_thread(&data);
	destroy_mutex(&data);
	free_momory(&data);
	return (0);
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

int	isargs_valid(t_data *data, char **argv)
{
	int	i;
	int	parsed_argv[8];

	i = 1;
	while (i != 8)
	{
		parsed_argv[i -1] = atoi(argv[i]);
		if (parsed_argv[i -1] >= 1)
		{
			if (i == 1 && parsed_argv[i -1] >= MAX_CODERS)
				return (display_error("coders must be < ", argv[i], data));
			i++;
		}
		else
			return(display_error("coders must be > ", argv[i], data));
	}
	if (parse_data(data, parsed_argv) == 1 || init_struct(data) == 1)
		return (1);
	if (strcmp(FIFO, argv[i]) == 0 || strcmp(EDT, argv[i]) == 0)
		data->scheduler = argv[i];
	else
		return (display_error("Invalid argument ", argv[i], data));
	return (0);
}

static int parse_data(t_data *data, int *argc)
{
	data->coder = malloc(sizeof(t_coder) * argc[0]);
	if (!data->coder)
		return (display_error("Can't allocate ", NULL, data));
	data->dongle = malloc(sizeof(t_dongle) * argc[0]);
	if (!data->dongle)
		return(display_error("Can't allocate ", NULL, data));
	data->ncoder = argc[0];
	data->ndongle = argc[0];
	data->max_burnout = argc[1];
	data->time_compile = argc[2];
	data->time_debug = argc[3];
	data->time_refactor = argc[4];
	data->required_compile = argc[5];
	data->dongle_cooldown = argc[6];
	return (0);

}

int	init_struct(t_data *data)
{
	int	i;

	data->active_simulation = 1;
	data->start_time = get_time_ms();
	data->queue_ctrl.first = NULL;
	data->queue_ctrl.last = NULL;
	data->heap_ctrl.size = 0;
	i = 0;

	while (i < MAX_CODERS)
	{
		data->heap_ctrl.tree[i] = NULL;
		i++;
	}
	create_coders_and_dongles(data);
	return (0);
}

long long get_time_ms(void)
{
	struct timeval tv;

	gettimeofday(&tv, NULL);
	return((tv.tv_sec * 1000) + (tv.tv_usec / 1000));
}

void create_coders_and_dongles(t_data *data)
{
	int count;

	count = 0;
	while (data->ncoder != count)
	{
		init_coders(data, &data->coder[count], count);
		fill_dongle(data->dongle[count].id, count);
		data->dongle[count].cooldown = 0;
		data->dongle[count].data = data;
		count++;
	}
}

static void init_coders(t_data *data, t_coder *coder, int count)
{
	int	next_id;

	init_basic_data(data, coder, count);
	if (data->ncoder > 1)
	{
		next_id = (count + 1) % data->ncoder;
		if (count < next_id)
		{
			coder->ldongle = &data->dongle[count];
			coder->rdongle = &data->dongle[next_id];
		}
		else
		{
			coder->ldongle = &data->dongle[next_id];
			coder->rdongle = &data->dongle[count];
		}
	}
	else
	{
		coder->ldongle = &data->dongle[count];
		display_log(coder->id, coder->ldongle->id, "takedongle", coder->data);
	}
}

void	init_basic_data(t_data *data, t_coder *coder, int count)
{
	coder->id = count + 1;
	coder->time_burnout = get_time_ms();
	coder->coder_compiled = 0;
	coder->have_done = 0;
	coder->data = data;
	coder->ldongle = NULL;
	coder->rdongle = NULL;
}

void    display_log(int i, char *dongle_id, char *action, t_data *data)
{
    long long time;

    (void)dongle_id;
    pthread_mutex_lock(&data->mutex_print);
    time = get_time_ms() - data->start_time;
    if (strcmp(action, "takedongle") == 0)
        printf("%lld %d has taken a dongle\n", time, i);
    else if (strcmp(action, "compile") == 0)
        printf("%lld %d is compiling\n", time, i);
    else if (strcmp(action, "debug") == 0)
        printf("%lld %d is debugging\n", time, i);
    else if (strcmp(action, "refactor") == 0)
        printf("%lld %d is refactoring\n", time, i);
    else if(strcmp(action, "burns_out") == 0)
        printf("%lld %d burned out\n", time, i);
    pthread_mutex_unlock(&data->mutex_print);

}

void	fill_dongle(char *string_id, int index)
{
	int	i;
	int	len;
	char	temp[10];

	i = 0;
	while (index >= 0)
	{
		temp[i++] = (index % 26);
		index = (index / 26) - 1;
	}
	temp[i] = '\0';
	len = i;
	i = 0;
	while (i < len)
	{
		string_id[i] = temp[len - 1 - i];
		i++;
	}
	string_id[i] = '\0';
	
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

void init_dongles_mutex(t_data *data)
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
            printf("\033[31mAll compiled successfully.\033[0m\n");
            pthread_mutex_unlock(&data->mutex_print);
            return (NULL);
        }
        usleep(100);
    }
    return (NULL);
}

int	get_simulation(t_data *data)
{
	int	simul;

	simul = 0;
	pthread_mutex_lock(&data->mutex_simul);
	simul = data->active_simulation;
	pthread_mutex_unlock(&data->mutex_simul);
	return (simul);
}

int	check_burnout(t_data *data, int *done)
{
	int	i;

	i = 0;
	*done = 0;
	while (data->ncoder != i)
	{
		if (get_have_done(&data->coder[i]) == 1)
			(*done)++;
		else if ((get_time_ms() - get_burnout(&data->coder[i])) > data->max_burnout)
		{
			stop_simulation(data);
			display_log(data->coder[i].id, 0, "burns_out", data);
			return (1);
		}
		i++;
	}
	return (0);
}

int get_have_done(t_coder *coder)
{
	int	done;

	done = 0;
	pthread_mutex_lock(&coder->mutex_done);
	done = coder->have_done;
	pthread_mutex_unlock(&coder->mutex_done);
	return (done);
}

long long   get_burnout(t_coder *coder)
{
    long long   burnout;

    burnout = 0;
    pthread_mutex_lock(&coder->mutex_burnout);
    burnout = coder->time_burnout;
    pthread_mutex_unlock(&coder->mutex_burnout);
    return (burnout);
}

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

void	*coder_start_routine(void *arg)
{
	t_coder	*coder;

	coder = (t_coder *)arg;
	while (get_simulation(coder->data) == 1 && coder->have_done == 0)
	{
		if (isfifo(coder->data))
			scheduler_fifo(coder->data, coder, "add_queue");
		else
			scheduler_edf_add(coder->data, coder);
		do_action(coder, "compile");
		if (isfifo(coder->data))
			scheduler_fifo(coder->data, coder, "remove_queue");
		do_action(coder, "debug");
		do_action(coder, "refactor");
	}
	return (NULL);
}

int isfifo(t_data *data)
{
    if (strcmp(FIFO, data->scheduler) == 0)
        return (1);
    return (0);
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

static int  heap_compare(t_coder *curr, t_coder *coder)
{
    return (get_burnout(curr) < get_burnout(coder));
}

static void heap_swap(t_coder **tree, int i, int j)
{
    t_coder *tmp;

    tmp = tree[i];
    tree[i] = tree[j];
    tree[j] = tmp;
}

int ispriority(t_data *data, t_coder *coder)
{
    int lelf_i;
    int right_i;
    long long   my_time;

    lelf_i = (coder->id - 2 + data->ncoder) % data->ncoder;
    right_i = coder->id % data->ncoder;
    my_time = get_burnout(coder);
    if (get_burnout(&data->coder[lelf_i]) < my_time)
        return (0);
    if (get_burnout(&data->coder[right_i]) < my_time)
        return (0);
    return (1);
}

int	take_dongle(t_coder *coder)
{
	if (try_take_dongle(coder->ldongle, coder->data) == 0)
	{
		if (coder->rdongle == NULL)
		{
			pthread_mutex_unlock(&coder->ldongle->lock);
			return (1);
		}
		if (try_take_dongle(coder->rdongle, coder->data) == 0)
		{
			display_log(coder->id, coder->ldongle->id, "takedongle", coder->data);
			display_log(coder->id, coder->rdongle->id, "takedongle", coder->data);
			return (0);
		}
		else
		{
			pthread_mutex_unlock(&coder->ldongle->lock);
			return (1);
		}
	}
	return (1);
}

static int	try_take_dongle(t_dongle *dongle, t_data *data)
{
	pthread_mutex_lock(&dongle->lock);
	if (get_simul_time(data) >= dongle->cooldown)
		return (0);
	pthread_mutex_unlock(&dongle->lock);
	return (1);
}

long long   get_simul_time(t_data *data)
{
    return (get_time_ms() - data->start_time);
}

void    heap_pop(t_heap *heap, t_coder *coder)
{
    int i;

    i = 0;
    while (i < heap->size)
    {
        if (heap->tree[i] == coder)
            break;
        i++;
    }
    if (i == heap->size)
        return ;
    heap->size--;
    heap->tree[i] = heap->tree[heap->size];
    while (i > 0 && heap_compare(heap->tree[i], heap->tree[(i - 1) / 2]))
    {
        heap_swap(heap->tree, i, (i - 1) / 2);
        i = (i - 1) / 2;
    }
    heap_check_deadline(heap, i);
}

static void    heap_check_deadline(t_heap *heap, int i)
{
    int lft;
    int rgt;
    int small;

    while ((i * 2) + 1 < heap->size)
    {
        lft = (i * 2) + 1;
        rgt = (i * 2) + 1;
        small = lft;
        if (rgt < heap->size && heap_compare(heap->tree[rgt], heap->tree[lft]))
            small = rgt;
        if (heap_compare(heap->tree[small], heap->tree[i]))
        {
            heap_swap(heap->tree, i, small);
            i = small;
        }
        else
            break;
    }
}

int *do_action(t_coder *coder, char *action)
{
    if (get_simulation(coder->data) == 0)
        return (NULL);
    else if (strcmp(action, "compile") == 0)
    {
        set_burnout(coder);
        display_log(coder->id, 0, "compile", coder->data);
        usleep(coder->data->time_compile * 100);
        coder->coder_compiled+= 1;
        if (coder->coder_compiled >= coder->data->required_compile)
            set_done(coder);
        release_dongles(coder, coder->data);
    }
    else if (strcmp(action, "debug") == 0)
    {
        display_log(coder->id, 0, "debug", coder->data);
        usleep(coder->data->time_debug * 100);
    }
    else if (strcmp(action, "refactor") == 0)
    {
        display_log(coder->id, 0, "refactor", coder->data);
        usleep(coder->data->time_refactor * 100);
    }
    return (0);
}

void    set_burnout(t_coder *coder)
{
    pthread_mutex_lock(&coder->mutex_burnout);
    coder->time_burnout = get_time_ms();
    pthread_mutex_unlock(&coder->mutex_burnout);
}

static void    set_done(t_coder *coder)
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

static void destroy_mutex_cond(t_data *data)
{
    pthread_cond_destroy(&data->queue_ctrl.cond);
    pthread_cond_destroy(&data->heap_ctrl.cond);
}

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

