#include "codexion.h"


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

void init_coders(t_data *data, t_coder *coder, int count)
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
		coder->ldongle = &data->dongle[count];
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

int	try_take_dongle(t_dongle *dongle, t_data *data)
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
