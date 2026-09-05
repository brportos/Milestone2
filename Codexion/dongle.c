#include "codexion.h"


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

static int	try_take_dongle(t_dongle *dongle, t_data *data)
{
	pthread_mutex_lock(&dongle->lock);
	if (get_simul_time(data) >= dongle->cooldown)
		return (0);
	pthread_mutex_unlock(&dongle->lock);
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
