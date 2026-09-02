#include "codexion.h"


int	main(int argc, char **argv)
{
	t_data	data;

	memset(&data, 0, sizeof(t_data));
	if (argc != 9)
		return (display_error("Invalid arg", NULL, &data));
	if (isargs_valid(&data, argv) == 1)
		return (1);
	init_mutex(&data);
	init_pthread(&data);
	join_thread(&data);
	destroy_mutex(&data);
	
	return (0);
}
