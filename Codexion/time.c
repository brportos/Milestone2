#include "codexion.h"


long long get_time_ms(void)
{
	struct timeval tv;

	gettimeofday(&tv, NULL);
	return((tv.tv_sec * 1000) + (tv.tv_usec / 1000));
}

long long   get_simul_time(t_data *data)
{
    return (get_time_ms() - data->start_time);
}
