#include "codexion.h"


static int parse_data(t_data *data, int *argc);
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
