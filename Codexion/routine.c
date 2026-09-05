#include "codexion.h"


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
