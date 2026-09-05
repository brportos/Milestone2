#include "codexion.h"


static void init_coders(t_data *data, t_coder *coder, int count)
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
