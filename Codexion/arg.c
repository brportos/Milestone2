/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   arg.c                                              :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: portos <portos@student.42.fr>              +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/09/07 19:17:53 by brportos          #+#    #+#             */
/*   Updated: 2026/09/10 17:34:42 by portos           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

static int	parse_data(t_data *data, int *argc);

int	isargs_valid(t_data *data, char **argv)
{
	int	i;
	int	parsed_argv[8];

	i = 1;
	while (i != 8)
	{
		parsed_argv[i - 1] = atoi(argv[i]);
		if (parsed_argv[i - 1] >= 1)
		{
			if (i == 1 && parsed_argv[i - 1] >= MAX_CODERS)
				return (display_error("coders must be < ", argv[i], data));
			i++;
		}
		else
			return (display_error("coders must be > ", argv[i], data));
	}
	if (parse_data(data, parsed_argv) == 1 || init_struct(data) == 1)
		return (1);
	if (strcmp(FIFO, argv[i]) == 0 || strcmp(EDT, argv[i]) == 0)
		data->scheduler = argv[i];
	else
		return (display_error("Invalid argument ", argv[i], data));
	return (0);
}

static int	parse_data(t_data *data, int *parsed_argv)
{
	data->coder = malloc(sizeof(t_coder) * parsed_argv[0]);
	if (!data->coder)
		return (display_error("Can't allocate ", NULL, data));
	data->dongle = malloc(sizeof(t_dongle) * parsed_argv[0]);
	if (!data->dongle)
		return (display_error("Can't allocate ", NULL, data));
	data->ncoder = parsed_argv[0];
	data->ndongle = parsed_argv[0];
	data->max_burnout = parsed_argv[1];
	data->time_compile = parsed_argv[2];
	data->time_debug = parsed_argv[3];
	data->time_refactor = parsed_argv[4];
	data->required_compile = parsed_argv[5];
	data->dongle_cooldown = parsed_argv[6];
	return (0);
}

int	add_to_queue(t_queue_manager *manager, t_coder *coder)
{
	t_queue	*queue;

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
