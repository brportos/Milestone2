#include "codexion.h"


static int parse_data(t_data *data, int *argc);
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
