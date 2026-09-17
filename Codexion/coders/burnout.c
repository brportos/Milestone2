/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   burnout.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: brportos <brportos@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/09/07 19:17:58 by brportos          #+#    #+#             */
/*   Updated: 2026/09/12 13:06:25 by brportos         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

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
		else if (data->coder[i].coder_compiled >= data->required_compile)
		{
			i++;
			continue ;
		}
		else if ((get_time_ms()
				- get_burnout(&data->coder[i])) > data->max_burnout)
		{
			stop_simulation(data);
			display_log(data->coder[i].id, "burns_out", data);
			return (1);
		}
		i++;
	}
	return (0);
}

long	get_burnout(t_coder *coder)
{
	long	burnout;

	burnout = 0;
	pthread_mutex_lock(&coder->mutex_burnout);
	burnout = coder->time_burnout;
	pthread_mutex_unlock(&coder->mutex_burnout);
	return (burnout);
}

void	set_burnout(t_coder *coder)
{
	pthread_mutex_lock(&coder->mutex_burnout);
	coder->time_burnout = get_time_ms();
	pthread_mutex_unlock(&coder->mutex_burnout);
}
