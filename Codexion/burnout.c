#include "codexion.h"


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

long long   get_burnout(t_coder *coder)
{
    long long   burnout;

    burnout = 0;
    pthread_mutex_lock(&coder->mutex_burnout);
    burnout = coder->time_burnout;
    pthread_mutex_unlock(&coder->mutex_burnout);
    return (burnout);
}

void    set_burnout(t_coder *coder)
{
    pthread_mutex_lock(&coder->mutex_burnout);
    coder->time_burnout = get_time_ms();
    pthread_mutex_unlock(&coder->mutex_burnout);
}
