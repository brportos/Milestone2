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

int	get_simulation(t_data *data)
{
	int	simul;

	simul = 0;
	pthread_mutex_lock(&data->mutex_simul);
	simul = data->active_simulation;
	pthread_mutex_unlock(&data->mutex_simul);
	return (simul);
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